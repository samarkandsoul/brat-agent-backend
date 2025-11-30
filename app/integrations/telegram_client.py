import requests
from typing import Optional, Tuple

from app.config.settings import settings
from app.agents.core.telegram_brat_brain import TelegramBratBrain

TELEGRAM_API_BASE = "https://api.telegram.org"

# Single global brain instance for all Telegram messages
telegram_brat_brain = TelegramBratBrain()


def send_telegram_message(
    chat_id: int,
    text: str,
    parse_mode: str = "Markdown",
    disable_web_page_preview: bool = True,
) -> bool:
    """
    Generic Telegram sender.
    Used by:
      - main.py (webhook responses)
      - reports (daily report, morning plan, etc.)
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


# ============================================================================
#  Telegram BRAT Brain – unified dialog handler
# ============================================================================


def _extract_chat_and_text(update: dict) -> Tuple[Optional[int], Optional[str]]:
    """
    Safely extract chat_id and incoming text from a Telegram update.

    Supports:
      - standard messages
      - edited messages (fallback)
    Callback query-lər üçün ayrıca handler main.py tərəfdə istifadə oluna bilər.
    """
    if not update:
        return None, None

    message = update.get("message") or update.get("edited_message")
    if not message:
        return None, None

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text")

    if not isinstance(chat_id, int):
        chat_id = None

    if text is not None:
        text = str(text)

    return chat_id, text


def handle_telegram_update(update: dict) -> Optional[str]:
    """
    Main entrypoint for Telegram webhook.

    - Gələn update-dən chat_id və text çıxarır
    - Mətni TelegramBratBrain-ə ötürür
    - Cavabı həmin user-ə geri göndərir
    - Cavab mətnini (debug və ya log üçün) geri qaytarır

    main.py içində tipik istifadə:
        from app.integrations.telegram_client import handle_telegram_update

        @app.post("/telegram/webhook")
        async def telegram_webhook(request: Request):
            data = await request.json()
            reply_text = handle_telegram_update(data)
            return {"ok": True}
    """
    chat_id, incoming_text = _extract_chat_and_text(update)

    if not chat_id or not incoming_text:
        print("[telegram_client] Could not extract chat_id or text from update")
        return None

    try:
        # BRAT dialoq beyni – burada bütün
        # BRAT: / ZAHID BRAT: stil loqika işləyir
        reply_text = telegram_brat_brain.process(incoming_text)
    except Exception as e:  # noqa: BLE001
        print("[telegram_client] Brain processing error:", e)
        reply_text = (
            "ESCALATION\n"
            "Reason: Internal brain error while processing Telegram message.\n"
            "Action: Human validation required.\n"
        )

    # Cavabı user-ə göndər
    ok = send_telegram_message(chat_id, reply_text)
    if not ok:
        print("[telegram_client] Failed to send reply to chat:", chat_id)

    return reply_text
