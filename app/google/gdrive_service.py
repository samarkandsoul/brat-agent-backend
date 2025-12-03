"""
Google Drive service skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GDriveCredentials:
    access_token: str


@dataclass
class DriveFile:
    id: str
    name: str
    mime_type: str
    folder_id: str | None = None


class GDriveService:
    def __init__(self, creds: GDriveCredentials):
        self.creds = creds

    def upload_file(self, folder_id: str, name: str, content: bytes, mime_type: str) -> Dict[str, Any]:
        # TODO: real Drive API call
        return {
            "status": "stub",
            "folder_id": folder_id,
            "name": name,
            "size": len(content),
            "mime_type": mime_type,
        }

    def list_files(self, folder_id: str) -> List[DriveFile]:
        # Stub – boş siyahı
        return []

    def create_folder(self, parent_id: str | None, name: str) -> Dict[str, Any]:
        return {
            "status": "stub",
            "parent_id": parent_id,
            "name": name,
            "id": "stub-folder-id",
      }
