# app/reports/morning_plan_service.py

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import List, Dict, Any

from app.integrations.telegram_client import send_telegram_message

# Eyni DAILY REPORT kimi – Render env-dən oxuyuruq
DEFAULT_CHAT_ID: int = int(os.getenv("DEFAULT_CHAT_ID", "0") or 0)


def build_morning_plan() -> Dict[str, Any]:
    """
    Sadə structured morning plan.
    Gələcəkdə bunu real tapşırıqlar, Google Calendar, Notion və s. ilə birləşdirə bilərik.
    İndi isə sabit skeleton verir.
    """
    now_utc = datetime.now(timezone.utc)
    date_iso = now_utc.date().isoformat()
    weekday = now_utc.strftime("%A")

    # Bunu gələcəkdə agentlər dolduracaq. İndi şablon kimi işləyir.
    sections: List[Dict[str, Any]] = [
        {
            "title": "Commander Focus",
            "items": [
                "Check Samarkand Soul Shopify store status & yesterday revenue.",
                "Review open tasks for today (marketing, product, operations).",
                "Choose 1 main WIN for today (non-negotiable).",
            ],
        },
        {
            "title": "Sales & Marketing",
            "items": [
                "Check running ads (Meta / TikTok) – basic spend & results.",
                "Decide 1 content piece to publish today (TikTok / Reels / Story).",
                "Plan 1 micro-experiment to improve conversion or CTR.",
            ],
        },
        {
            "title": "System & Agents",
            "items": [
                "Confirm Brat Agent Backend is alive (health endpoint).",
                "Note any issues from yesterday to feed into SYS agents later.",
            ],
        },
        {
            "title": "Life & Energy",
            "items": [
                "Set focus blocks (Deep work) for the day.",
                "Plan workout & minimum movement.",
                "Decide water & sleep targets (keep commander battery full).",
            ],
        },
    ]

    return {
        "date_iso": date_iso,
        "weekday": weekday,
        "headline": "Samarkand Soul — Morning Focus Plan",
        "sections": sections,
    }


def generate_morning_plan_text() -> str:
    """
    Morning plan-ı Telegram üçün formatlanmış mətinə çevirir.
    """
    plan = build_morning_plan()

    lines: List[str] = []
    lines.append(
        f"🧭 *Samarkand Soul Morning Plan* — {plan['date_iso']} ({plan['weekday']})"
    )
    if plan.get("headline"):
        lines.append(f"⭐ _{plan['headline']}_")
    lines.append("")

    for section in plan["sections"]:
        title = section.get("title", "Section")
        items = section.get("items", [])
        lines.append(f"• *{title}*")
        for i in items:
            lines.append(f"  - {i}")
        lines.append("")

    # Son motivasiya xətti
    lines.append("🚀 Commander mode: 1 böyük WIN seç və onu bugün mütləq bağla.")

    return "\n".join(lines)


def send_morning_plan_via_telegram() -> bool:
    """
    Morning plan mətni hazırlayıb Telegram-a göndərir.
    Cron job POST bu funksiyanı çağıracaq.
    """
    if not DEFAULT_CHAT_ID:
        print("DEFAULT_CHAT_ID env is not set – skipping morning plan send.")
        return False

    text = generate_morning_plan_text()

    try:
        send_telegram_message(DEFAULT_CHAT_ID, text)
        return True
    except Exception as e:  # noqa: BLE001
        print("Morning plan Telegram send error:", e)
        return False
