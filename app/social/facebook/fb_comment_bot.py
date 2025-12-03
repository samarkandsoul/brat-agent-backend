"""
Facebook comment bot skeleton.

Məqsəd:
- Reklam postlarının altındakı şərhlərə auto-reply
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class FBComment:
    comment_id: str
    user_name: str
    message: str


class FacebookCommentBot:
    def classify_intent(self, comment: FBComment) -> str:
        text = comment.message.lower()
        if "qiymət" in text or "neçəyə" in text:
            return "price"
        if "haradadı" in text or "ünvan" in text:
            return "location"
        if "var?" in text or "stok" in text:
            return "availability"
        return "other"

    def build_reply(self, comment: FBComment) -> str:
        intent = self.classify_intent(comment)
        if intent == "price":
            return "Qiymətlər modelə görə dəyişir – DM yaz, detallı izah edək ❤️"
        if intent == "location":
            return "Onlayn sifariş, kuryer çatdırılma mümkündür 🚚"
        if intent == "availability":
            return "Mövcud modellərin siyahısını DM-də paylaşa bilərik ✅"
        return "Şərhin üçün təşəkkürlər! Sualın varsa, DM-də yaz 😊"

    def reply_to_comment(self, comment: FBComment) -> Dict[str, str]:
        """
        Realda burada Meta API çağırışı olacaq.
        Hal-hazırda sadəcə cavabı qaytarır.
        """
        reply = self.build_reply(comment)
        return {
            "status": "stub",
            "reply": reply,
      }
