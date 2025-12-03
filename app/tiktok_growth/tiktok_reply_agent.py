"""
TikTok Reply Agent

Məqsəd:
- Şərhlərə / DM-lərə auto-cavab üçün skeleton.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class ReplyDecision:
  should_reply: bool
  reply_text: str | None = None


class TikTokReplyAgent:
  """Auto-reply üçün sadə qərar mexanizmi."""

  def decide_reply(self, message: Dict[str, Any]) -> ReplyDecision:
    """
    TODO:
    - LLM + sentiment analizi ilə real cavab sistemi.
    """
    text = (message.get("text") or "").lower()
    logger.info("Deciding reply for incoming message: %s", text)

    if "qiymət" in text or "neçə" in text:
      return ReplyDecision(should_reply=True, reply_text="Qiymət və detalları linkdə görərsən ❤️")
    if "salam" in text:
      return ReplyDecision(should_reply=True, reply_text="Salam! Nə kömək edə bilərəm?")

    return ReplyDecision(should_reply=False)
