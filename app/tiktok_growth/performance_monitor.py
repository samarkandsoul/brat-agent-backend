"""
Performance Monitor

Məqsəd:
- TikTok kampaniyalarının performans metriklərini oxuyub
  sadə siqnal / alert çıxarmaq.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceSnapshot:
  spend: float
  revenue: float
  impressions: int
  clicks: int
  conversions: int

  @property
  def roas(self) -> float:
    return self.revenue / self.spend if self.spend > 0 else 0.0


@dataclass
class PerformanceAlert:
  level: str  # "info" | "warning" | "critical"
  message: str


class PerformanceMonitor:
  """Sadə performans analiz skeletonu."""

  def analyse(self, snapshot: PerformanceSnapshot) -> List[PerformanceAlert]:
    alerts: List[PerformanceAlert] = []

    logger.info("Analysing performance snapshot: %s", snapshot)

    if snapshot.roas < 1:
      alerts.append(
        PerformanceAlert(
          level="critical",
          message="ROAS < 1 – kampaniya pulları yandırır.",
        )
      )
    elif snapshot.roas < 2:
      alerts.append(
        PerformanceAlert(
          level="warning",
          message="ROAS zəifdir, creative və targeting yoxlanmalıdır.",
        )
      )

    return alerts
