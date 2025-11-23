import os
import json
from typing import Optional, List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class DriveAgent:
    """
    SamarkandSoulSystem üçün qovluq generatoru.
    Verilən path-i (məs: 'SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master')
    hissələrə bölür və hər səviyyəni ardıcıl yaradır.
    """

    def __init__(self) -> None:
        # GOOGLE_SERVICE_ACCOUNT_JSON – Render env-də saxladığımız JSON
        service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        self.share_email = os.environ.get("DRIVE_SHARE_EMAIL")

        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
        ]
        creds = Credentials.from_service_account_info(
            service_account_info, scopes=scopes
        )
        self.service = build("drive", "v3", credentials=creds)

    def process(self, command: str) -> str:
        """
        command: msp-dən gələn PATH hissəsi.
        Məsələn:
          'SamarkandSoulSystem'
          'SamarkandSoulSystem / Business Core'
          'SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
        """
        path = command.strip()
        if not path:
            return "Drive Agent: Boş path göndərdin brat. Zəhmət olmasa qovluq adını yaz. 🙂"

        parts: List[str] = [p.strip() for p in path.split("/") if p.strip()]
        if not parts:
            return "Drive Agent: Path düzgün deyil, yenidən yoxlayaq. 🙂"

        try:
            parent_id: Optional[str] = None
            built_parts: List[str] = []

            for part in parts:
                folder_id = self._ensure_folder(part, parent_id)
                parent_id = folder_id
                built_parts.append(part)

            if parent_id is None:
                return "Drive Agent: Qovluq yaradıla bilmədi, path-i yenidən yoxlayaq."

            # İstəyə görə qovluğu əsas gmail ilə bölüş.
            if self.share_email:
                self._ensure_permission(parent_id, self.share_email)

            link = f"https://drive.google.com/drive/folders/{parent_id}"
            nice_path = " / ".join(built_parts)

            msg = (
                "Drive Agent: Qovluq strukturu hazırdır.\n"
                f"Path: {nice_path}\n"
            )
            if self.share_email:
                msg += f"Bu qovluq {self.share_email} ilə bölüşüldü.\n"
            msg += f"Link: {link}"
            return msg

        except HttpError as e:
            return f"Drive Agent: Google Drive xətası baş verdi: {e}"
        except Exception as e:
            # Burda heç vaxt səssiz kalmayaq
            return f"Drive Agent: Gözlənilməz xəta baş verdi: {e}"

    # --- Daxili helperlər ---

    def _ensure_folder(self, name: str, parent_id: Optional[str]) -> str:
        """
        Verilən parent altında bu adda qovluq varsa, onun id-sini qaytarır,
        yoxdursa yaradır.
        """
        query_parts = [f"name = '{name.replace(\"'\", \"\\\\'\")}'", "mimeType = 'application/vnd.google-apps.folder'", "trashed = false"]
        if parent_id:
            query_parts.append(f"'{parent_id}' in parents")
        query = " and ".join(query_parts)

        results = (
            self.service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=1)
            .execute()
        )
        files = results.get("files", [])
        if files:
            return files[0]["id"]

        metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata["parents"] = [parent_id]

        folder = self.service.files().create(body=metadata, fields="id").execute()
        return folder["id"]

    def _ensure_permission(self, file_id: str, email: str) -> None:
        """
        Qovluğu email ilə 'writer' kimi bölüşür (əgər artıq varsa, heç nə etmir).
        """
        try:
            perms = (
                self.service.permissions()
                .list(fileId=file_id, fields="permissions(emailAddress, role)")
                .execute()
            )
            for p in perms.get("permissions", []):
                if p.get("emailAddress") == email:
                    return
        except HttpError:
            # Əgər oxumağa icazə vermirsə, yenə də paylaşmağı yoxlayaq
            pass

        body = {
            "type": "user",
            "role": "writer",
            "emailAddress": email,
        }
        self.service.permissions().create(
            fileId=file_id,
            body=body,
            sendNotificationEmail=False,
        ).execute()
