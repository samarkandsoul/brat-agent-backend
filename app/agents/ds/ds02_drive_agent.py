import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class DriveAgent:
    def __init__(self):
        # Service account key file
        key_path = os.path.join(os.getcwd(), "google_key.json")

        # Authenticate
        self.creds = service_account.Credentials.from_service_account_file(
            key_path,
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        # Drive service
        self.service = build("drive", "v3", credentials=self.creds)

    def create_folder(self, name, parent_id=None):
        """Creates a Google Drive folder and returns its ID."""
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }

        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")

    def process(self, command: str):
        """
        Processes commands like:
        drive: Samarkand Soul / 2025 / Market Research
        """
        try:
            # Clean incoming command
            clean = command.replace("drive:", "").strip()

            # Split by "/"
            parts = [p.strip() for p in clean.split("/")]

            parent_id = None
            current_path = ""

            for part in parts:
                current_path += f"{part} / "

                folder_id = self.create_folder(part, parent_id)
                parent_id = folder_id

            return f"Drive Agent: Qovluq quruldu → {clean}"

        except Exception as e:
            return f"Drive Agent xətası: {str(e)}"
