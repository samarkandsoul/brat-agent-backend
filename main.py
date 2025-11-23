from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest

app = FastAPI(title="BRAT Backend")

# =========================
#  ROOT CHECK
# =========================
@app.get("/")
def root():
    return {"status": "OK", "message": "BRAT backend running"}

# =========================
#  DS-01 MARKET ANALYZE
# =========================
@app.post("/market/analyze")
def market_analyze(req: MarketResearchRequest):
    """
    DS-01 backend endpoint.
    """
    result = analyze_market(req)
    return {"status": "success", "data": result}

# =========================
#  TELEGRAM MASTER AGENT
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id: int, text: str):
    """
    Cavabı Telegram-a göndərir.
    """
    if not TELEGRAM_BOT_TOKEN:
        # Token qoyulmayıbsa, heç olmasa log yazsın
        print("TELEGRAM_BOT_TOKEN is not set")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Telegram çox uzun mesajları kəsməsin deyə disable_web_page_preview və s. qoya bilərik
    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        },
        timeout=15,
    )


def handle_telegram_command(chat_id: int, text: str):
    """
    Burada "əsas agent" loqikasıdır.
    Hal-hazırda yalnız 1 komanda dəstəkləyirik:

    market: niche | country

    Məs:
    market: pet hair remover | US
    """
    lower = text.strip().lower()

    if lower.startswith("start") or lower.startswith("/start"):
        msg = (
            "Salam, mən BRAT Core agentiyəm. Hal-hazırda bu komandaları bacarıram:\n\n"
            "*Market araşdırması:*\n"
            "`market: Niche | Country`\n\n"
            "Məsələn:\n"
            "`market: pet hair remover | US`"
        )
        send_telegram_message(chat_id, msg)
        return

    if lower.startswith("market:"):
        # "market: pet hair remover | US" formatını parse edək
        try:
            after_keyword = text.split(":", 1)[1].strip()
            parts = [p.strip() for p in after_keyword.split("|")]

            niche = parts[0] if len(parts) >= 1 else ""
            country = parts[1] if len(parts) >= 2 else "US"

            if not niche:
                send_telegram_message(
                    chat_id,
                    "Niche boşdur. Format belə olmalıdır:\n`market: pet hair remover | US`",
                )
                return

            # DS-01 backend funksiyasını birbaşa çağırırıq
            req = MarketResearchRequest(niche=niche, country=country)
            result = analyze_market(req)

            # OpenAI kvota problemi varsa, onu da göstərsin
            if isinstance(result, dict) and "error" in result:
                send_telegram_message(
                    chat_id,
                    f"DS-01 error:\n`{result}`",
                )
                return

            send_telegram_message(
                chat_id,
                f"*DS-01 Market Research nəticəsi*:\n\n{result}",
            )
        except Exception as e:
            send_telegram_message(
                chat_id,
                f"Komandanı oxuya bilmədim. Düzgün format nümunəsi:\n"
                "`market: pet hair remover | US`\n\nXəta: `{e}`",
            )
        return

    # Default: tanımadığı komanda
    msg = (
        "Bu komandaları anlayıram:\n\n"
        "*Market araşdırması:*\n"
        "`market: Niche | Country`\n"
        "Məsələn:\n"
        "`market: gaming chairs | US`\n\n"
        "Başlamaq üçün sadəcə yaz:\n"
        "`market: pet hair remover | US`"
    )
    send_telegram_message(chat_id, msg)


class TelegramUpdate(BaseModel):
    update_id: int | None = None
    message: dict | None = None


@app.post("/tg/webhook")
def telegram_webhook(update: TelegramUpdate):
    """
    Telegram webhook endpoint.
    Bot mesajı buraya göndərəcək, biz də handle_telegram_command işə salacağıq.
    """
    try:
        message = update.message or {}
        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        text = message.get("text", "")

        if not chat_id or not text:
            return {"ok": True}

        handle_telegram_command(chat_id, text)
    except Exception as e:
        print("Telegram webhook error:", e)
    return {"ok": True}
