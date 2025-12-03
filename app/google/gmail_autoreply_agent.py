"""
Gmail auto-reply agent skeleton.

Məqsəd:
- Müştəri emaillərini intent-ə görə qruplaşdırmaq
- Sadə auto-cavablar yaratmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .gmail_service import GmailService, GmailMessage


@dataclass
class AutoReplyConfig:
    support_email: str
    brand_name: str = "Samarkand Soul"


class GmailAutoReplyAgent:
    def __init__(self, gmail: GmailService, config: AutoReplyConfig):
        self.gmail = gmail
        self.config = config

    def classify_intent(self, msg: GmailMessage) -> str:
        text = (msg.subject + " " + msg.snippet).lower()
        if "refund" in text or "geri qaytar" in text:
            return "refund"
        if "çatdırılma" in text or "kuryer" in text or "shipping" in text:
            return "shipping"
        if "topdan" in text or "wholesale" in text:
            return "wholesale"
        return "general"

    def build_reply_body(self, msg: GmailMessage) -> str:
        intent = self.classify_intent(msg)
        if intent == "refund":
            return (
                "Salam 🌿\n\n"
                "Geri qaytarma ilə bağlı sorğunuzu aldıq. Sifariş nömrəsini cavabda yazın, "
                "detalları yoxlayaq.\n\nHörmətlə,\n"
                f"{self.config.brand_name} dəstəyi"
            )
        if intent == "shipping":
            return (
                "Salam 🌿\n\n"
                "Çatdırılma şərtlərimiz bölgəyə görə dəyişir. Ünvanınızı göndərin, "
                "dəqiq məlumat paylaşaq.\n\nHörmətlə,\n"
                f"{self.config.brand_name} dəstəyi"
            )
        if intent == "wholesale":
            return (
                "Salam 🌿\n\n"
                "Topdan satışla maraqlandığınıza görə təşəkkürlər. Gözlənilən aylıq "
                "miqdarı və ölkəni yazın, komanda sizi əlaqələndirsin.\n\nHörmətlə,\n"
                f"{self.config.brand_name} komandasına"
            )
        return (
            "Salam 🌿\n\n"
            "Mesajınız üçün təşəkkür edirik. Sorğunuzu komanda alıb, ən qısa zamanda cavablayacaq.\n\n"
            f"Hörmətlə,\n{self.config.brand_name}"
        )

    def auto_reply(self, msg: GmailMessage) -> Dict[str, str]:
        body = self.build_reply_body(msg)
        send_result = self.gmail.send_email(
            to=msg.sender,
            subject=f"Re: {msg.subject}",
            body=body,
        )
        return {
            "intent": self.classify_intent(msg),
            "api_status": send_result.get("status", "unknown"),
      }
