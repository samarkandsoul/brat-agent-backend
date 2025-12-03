"""
Ad Script Lab

Məqsəd:
- Reklam videoları üçün script skeleton-ları generasiya etmək.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class ScriptLine:
  role: str  # "HOOK", "BODY", "CTA"
  text: str


@dataclass
class AdScript:
  lines: List[ScriptLine]


class AdScriptLab:
  """TikTok reklam script-ləri üçün skelet servis."""

  def generate_script(self, brief: Dict[str, Any]) -> AdScript:
    """
    TODO:
    - Offer, objection, proof elementlərinə görə copy strukturlaşdırmaq.
    """
    product = brief.get("product_name", "məhsul")
    main_benefit = brief.get("main_benefit", "sürətli nəticə")

    logger.info("Generating ad script for product=%s", product)

    lines = [
      ScriptLine(role="HOOK", text=f"{product} istifadə edənlər niyə geriyə qayıtmır?"),
      ScriptLine(
        role="BODY",
        text=f"Əvvəl {brief.get('problem', 'problem')} yaşayırdın, indi isə {main_benefit}.",
      ),
      ScriptLine(role="CTA", text="Sifariş üçün link bio-da – stok məhduddur!"),
    ]

    return AdScript(lines=lines)
