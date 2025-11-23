import os
import json
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/drive"]


class DriveAgent:
    def __init__(self) -> None:
        self.service = self._build_service()

    def _build_service(self):
        key_env = "GOOGLE_SERVICE_ACCOUNT_KEY"
        if key_env not in os.environ:
            raise RuntimeError(
                f"{key_env} env variable not set in Render."
            )

        try:
            info = json.loads(os.environ[key_env])
        except json.JSONDecodeError as e:
            raise RuntimeError(
                "GOOGLE_SERVICE_ACCOUNT_KEY is not valid JSON"
            ) from e

        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        service = build("drive", "v3", credentials=creds)
        return service

    def handle_drive_command(self, path_str: str, user_email: str) -> str:
        """
        Creates the full folder path in Google Drive and shares
        the last folder with `user_email`.
        """
        print(f"[DriveAgent] handle_drive_command path='{path_str}'", flush=True)

        folder_id = self._ensure_path(path_str)
        self._share_folder(folder_id, user_email)

        link = f"https://drive.google.com/drive/folders/{folder_id}"
        return (
            "Drive Agent: Qovluq strukturu hazirdir.\n"
            f"Path: {path_str}\n"
            f"Link: {link}"
        )

    def _ensure_path(self, path_str: str) -> str:
        parts = [p.strip() for p in path_str.split("/") if p.strip()]
        if not parts:
            raise ValueError("Boş path göndərilib")

        parent_id = "root"
        for name in parts:
            parent_id = self._find_or_create_folder(name, parent_id)

        return parent_id

    def _find_or_create_folder(self, name: str, parent_id: str) -> str:
        # Search
        query = (
            f"mimeType='application/vnd.google-apps.folder' "
            f"and name='{name}' and '{parent_id}' in parents "
            f"and trashed = false"
        )

        res = self.service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)",
        ).execute()

        files = res.get("files", [])
        if files:
            folder_id = files[0]["id"]
            print(f"[DriveAgent] Found folder '{name}' -> {folder_id}", flush=True)
            return folder_id

        # Create
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = self.service.files().create(
            body=file_metadata,
            fields="id",
        ).execute()

        folder_id = folder["id"]
        print(f"[DriveAgent] Created folder '{name}' -> {folder_id}", flush=True)
        return folder_id

    def _share_folder(self, folder_id: str, user_email: str) -> None:
        print(f"[DriveAgent] Sharing {folder_id} with {user_email}", flush=True)
        try:
            permission = {
                "type": "user",
                "role": "writer",
                "emailAddress": user_email,
            }
            self.service.permissions().create(
                fileId=folder_id,
                body=permission,
                sendNotificationEmail=False,
            ).execute()
        except HttpError as e:
            # Əgər artıq share olunubsa və s., burda sadəcə log yazırıq
            print(f"[DriveAgent] share error: {e}", flush=True)
