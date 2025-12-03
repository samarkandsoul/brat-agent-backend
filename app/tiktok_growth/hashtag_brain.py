"""
Hashtag Brain

Məqsəd:
- Video / niş / ölkə üzrə hashtag strategiyası qurmaq.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class HashtagPlan:
  primary: List[str]
  secondary: List[str]
  experimental: List[str]


class HashtagBrain:
  """Hashtag strategiyası üçün skeleton servis."""

  def build_plan(self, context: Dict[str, Any]) -> HashtagPlan:
    """
    TODO:
    - TikTok hashtag search + LLM ilə daha ağıllı planlama.
    """
    niche = context.get("niche", "gen")
    country = context.get("country", "az")

    logger.info("Building hashtag plan for niche=%s country=%s", niche, country)

    primary = [f"#{niche}", "#foryou", "#fyp"]
    secondary = [f"#{niche}tips", f"#{niche}trend"]
    experimental = [f"#{country}", "#testhashtag"]

    return HashtagPlan(primary=primary, secondary=secondary, experimental=experimental)


def generate_hashtags(context: Dict[str, Any]) -> HashtagPlan:
  return HashtagBrain().build_plan(context)
