"""
Instagram DM auto-reply agent skeleton.

Məqsəd:
- Sadə FAQ cavabları
- Sifariş sorğularını strukturlaşdırmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .ig_api_client import InstagramApiClient


@dataclass
class IncomingDM:
    user_id: str
    message: str


class InstagramDMAutoReplyAgent:
    def __init__(self, api_client: InstagramApiClient):
        self.api_client = api_client

    def classify_intent(self, dm: IncomingDM) -> str:
        """
        Mesajın intent-i: 'order', 'shipping', 'price', 'other' və s.
        """
        text = dm.message.lower()
        if "qiymət" in text or "neçəyə" in text:
            return "price"
        if "çatdırılma" in text or "kuryer" in text:
            return "shipping"
        if "sifariş" in text:
            return "order"
        return "other"

    def build_reply(self, dm: IncomingDM) -> str:
        intent = self.classify_intent(dm)
        if intent == "price":
            return "Qiymət üçün ölçü/model göndərin, detallı cavab verim ✨"
        if intent == "shipping":
            return "Çatdırılma Bakı daxili mümkündür, rayonlar üçün kuryer şərtlərini yazım? 🚚"
        if intent == "order":
            return "Sifariş üçün ad + nömrə + ünvan göndərin, komandamız sizinlə əlaqə saxlasın 📝"
        return "Mesaj üçün təşəkkürlər! Bir azdan ətraflı cavab yazacağıq 💌"

    def handle_incoming_dm(self, dm: IncomingDM) -> Dict[str, str]:
        reply = self.build_reply(dm)
        result = self.api_client.send_dm(user_id=dm.user_id, message=reply)
        return {
            "intent": self.classify_intent(dm),
            "reply": reply,
            "api_status": result.get("status", "unknown"),
      }
