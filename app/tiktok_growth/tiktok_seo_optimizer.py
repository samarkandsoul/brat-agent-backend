"""
TikTok SEO Optimizer

Məqsəd:
- TikTok search üçün keyword strategiyası və SEO optimizasiyası skeleton-u.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class SeoPlan:
  primary_keywords: List[str]
  secondary_keywords: List[str]
  description: str


class TikTokSeoOptimizer:
  """SEO üçün sadə plan generatoru."""

  def build_plan(self, context: Dict[str, Any]) -> SeoPlan:
    """
    TODO:
    - Real search data + LLM ilə keyword map.
    """
    niche = context.get("niche", "shopify-store")
    language = context.get("language", "az")

    logger.info("Building TikTok SEO plan for niche=%s language=%s", niche, language)

    primary = [f"{niche} necə etmək", f"{niche} tips"]
    secondary = [f"{niche} səhvlər", f"{niche} strategiya"]

    description = (
      "AUTO TikTok SEO skeleton – buraya daha detallı, keyword zəngin "
      "video description generasiyası gələcək."
    )

    return SeoPlan(
      primary_keywords=primary,
      secondary_keywords=secondary,
      description=description,
  )
