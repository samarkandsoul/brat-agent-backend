"""
YouTube video poster skeleton.

Məqsəd:
- Video upload + title/description/keywords strukturunu hazırlamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class YouTubeVideoMeta:
    title: str
    description: str
    tags: List[str]
    privacy_status: str = "unlisted"


class YouTubeVideoPoster:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def upload_video(self, file_path: str, meta: YouTubeVideoMeta) -> Dict[str, Any]:
        # TODO: real YouTube Data API call
        return {
            "status": "stub",
            "file_path": file_path,
            "title": meta.title,
            "privacy_status": meta.privacy_status,
                     }
