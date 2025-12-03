"""
Campaign Builder

Məqsəd:
- Kampaniya səviyyəsində obyekt yaratmaq üçün skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class CampaignConfig:
  name: str
  objective: str = "CONVERSIONS"
  buying_type: str = "AUCTION"


class CampaignBuilder:
  """TikTok kampaniyası üçün skeleton builder."""

  def build_campaign(self, brief: Dict[str, Any]) -> CampaignConfig:
    """
    TODO:
    - Funnel mərhələsinə görə objective seçimi (TOF/MOF/BOF).
    """
    name = brief.get("campaign_name", "Auto Campaign")
    objective = brief.get("objective", "CONVERSIONS")

    logger.info("Building campaign config name=%s objective=%s", name, objective)

    return CampaignConfig(name=name, objective=objective)
