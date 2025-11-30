import requests
from typing import Optional

from app.config.settings import settings

TELEGRAM_API_BASE = "https://api.telegram.org"


def send_telegram_message(
    chat_id: int,
    text: str,
    parse_mode: str = "Markdown",
    disable_web_page_preview: bool = True,
) -> bool:
    """
    Generic Telegram sender.
    Used by:
      - main.py (webhook cavabları)
      - reports (daily report)
    """
    token = settings.TELEGRAM_BOT_TOKEN

    if not token:
        print("[telegram_client] TELEGRAM_BOT_TOKEN is not set")
        return False

    if not chat_id:
        print("[telegram_client] chat_id is missing")
        return False

    url = f"{TELEGRAM_API_BASE}/bot{token}/sendMessage"

    try:
        resp = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": disable_web_page_preview,
            },
            timeout=15,
        )
        if resp.status_code != 200:
            print("[telegram_client] sendMessage failed:", resp.text)
            return False
        return True
    except Exception as e:  # noqa: BLE001
        print("[telegram_client] Telegram send error:", e)
        return False


def send_to_default_chat(text: str) -> bool:
    """
    Daily report və s. üçün DEFAULT_CHAT_ID istifadə edir.
    """
    chat_id: int = settings.DEFAULT_CHAT_ID
    if not chat_id:
        print("[telegram_client] DEFAULT_CHAT_ID is not configured")
        return False
    return send_telegram_message(chat_id, text)
