import os
import json
from typing import Optional

from googleapiclient.discovery import build
from google.oauth2 import service_account


class DriveAgent:
    """
    Google Drive ilə işləyən agent.
    Verilən path üzrə qovluq zəncirini tapır, olmayanları yaradır
    və son qovluğun linkini qaytarır.
    """

    def __init__(self) -> None:
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
                "Service account .json faylının TAM məzmununu kopyalayıb oraya yapışdırmalısan."
            )

        scopes = ["https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=scopes,
        )

        self.service = build("drive", "v3", credentials=creds)

    def _find_folder(self, name: str, parent_id: Optional[str]) -> Optional[str]:
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

        return files[0]["id"]

    def _create_folder(self, name: str, parent_id: Optional[str]) -> str:
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

    def create_folder_path(self, path: str) -> str:
        clean = path.strip()
        if not clean:
            raise ValueError("Drive path boşdur.")

        parts = [p.strip() for p in clean.split("/") if p.strip()]
        if not parts:
            raise ValueError("Drive path doğru formatda deyil.")

        parent_id: Optional[str] = None
        created_any = False

        for part in parts:
            folder_id = self._find_folder(part, parent_id)
            if folder_id is None:
                folder_id = self._create_folder(part, parent_id)
                created_any = True
            parent_id = folder_id

        if parent_id is None:
            raise RuntimeError("Qovluq ID-si tapılmadı və ya yaradılmadı.")

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
