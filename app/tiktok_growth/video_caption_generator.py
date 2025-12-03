"""
Video Caption Generator

Məqsəd:
- Video üçün caption skeleton-u generasiya etmək.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class CaptionResult:
  text: str


class VideoCaptionGenerator:
  """Caption generasiyası üçün skeleton servis."""

  def generate(self, context: Dict[str, Any]) -> CaptionResult:
    """
    TODO:
    - Hook + benefit + CTA strukturunda fərqli caption variantları.
    """
    product = context.get("product_name", "məhsul")
    benefit = context.get("main_benefit", "daha rahat həyat")

    logger.info("Generating caption for product=%s", product)

    caption = f"{product} ilə {benefit} ✨\nDaha çox info üçün profili yoxla 👆"
    return CaptionResult(text=caption)
