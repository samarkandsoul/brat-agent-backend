"""
Sound Trend Scanner

Məqsəd:
- TikTok sound trend-lərini izləmək üçün skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class TrendingSound:
  name: str
  estimated_uses: int
  trend_score: float
  last_checked_at: datetime


class SoundTrendScanner:
  """Trend səs məlumatları üçün placeholder scanner."""

  def fetch_trending_sounds(self, niche: str | None = None) -> List[TrendingSound]:
    """
    TODO:
    - TikTok API / scraping agent ilə real trend data toplamaq.
    """
    logger.info("Fetching trending sounds for niche=%s", niche)

    now = datetime.utcnow()
    return [
      TrendingSound(
        name="Generic Trend Sound",
        estimated_uses=100000,
        trend_score=0.8,
        last_checked_at=now,
      )
                            ]
