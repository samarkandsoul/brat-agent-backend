"""
Google Drive backup agent skeleton.

Məqsəd:
- Məsələn: Brat reportlarını, configləri və s. müəyyən intervalla Drive-a dump etmək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from .gdrive_service import GDriveService


@dataclass
class BackupItem:
    path: str          # sistemdəki lokasiya, məsələn: "reports/daily_2024-01-01.json"
    target_folder_id: str
    mime_type: str = "application/json"


class GDriveBackupAgent:
    def __init__(self, drive: GDriveService):
        self.drive = drive

    def load_file_content(self, path: str) -> bytes:
        """
        Real versiyada: serverdə faylı oxuyur.
        Skeleton-da sadəcə boş content.
        """
        return f"stub-content-for-{path}".encode("utf-8")

    def backup_items(self, items: List[BackupItem]) -> List[Dict[str, object]]:
        results: List[Dict[str, object]] = []
        for item in items:
            content = self.load_file_content(item.path)
            res = self.drive.upload_file(
                folder_id=item.target_folder_id,
                name=item.path.split("/")[-1],
                content=content,
                mime_type=item.mime_type,
            )
            results.append(res)
        return results
