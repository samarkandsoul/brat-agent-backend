import os
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # your personal chat or group id


class TelegramNotConfigured(Exception):
    """Raised when Telegram env variables are missing."""
    pass


def _ensure_configured() -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise TelegramNotConfigured(
            "Telegram is not configured. "
            "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment."
        )


def send_telegram_message(text: str, parse_mode: Optional[str] = "Markdown") -> bool:
    """
    Send a plain text message to Telegram.

    Returns True if message was successfully sent, False otherwise.
    """
    _ensure_configured()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.error(
                "Telegram sendMessage failed: %s - %s",
                resp.status_code,
                resp.text[:500],
            )
            return False
        return True
    except Exception as exc:  # noqa: BLE001
        logger.exception("Telegram sendMessage exception: %s", exc)
        return False
