"""
Instagram post scheduler skeleton.

Məqsəd:
- Planlaşdırılmış postların daxili təsviri
- Real cron / task runner sonradan əlavə olunacaq
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from .ig_api_client import InstagramApiClient


@dataclass
class ScheduledPost:
    image_url: str
    caption: str
    publish_at: datetime


class InstagramPostScheduler:
    def __init__(self, api_client: InstagramApiClient):
        self.api_client = api_client
        self._queue: List[ScheduledPost] = []

    def schedule_post(self, post: ScheduledPost) -> None:
        self._queue.append(post)

    def list_scheduled_posts(self) -> List[ScheduledPost]:
        return list(self._queue)

    def run_due_posts(self, now: datetime) -> int:
        """
        Sadə in-memory scheduler:
        - `now`-dan əvvəl olan postları paylaşır
        """
        due = [p for p in self._queue if p.publish_at <= now]
        remaining = [p for p in self._queue if p.publish_at > now]

        for post in due:
            self.api_client.publish_post(
                image_url=post.image_url,
                caption=post.caption,
            )

        self._queue = remaining
        return len(due)
