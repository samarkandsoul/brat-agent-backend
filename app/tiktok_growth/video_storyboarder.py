"""
Video Storyboarder

Məqsəd:
- CreativeBrain-dən gələn ideyanı kadr-kadr (shot-by-shot) storyboard-a çevirmək.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class StoryboardShot:
  """Bir kadr üçün təsvir."""
  order: int
  description: str
  on_screen_text: str = ""
  duration_seconds: float = 2.0


@dataclass
class Storyboard:
  """Tam video storyboard strukturu."""
  idea_id: str
  shots: List[StoryboardShot] = field(default_factory=list)


class VideoStoryboarder:
  """Storyboard generasiya edən əsas servis."""

  def build_storyboard(self, idea: Dict[str, Any]) -> Storyboard:
    """
    Verilən ideyadan sadə default storyboard yaradır.

    TODO:
    - Hook / angle / offer strukturlarını istifadə edib daha ağıllı
      shot ardıcıllığı generasiya etmək.
    """
    idea_id = idea.get("id", "idea_1")
    hook = idea.get("hook", "Hook mətni yoxdur")
    angle = idea.get("angle", "generic")

    logger.info("Building storyboard for idea_id=%s angle=%s", idea_id, angle)

    shots = [
      StoryboardShot(
        order=1,
        description="Fast close-up, problem göstərilir.",
        on_screen_text=hook,
      ),
      StoryboardShot(
        order=2,
        description="Məhsul göstərilir, istifadə prosesi.",
        on_screen_text="Niyə bu həll daha yaxşıdır?",
      ),
      StoryboardShot(
        order=3,
        description="Before/after müqayisə.",
        on_screen_text="Fərqi hiss edirsən?",
      ),
      StoryboardShot(
        order=4,
        description="CTA ekranı, qiymət və təklif.",
        on_screen_text="Link bio-da, stok məhduddur ⚡",
      ),
    ]

    return Storyboard(idea_id=idea_id, shots=shots)


def create_storyboard(idea: Dict[str, Any]) -> Storyboard:
  return VideoStoryboarder().build_storyboard(idea)
