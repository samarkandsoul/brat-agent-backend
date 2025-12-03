"""
Adset Builder

Məqsəd:
- Targeting, placement, budget parametrlərini generasiya edən layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class AdsetConfig:
  name: str
  daily_budget: float
  optimization_event: str = "PURCHASE"
  country: str = "AZ"
  min_age: int = 18
  max_age: int = 55


class AdsetBuilder:
  """Adset parametrləri üçün skeleton builder."""

  def build_adset(self, brief: Dict[str, Any]) -> AdsetConfig:
    """
    TODO:
    - Lookalike / interest / custom audience logikasını əlavə etmək.
    """
    name = brief.get("campaign_name", "Auto Adset")
    budget = float(brief.get("daily_budget", 20.0))

    logger.info("Building adset for campaign=%s", name)

    return AdsetConfig(name=name, daily_budget=budget)
