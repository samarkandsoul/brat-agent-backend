"""
Pixel Event Debugger

Məqsəd:
- TikTok pixel event-ləri üçün sadə yoxlama / logging skeleton-u.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class PixelEvent:
  name: str
  payload: Dict[str, Any]


@dataclass
class PixelIssue:
  level: str  # "info" | "warning" | "error"
  message: str


class PixelEventDebugger:
  """Pixel event-ləri üçün sadə validator."""

  def validate(self, event: PixelEvent) -> List[PixelIssue]:
    issues: List[PixelIssue] = []

    logger.info("Validating pixel event: %s", event)

    if "event_id" not in event.payload:
      issues.append(PixelIssue(level="warning", message="event_id çatışmır."))

    if event.name == "Purchase" and "value" not in event.payload:
      issues.append(PixelIssue(level="error", message="Purchase event-də value yoxdur."))

    return issues
