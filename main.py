# app/main.py

from typing import Any, Dict

from fastapi import FastAPI

from app.agents.ds.ds01_market_research import (
    analyze_market,
    MarketResearchRequest,
)
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
from app.integrations.telegram_client import handle_telegram_update

# ======================================
# INTEL ROUTER IMPORT (DÜZGÜN PATH)
# ======================================
from app.integrations.intel.web_core import router as intel_router

app = FastAPI(title="BRAT Backend")


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
            "error": (
                "send_daily_report_via_telegram() returned False. "
                "DEFAULT_CHAT_ID env dəyərini və Telegram bot konfiqurasiyasını yoxla."
            ),
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
            "error": (
                "send_morning_plan_via_telegram() returned False. "
                "DEFAULT_CHAT_ID env dəyərini və Telegram bot konfiqurasiyasını yoxla."
            ),
        }
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "error": str(e)}


# =========================
#  TELEGRAM WEBHOOK (BRAT DIALOQ BEYNİ)
# =========================
@app.post("/tg/webhook")
def telegram_webhook(update: Dict[str, Any]):
    """
    Telegram webhook endpoint.

    Telegram bu endpoint-ə JSON `update` göndərir.
    Biz də update-i birbaşa `handle_telegram_update`-ə ötürürük.
    Orada:
      - chat_id + text çıxarılır
      - TelegramBratBrain.process(...) çağırılır
      - cavab geri həmin user-ə göndərilir
    """
    try:
        reply_text = handle_telegram_update(update)
        return {"ok": True, "reply": reply_text}
    except Exception as e:  # noqa: BLE001
        print("Telegram webhook error:", e)
        return {"ok": False, "error": str(e)}


# ======================================
# INTEL ROUTER REGISTRATION (YENİ)
# ======================================
app.include_router(intel_router)
