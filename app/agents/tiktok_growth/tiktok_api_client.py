# app/agents/tiktok_growth/tiktok_api_client.py

"""
TikTokApiClient

Lightweight wrapper around TikTok Business / Creator APIs.

Right now this is a pure stub: it does NOT talk to real TikTok servers yet.
We only define the interface and log calls to the console, so that:

  - The rest of the system can import and use this client safely
  - Later we can plug in real HTTP calls without changing other modules
"""

from __future__ import annotations

import os
from typing import Dict, Any, List, Optional


class TikTokApiClient:
    """
    Simple TikTok API client stub.

    In the future this client will:
      - Upload videos
      - Fetch comments
      - Reply to comments
      - Fetch basic insights (views, likes, etc.)

    For now, all methods just print what they *would* do and
    return dummy data structures.
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
    ) -> None:
        # In the future we will use these values to sign real API requests.
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN", "")
        self.app_id = app_id or os.getenv("TIKTOK_APP_ID", "")
        self.app_secret = app_secret or os.getenv("TIKTOK_APP_SECRET", "")

        print(
            "[TikTokApiClient] Initialized (stub). "
            "No real network calls will be made yet."
        )

    # ==================================================================
    # VIDEO UPLOAD
    # ==================================================================

    def upload_video(self, video_path: str, caption: str) -> Dict[str, Any]:
        """
        Upload a video with a caption.

        STUB BEHAVIOUR:
          - Just logs the call
          - Returns a fake 'video_id'
        """
        print(
            f"[TikTokApiClient] (stub) upload_video called "
            f"video_path='{video_path}', caption='{caption}'"
        )

        # In real implementation we would send an HTTP POST here.
        fake_video_id = "stub_video_id_12345"

        return {
            "ok": True,
            "video_id": fake_video_id,
            "note": "This is a stub response. No real upload happened.",
        }

    # ==================================================================
    # COMMENTS
    # ==================================================================

    def get_comments(self, video_id: str) -> List[Dict[str, Any]]:
        """
        Fetch comments for a given video.

        STUB BEHAVIOUR:
          - Returns a small list of fake comments
        """
        print(f"[TikTokApiClient] (stub) get_comments called for video_id={video_id}")

        return [
            {
                "comment_id": "cmt_1",
                "user": "fake_user_1",
                "text": "This table textile looks so cozy! 💕",
            },
            {
                "comment_id": "cmt_2",
                "user": "fake_user_2",
                "text": "Where can I buy this tablecloth?",
            },
        ]

    def reply_to_comment(
        self, video_id: str, comment_id: str, text: str
    ) -> Dict[str, Any]:
        """
        Reply to a specific comment.

        STUB BEHAVIOUR:
          - Only logs what would be sent
        """
        print(
            f"[TikTokApiClient] (stub) reply_to_comment called "
            f"video_id={video_id}, comment_id={comment_id}, text='{text}'"
        )

        return {
            "ok": True,
            "note": "Stub reply sent. No real comment was posted.",
        }

    # ==================================================================
    # INSIGHTS / ANALYTICS
    # ==================================================================

    def get_basic_insights(self, video_id: str) -> Dict[str, Any]:
        """
        Fetch simple analytics for a video.

        STUB BEHAVIOUR:
          - Returns dummy numbers so that higher-level logic can be tested.
        """
        print(
            f"[TikTokApiClient] (stub) get_basic_insights called for video_id={video_id}"
        )

        return {
            "video_id": video_id,
            "views": 1234,
            "likes": 210,
            "comments": 17,
            "shares": 9,
            "note": "These are stub analytics numbers.",
      }
