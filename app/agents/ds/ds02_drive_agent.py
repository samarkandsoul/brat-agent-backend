import os
import json
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class DriveAgent:
    """
    Google Drive ilə işləyən agent.
    Service account JSON məlumatını GOOGLE_SERVICE_ACCOUNT env-dən oxuyur.
    Yaradılan qovluqları istəyə görə DRIVE_SHARE_EMAIL ünvanı ilə bölüşür.
    """

    def __init__(self) -> None:
        # Env-dən service account JSON-u oxu
        sa_raw = os.getenv("GOOGLE_SERVICE_ACCOUNT")
        if not sa_raw:
            raise RuntimeError("GOOGLE_SERVICE_ACCOUNT env boşdur")

        try:
            sa_info = json.loads(sa_raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"GOOGLE_SERVICE_ACCOUNT JSON parse xətası: {e!r}")

        # Drive üçün səlahiyyətlər
        scopes = ["https://www.googleapis.com/auth/drive"]

        self.creds = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=scopes,
        )

        # Drive service obyekti
        self.service = build("drive", "v3", credentials=self.creds)

        # Qovluqları kimlə paylaşaq? (sənin əsas Gmail ünvanın)
        self.share_email: Optional[str] = os.getenv("DRIVE_SHARE_EMAIL")

    def _find_existing_folder(self, name: str, parent_id: Optional[str]) -> Optional[str]:
        """
        Verilmiş parent altında adı 'name' olan qovluq varsa, onun ID-sini qaytarır.
        Yoxdursa, None qaytarır.
        """
        try:
            # Parent filter
            if parent_id:
                q = (
                    f"name = '{name}' and "
                    "mimeType = 'application/vnd.google-apps.folder' and "
                    f"'{parent_id}' in parents and trashed = false"
                )
            else:
                # Root səviyyəsində axtarış
                q = (
                    f"name = '{name}' and "
                    "mimeType = 'application/vnd.google-apps.folder' and "
                    "'root' in parents and trashed = false"
                )

            results = (
                self.service.files()
                .list(q=q, spaces="drive", fields="files(id, name)", pageSize=1)
                .execute()
            )

            files = results.get("files", [])
            if files:
                return files[0]["id"]
            return None
        except HttpError as e:
            print("Find folder error:", e)
            return None

    def _share_folder_if_needed(self, folder_id: str) -> None:
        """
        Əgər DRIVE_SHARE_EMAIL təyin olunubsa, qovluğu həmin mail ilə paylaşır.
        """
        if not self.share_email:
            return

        try:
            self.service.permissions().create(
                fileId=folder_id,
                body={
                    "role": "writer",
                    "type": "user",
                    "emailAddress": self.share_email,
                },
                fields="id",
                sendNotificationEmail=False,
            ).execute()
        except HttpError as e:
            print("Share folder error:", e)

    def create_or_get_folder(self, name: str, parent_id: Optional[str]) -> str:
        """
        Əvvəl qovluq varsa, onun ID-sini qaytarır.
        Yoxdursa, yeni qovluq yaradır və ID-ni qaytarır.
        """
        # Əvvəl mövcud qovluğu yoxlayaq (idempotent olsun)
        existing_id = self._find_existing_folder(name, parent_id)
        if existing_id:
            return existing_id

        # Yoxdursa, yenisini yaradırıq
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = (
            self.service.files()
            .create(body=file_metadata, fields="id")
            .execute()
        )
        folder_id = folder.get("id")

        # Qovluğu sənin Gmail ilə paylaş
        self._share_folder_if_needed(folder_id)

        return folder_id

    def process(self, command: str) -> str:
        """
        Komandalara misal:
          "Samarkand Soul System"
          "Samarkand Soul System / Business Core"
          "Samarkand Soul System / DS System / DS-01 - Market-Research-Master"

        MSP bizə artıq "drive:" hissəsiz payload ötürür, biz sadəcə
        path-i "/" ilə bölüb ardıcıl qovluqları yaradırıq.
        """
        raw = (command or "").strip()
        if not raw:
            return "Drive Agent: Komanda boşdur."

        # "Samarkand Soul System / DS System / DS-01 ..." → ["Samarkand Soul System", "DS System", ...]
        parts = [p.strip() for p in raw.split("/") if p.strip()]
        if not parts:
            return "Drive Agent: Qovluq adı tapılmadı."

        parent_id: Optional[str] = None
        created_path_parts = []

        try:
            for part in parts:
                folder_id = self.create_or_get_folder(part, parent_id)
                parent_id = folder_id
                created_path_parts.append(part)

            final_path = " / ".join(created_path_parts)
            folder_link = (
                f"https://drive.google.com/drive/folders/{parent_id}"
                if parent_id
                else "link tapılmadı"
            )

            msg = (
                "Drive Agent: Qovluq strukturu hazırdır.\n"
                f"Path: {final_path}\n"
            )
            if self.share_email:
                msg += f"Bu qovluq {self.share_email} ilə bölüşüldü.\n"

            msg += f"Link: {folder_link}"

            return msg

        except Exception as e:
            return f"Drive Agent xətası: {e!r}"
