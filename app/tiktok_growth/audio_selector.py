"""
Audio Selector

Məqsəd:
- Videoya uyğun səs/mahnı tipini seçmək üçün skeleton layer.
- Real inteqrasiya: TikTok audio trend API / research agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class AudioSuggestion:
  title: str
  audio_id: str | None = None
  mood: str = "energetic"
  is_trending: bool = False


class AudioSelector:
  """Brief və kreativə əsasən audio suggestion qaytarır."""

  def suggest_audio(self, context: Dict[str, Any]) -> List[AudioSuggestion]:
    """
    TODO:
    - Niş, hədəf kütlə, ölkə və trend datalarına görə audio seçimi.
    """
    logger.info("Suggesting audio for context: %s", context)

    niche = context.get("niche", "general")

    return [
      AudioSuggestion(
        title=f"{niche} – generic upbeat track",
        mood="energetic",
        is_trending=False,
      )
    ]


def get_audio_suggestions(context: Dict[str, Any]) -> List[AudioSuggestion]:
  return AudioSelector().suggest_audio(context)
