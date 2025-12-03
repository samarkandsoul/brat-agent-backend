"""
Offer → Video Mapper

Məqsəd:
- Offer strukturunu (price, bonus, urgency və s.) video konseptlərinə map etmək.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class VideoConcept:
  title: str
  angle: str
  notes: str = ""


class OfferToVideoMapper:
  """Offer-dən video konseptləri çıxaran skeleton servis."""

  def map_offer(self, offer: Dict[str, Any]) -> List[VideoConcept]:
    """
    TODO:
    - Guarantee, scarcity, social proof parametrlərindən çıxış edib
      fərqli video strukturları generasiya etmək.
    """
    logger.info("Mapping offer to video concepts: %s", offer)

    price = offer.get("price")
    guarantee = offer.get("guarantee", "30 gün geri qaytarma")
    bonus = offer.get("bonus")

    concepts: List[VideoConcept] = [
      VideoConcept(
        title="Problem → Həll → Sosial sübut",
        angle="testimonial",
        notes="Müştəri rəyləri və həqiqi istifadə kadrları.",
      ),
      VideoConcept(
        title="Risk-free təklif",
        angle="guarantee",
        notes=f"Guarantee vurğulanır: {guarantee}",
      ),
    ]

    if bonus:
      concepts.append(
        VideoConcept(
          title="Bonus fokuslu video",
          angle="bonus",
          notes=f"Bonus: {bonus}, qiymət: {price}",
        )
      )

    return concepts
