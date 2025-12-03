"""
Instagram API client skeleton.

Məqsəd:
- Instagram Graph API ilə bütün request-lərin tək mərkəzdən çıxması
- Qalan modulalar (reel, scheduler, dm və s.) bu client-dən istifadə edəcək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class InstagramCredentials:
    access_token: str
    account_id: str


class InstagramApiClient:
    """
    Yalnız low-level HTTP/Graph çağırışlarını saxlayan layer.
    Buradan kənarda birbaşa Instagram API çağırışı edilməməlidir.
    """

    def __init__(self, creds: InstagramCredentials):
        self.creds = creds

    def publish_reel(self, video_url: str, caption: str) -> Dict[str, Any]:
        """
        Real implementasiya: Instagram Graph API /media və /media_publish endpoint-ləri.
        Hal-hazırda sadəcə skeleton-dur.
        """
        # TODO: implement real HTTP call
        return {
            "status": "stub",
            "video_url": video_url,
            "caption": caption,
        }

    def publish_post(self, image_url: str, caption: str) -> Dict[str, Any]:
        """
        Sadə image post üçün placeholder.
        """
        # TODO: implement real HTTP call
        return {
            "status": "stub",
            "image_url": image_url,
            "caption": caption,
        }

    def send_dm(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        DM göndərmək üçün skeleton.
        """
        # TODO: implement real HTTP call
        return {
            "status": "stub",
            "user_id": user_id,
            "message": message,
        }

    def raw_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Aşağı səviyyə "escape hatch". Qalan modulalar üçün lazım ola bilər.
        """
        # TODO: implement real HTTP call
        return {
            "status": "stub",
            "endpoint": endpoint,
            "params": params or {},
      }
