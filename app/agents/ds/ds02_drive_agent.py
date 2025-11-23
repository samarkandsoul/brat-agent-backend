import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class DriveAgent:
    def __init__(self):
        # Render env-dən Service Account JSON almaq
        service_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not service_json:
            raise Exception("Service Account JSON tapılmadı (GOOGLE_SERVICE_ACCOUNT_JSON)")

        # Credential yarat
        credentials = service_account.Credentials.from_service_account_info(
            eval(service_json),
            scopes=['https://www.googleapis.com/auth/drive']
        )

        self.drive = build('drive', 'v3', credentials=credentials)

    def create_folder(self, name, parent_id=None):
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = self.drive.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")

    def find_or_create(self, name, parent_id=None):
        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.drive.files().list(
            q=query, spaces='drive', fields="files(id, name)"
        ).execute()

        files = results.get("files", [])
        if files:
            return files[0]["id"]

        return self.create_folder(name, parent_id)

    def create_folder_path(self, path: str):
        parts = [p.strip() for p in path.split("/") if p.strip()]
        parent = None
        for p in parts:
            parent = self.find_or_create(p, parent)
        return f"Drive qovluqları yaradıldı: {path}"
