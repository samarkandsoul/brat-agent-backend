"""
TikTok Creative Brain

Məqsəd:
- Məhsul / offer / brend məlumatından çıxış edərək
  kreativ ideyalar, hook-lar və kontent bucaqları (angles) generasiya etmək.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class CreativeIdea:
  """Bir TikTok videosu üçün əsas kreativ fikir modeli."""
  hook: str
  angle: str
  cta: str
  notes: str = ""


@dataclass
class CreativeBrainConfig:
  """CreativeBrain üçün baza konfiqurasiya."""
  max_ideas: int = 5
  language: str = "az"
  tone: str = "direct_response"  # və ya "educational", "storytelling"


class CreativeBrain:
  """TikTok Creative Brain əsas servisi."""

  def __init__(self, config: CreativeBrainConfig | None = None) -> None:
    self.config = config or CreativeBrainConfig()

  def generate_ideas(self, brief: Dict[str, Any]) -> List[CreativeIdea]:
    """
    Verilən brief əsasında skeleton ideyalar qaytarır.

    TODO:
    - Buraya LLM çağırışları inteqrasiya olunacaq.
    - Brand / offer / audience datasını istifadə edərək real ideyalar generasiya ediləcək.
    """
    logger.info("Generating TikTok creative ideas from brief: %s", brief)

    product_name = brief.get("product_name", "Məhsul")
    base_hook = f"{product_name} haqqında bilmədiyin 1 şey"
    base_angle = "problem-solution"

    ideas: List[CreativeIdea] = []

    for i in range(self.config.max_ideas):
      ideas.append(
        CreativeIdea(
          hook=f"{base_hook} #{i + 1}",
          angle=base_angle,
          cta="Link bio-da, indi yoxla ✅",
          notes="AUTO-GENERATED SKELETON IDEA – real logic TODO.",
        )
      )

    return ideas


def generate_creatives(brief: Dict[str, Any]) -> List[CreativeIdea]:
  """
  Convenience helper – birbaşa modul səviyyəsindən ideya generasiyası.
  """
  brain = CreativeBrain()
  return brain.generate_ideas(brief)
