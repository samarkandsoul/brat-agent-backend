# app/agents/ds/ds02_drive_agent.py

import os
import json
from typing import Optional

from googleapiclient.discovery import build
from google.oauth2 import service_account


class DriveAgent:
    """
    Google Drive ilə işləyən real agent.
    Verilən path üzrə (SamarkandSoulSystem / DS System / ...) qovluq zəncirini
    tapır, olmayanları yaradır və son qovluğun linkini qaytarır.
    """

    def __init__(self) -> None:
        # Service account JSON-u environment-dən oxuyuruq
        raw_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not raw_json:
            raise RuntimeError(
                "GOOGLE_SERVICE_ACCOUNT_JSON env dəyişəni tapılmadı. "
                "Render-də service account JSON mətnini bu dəyişənə yazmaq lazımdır."
            )

        try:
            info = json.loads(raw_json)
        except json.JSONDecodeError:
            raise RuntimeError(
                "GOOGLE_SERVICE_ACCOUNT_JSON düzgün JSON deyil. "
                "Service account .json faylının tam məzmununu oraya copy etməlisən."
            )

        scopes = ["https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=scopes,
        )

        # Drive API v3 client
        self.service = build("drive", "v3", credentials=creds)

    # ======== DAXİLİ KÖMƏKÇİ METODLAR ========

    def _find_folder(self, name: str, parent_id: Optional[str]) -> Optional[str]:
        """
        Verilən ad və parent-id üçün mövcud qovluğu tapır.
        Tapmasa None qaytarır.
        """
        # Parent varsa onu da query-yə əlavə edirik
        if parent_id:
            q = (
                f"name = '{name}' "
                "and mimeType = 'application/vnd.google-apps.folder' "
                "and trashed = false "
                f"and '{parent_id}' in parents"
            )
        else:
            q = (
                f"name = '{name}' "
                "and mimeType = 'application/vnd.google-apps.folder' "
                "and trashed = false"
            )

        resp = (
            self.service.files()
            .list(
                q=q,
                spaces="drive",
                fields="files(id, name)",
                pageSize=5,
            )
            .execute()
        )

        files = resp.get("files", [])
        if not files:
            return None

        # Birincini götürürük (adı eyni olan birdən çox qovluq olsa belə)
        return files[0]["id"]

    def _create_folder(self, name: str, parent_id: Optional[str]) -> str:
        """
        Verilən adla (və parent varsa) yeni qovluq yaradır və id qaytarır.
        """
        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            metadata["parents"] = [parent_id]

        folder = (
            self.service.files()
            .create(
                body=metadata,
                fields="id",
            )
            .execute()
        )

        return folder["id"]

    # ======== İCTİMAİ METOD ========

    def create_folder_path(self, path: str) -> str:
        """
        Məsələn:
        path = 'SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
        """
        clean = path.strip()
        if not clean:
            raise ValueError("Drive path boşdur.")

        # 'A / B / C' -> ['A', 'B', 'C']
        parts = [p.strip() for p in clean.split("/") if p.strip()]
        if not parts:
            raise ValueError("Drive path doğru formatda deyil.")

        parent_id: Optional[str] = None
        created_any = False

        for part in parts:
            # 1) Mövcud qovluğu axtar
            folder_id = self._find_folder(part, parent_id)

            # 2) Tapılmadısa – yarat
            if folder_id is None:
                folder_id = self._create_folder(part, parent_id)
                created_any = True

            parent_id = folder_id

        final_id = parent_id
        folder_link = f"https://drive.google.com/drive/folders/{final_id}"

        if created_any:
            status = "Yeni qovluq strukturu yaradıldı."
        else:
            status = "Bu qovluq strukturu artıq mövcuddur."

        return (
            "MSP cavabı:\n"
            f"{status}\n"
            f"Path: {clean}\n"
            f"Link: {folder_link}"
        )
