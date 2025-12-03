"""
TikTok Post Scheduler

Məqsəd:
- Orqanik TikTok postları üçün sadə planlama layer-i.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import logging

logger = logging.getLogger(__name__)


@dataclass
class ScheduledPost:
  caption: str
  scheduled_at: datetime


class TikTokPostScheduler:
  """Post schedule skeleton servisi."""

  def build_schedule(
    self,
    base_caption: str,
    posts_per_day: int = 1,
    days: int = 7,
    start_time: datetime | None = None,
  ) -> List[ScheduledPost]:
    logger.info(
      "Building TikTok post schedule posts_per_day=%s days=%s",
      posts_per_day,
      days,
    )

    start = start_time or datetime.utcnow()
    schedule: List[ScheduledPost] = []

    for day in range(days):
      for i in range(posts_per_day):
        ts = start + timedelta(days=day, hours=i * 3)
        schedule.append(ScheduledPost(caption=base_caption, scheduled_at=ts))

    return schedule
