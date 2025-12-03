"""
Profile Optimizer

Məqsəd:
- TikTok profil bio, link və vizual strukturunu optimallaşdırmaq üçün skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProfileSuggestion:
  bio: str
  link: str | None = None
  notes: str = ""


class ProfileOptimizer:
  """Profil optimizasiyası üçün sadə agent."""

  def suggest_profile(self, context: Dict[str, Any]) -> ProfileSuggestion:
    """
    TODO:
    - Funnel mərhələsinə görə fərqli bio variantları.
    """
    brand = context.get("brand_name", "Brend")
    main_benefit = context.get("main_benefit", "premium həll")

    logger.info("Suggesting profile for brand=%s", brand)

    bio = f"{brand} · {main_benefit}\nSifariş və suallar üçün link 👇"
    link = context.get("primary_link")

    return ProfileSuggestion(bio=bio, link=link)
