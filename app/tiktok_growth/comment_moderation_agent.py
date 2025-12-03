"""
Comment Moderation Agent

Məqsəd:
- Zərərli / spam şərhləri flag-ləmək üçün skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModerationDecision:
  should_hide: bool
  reason: str | None = None


BANNED_KEYWORDS = ["scam", "fake", "dolandırıcı", "follow for follow"]


class CommentModerationAgent:
  """Şərh moderasiyası üçün sadə qayda bazası."""

  def moderate(self, comment: Dict[str, Any]) -> ModerationDecision:
    text = (comment.get("text") or "").lower()
    logger.info("Moderating comment: %s", text)

    for kw in BANNED_KEYWORDS:
      if kw in text:
        return ModerationDecision(
          should_hide=True,
          reason=f"Contains banned keyword '{kw}'",
        )

    return ModerationDecision(should_hide=False)
