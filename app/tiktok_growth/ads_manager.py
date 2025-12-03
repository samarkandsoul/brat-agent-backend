"""
Ads Manager

Məqsəd:
- TikTok Ads hesabında kampaniya / adset / ad idarəçiliyi üçün
  yüksək səviyyəli abstraksiya (skelet).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdCreateResult:
  success: bool
  external_id: str | None = None
  raw_response: Dict[str, Any] | None = None


class AdsManager:
  """TikTok reklam əməliyyatları üçün skeleton manager."""

  def create_ad(self, payload: Dict[str, Any]) -> AdCreateResult:
    """
    TODO:
    - TikTok Ads API client inteqrasiyası.
    """
    logger.info("Pretend-creating TikTok ad with payload: %s", payload)

    return AdCreateResult(
      success=True,
      external_id="ad_fake_id_123",
      raw_response={"status": "stubbed"},
    )

  def pause_ad(self, ad_id: str) -> bool:
    logger.info("Pretend-pausing ad_id=%s", ad_id)
    return True

  def resume_ad(self, ad_id: str) -> bool:
    logger.info("Pretend-resuming ad_id=%s", ad_id)
    return True
