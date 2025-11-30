# app/main.py  (əgər adı başqa idisə – FastAPI start faylın hansıdırsa, onu əvəz et)

from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest
from app.agents.core.msp import MSP
from app.llm.brat_gpt import brat_gpt_chat

from app.reports.daily_report_service import (
    build_daily_report,
    generate_daily_report_text,
    send_daily_report_via_telegram,
)
from app.reports.morning_plan_service import (
    build_morning_plan,
    generate_morning_plan_text,
    send_morning_plan_via_telegram,
)
from app.integrations.telegram_client import send_telegram_message

app = FastAPI(title="BRAT Backend")

# =========================
#  MSP CORE
# =========================
msp = MSP()


# =========================
#  ROOT CHECK
# =========================
@app.get("/")
def root():
    return {"status": "OK", "message": "BRAT backend running"}


# =========================
#  HEALTH CHECK (Monitor üçün)
# =========================
@app.get("/health")
def health():
    """
    Samarkand Monitor üçün sadə heartbeat endpoint.
    """
    return {
        "status": "alive",
        "service": "agent-mesh",
        "message": "Brat Agent Backend işləyir, agent şəbəkəsi aktivdir 🤖",
    }


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
#  DAILY REPORT ENDPOINTLƏRİ
# =========================

@app.get("/daily-report/preview")
def daily_report_preview():
    """
    DailyReport obyektini xam JSON kimi qaytarır.
    """
    try:
        report = build_daily_report()
        return {"status": "ok", "report": report}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


@app.get("/daily-report/text")
def daily_report_text():
    """
    Telegram-a göndərilən formatlanmış mətnin preview versiyası.
    """
    try:
        text = generate_daily_report_text()
        return {"status": "ok", "text": text}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


from fastapi import APIRouter  # lazımsız olsa da qalmağı problem deyil


@app.api_route("/daily-report/send", methods=["GET", "POST"])
def daily_report_send():
    """
    Daily report-u Telegram-a göndərir.
    - Render cron job POST ilə çağırır.
    - Sən brauzerdən GET ilə test edə bilərsən.
    """
    try:
        ok = send_daily_report_via_telegram()
        if ok:
            return {"status": "ok"}
        return {
            "status": "failed",
            "error": "send_daily_report_via_telegram() returned False. "
                     "DEFAULT_CHAT_ID env dəyərini və Telegram bot konfiqurasiyasını yoxla.",
        }
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


# =========================
#  MORNING PLAN ENDPOINTLƏRİ
# =========================

@app.get("/morning-plan/preview")
def morning_plan_preview():
    """
    Morning plan-ın structured JSON preview-i.
    """
    try:
        plan = build_morning_plan()
        return {"status": "ok", "plan": plan}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


@app.get("/morning-plan/text")
def morning_plan_text():
    """
    Morning plan-ın Telegram mətni (preview).
    """
    try:
        text = generate_morning_plan_text()
        return {"status": "ok", "text": text}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


@app.api_route("/morning-plan/send", methods=["GET", "POST"])
def morning_plan_send():
    """
    Morning plan-ı Telegram-a göndərir.
    - Cron job POST ilə çağıracaq.
    - Brauzerdən GET ilə test etmək də olar.
    """
    try:
        ok = send_morning_plan_via_telegram()
        if ok:
            return {"status": "ok"}
        return {
            "status": "failed",
            "error": "send_morning_plan_via_telegram() returned False. "
                     "DEFAULT_CHAT_ID env dəyərini və Telegram bot konfiqurasiyasını yoxla.",
        }
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


# =========================
#  TELEGRAM MASTER AGENT
# =========================


def handle_telegram_command(chat_id: int, text: str):
    """
    Telegram komanda router-i.
    """
    lower = text.strip().lower()

    # 1) /start komandası
    if lower.startswith("/start") or lower.startswith("start"):
        msg = (
            "Salam, mən BRAT Core agentiyəm. Hal-hazırda bu komandaları bacarıram:\n\n"
            "*MSP test:*\n"
            "`msp: hər hansı komanda`\n\n"
            "*Market araşdırması (DS-01):*\n"
            "`market: Niche | Country`\n\n"
            "Məsələn:\n"
            "`market: pet hair remover | US`\n\n"
            "*Brat GPT dialoq:*\n"
            "Adi sualını yaz, mən sənin GPT Brat ekizin kimi cavab verim. 🧠"
        )
        send_telegram_message(chat_id, msg)
        return

    # 2) MSP komandası (msp: ... )
    if lower.startswith("msp:"):
        try:
            msp_command = text.split(":", 1)[1].strip()
        except Exception:  # noqa: BLE001
            msp_command = ""

        if not msp_command:
            send_telegram_message(
                chat_id,
                "MSP komandası boşdur. Format nümunəsi:\n"
                "`msp: bugünkü tapşırıqlarım nədir?`",
            )
            return

        try:
            response = msp.process(msp_command)
        except Exception as e:  # noqa: BLE001
            response = f"MSP error: {e}"

        send_telegram_message(chat_id, f"*MSP cavabı:*\n{response}")
        return

    # 3) DS-01 Market Research komandası
    if lower.startswith("market:"):
        try:
            after_keyword = text.split(":", 1)[1].strip()
            parts = [p.strip() for p in after_keyword.split("|")]

            niche = parts[0] if len(parts) >= 1 else ""
            country = parts[1] if len(parts) >= 2 else "US"

            if not niche:
                send_telegram_message(
                    chat_id,
                    "Niche boşdur. Format belə olmalıdır:\n"
                    "`market: pet hair remover | US`",
                )
                return

            req = MarketResearchRequest(niche=niche, country=country)
            result = analyze_market(req)

            if isinstance(result, dict) and "error" in result:
                send_telegram_message(
                    chat_id,
                    f"DS-01 error:\n`{result}`",
                )
                return

            send_telegram_message(
                chat_id,
                f"*DS-01 Market Research nəticəsi:*\n\n{result}",
            )
        except Exception as e:  # noqa: BLE001
            send_telegram_message(
                chat_id,
                "Komandanı oxuya bilmədim. Düzgün format nümunəsi:\n"
                "`market: pet hair remover | US`\n\n"
                f"Xəta: `{e}`",
            )
        return

    # 4) Brat GPT dialoq rejimi — qalan bütün mesajlar üçün
    try:
        reply = brat_gpt_chat(text)
        send_telegram_message(chat_id, reply)
        return
    except Exception as e:  # noqa: BLE001
        send_telegram_message(chat_id, f"BratGPT error: {e}")
        return


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
    except Exception as e:  # noqa: BLE001
        print("Telegram webhook error:", e)

    return {"ok": True}
