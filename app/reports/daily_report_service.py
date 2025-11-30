# app/reports/daily_report_service.py

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import List
import os

from app.reports.daily_report_models import (
    DailyReport,
    SalesMetrics,
    AdsChannelMetrics,
    ContentProductionMetrics,
    LifeMetrics,
    SystemHealthMetrics,
)
from app.integrations.telegram_client import send_telegram_message


# Telegram üçün default chat id (Render Environment-də DEFAULT_CHAT_ID kimi saxlayırsan)
DEFAULT_CHAT_ID: int = int(os.getenv("DEFAULT_CHAT_ID", "0"))


def _build_sales_block() -> SalesMetrics:
    """
    Burada hələ real Shopify inteqrasiya yoxdur, ona görə DEMO rəqəmlər qaytarırıq.
    Sonra Shopify agenti ilə əvəz edəcəyik.
    """
    return SalesMetrics(
        total_revenue=0.0,
        currency="USD",
        orders_count=0,
        conversion_rate=0.0,
        avg_order_value=None,
        atc_rate=None,
        checkout_drop_rate=None,
    )


def _build_ads_block() -> List[AdsChannelMetrics]:
    """
    Reklam kanalları üçün DEMO məlumat.
    Gələcəkdə Meta/TikTok API-lərindən real rəqəmlər gələcək.
    """
    meta = AdsChannelMetrics(
        channel_name="Meta",
        spend=0.0,
        revenue=0.0,
        impressions=0,
        clicks=0,
        ctr=0.0,
        cpc=None,
        cpm=None,
        roas=None,
        best_creatives=[],
        notes="DEMO mode – no real ads data yet.",
    )

    tiktok = AdsChannelMetrics(
        channel_name="TikTok",
        spend=0.0,
        revenue=0.0,
        impressions=0,
        clicks=0,
        ctr=0.0,
        cpc=None,
        cpm=None,
        roas=None,
        best_creatives=[],
        notes="DEMO mode – no real ads data yet.",
    )

    return [meta, tiktok]


def _build_content_block() -> ContentProductionMetrics:
    return ContentProductionMetrics(
        tiktok_videos_created=0,
        scripts_written=0,
        image_variants_created=0,
        trends_detected=0,
        notes="Content agent hələ qoşulmayıb – DEMO.",
    )


def _build_life_block() -> LifeMetrics:
    return LifeMetrics(
        planned_focus_minutes=0,
        completed_focus_minutes=0,
        workout_planned=False,
        workout_completed=False,
        water_target_liters=0.0,
        water_completed_liters=0.0,
        sleep_hours_last_night=None,
        notes="LIFE01 agent DEMO rejimindədir.",
    )


def _build_system_health_block() -> SystemHealthMetrics:
    return SystemHealthMetrics(
        monitor_service_alive=True,
        agent_mesh_alive=True,
        http_status_code=200,
        incidents_last_24h=[],
    )


def build_daily_report() -> DailyReport:
    """
    Bütün blokları birləşdirib DailyReport obyektini yaradır.
    QƏDİM 'generated_at_utc' və s. field-lər YOXDUR – yalnız sənin dataclass-larındakı field-lər var.
    """
    today_iso = datetime.now(timezone.utc).date().isoformat()

    sales = _build_sales_block()
    ads_channels = _build_ads_block()
    content = _build_content_block()
    life = _build_life_block()
    system = _build_system_health_block()

    headline = "Samarkand Soul – Daily Report (DEMO mode)"
    key_warnings: List[str] = []

    return DailyReport(
        date_iso=today_iso,
        sales=sales,
        ads_channels=ads_channels,
        content=content,
        life=life,
        system_health=system,
        headline=headline,
        key_warnings=key_warnings,
    )


def generate_daily_report_text() -> str:
    """
    DailyReport obyektini insan oxuyan formatlı mətnə çevirir (Telegram üçün).
    """
    report = build_daily_report()

    lines: List[str] = []
    lines.append(f"📊 *Samarkand Soul Daily Report* — {report.date_iso}")

    if report.headline:
        lines.append(f"⭐ _{report.headline}_")

    lines.append("")

    # --- Sales ---
    if report.sales:
        s = report.sales
        lines.append("💰 *SALES*")
        lines.append(
            f"- Revenue: {s.total_revenue:.2f} {s.currency} "
            f"(orders: {s.orders_count}, CR: {s.conversion_rate:.1f}%)"
        )
        if s.avg_order_value is not None:
            lines.append(f"- AOV: {s.avg_order_value:.2f} {s.currency}")
        if s.atc_rate is not None:
            lines.append(f"- Add-to-cart rate: {s.atc_rate:.1f}%")
        if s.checkout_drop_rate is not None:
            lines.append(f"- Checkout drop: {s.checkout_drop_rate:.1f}%")
        lines.append("")

    # --- Ads ---
    if report.ads_channels:
        lines.append("📣 *ADS & TRAFFIC*")
        for ch in report.ads_channels:
            lines.append(f"- {ch.channel_name}: spend {ch.spend:.2f}, revenue {ch.revenue:.2f}")
            lines.append(
                f"  impressions {ch.impressions}, clicks {ch.clicks}, CTR {ch.ctr:.2f}%"
            )
            if ch.roas is not None:
                lines.append(f"  ROAS: {ch.roas:.2f}x")
            if ch.notes:
                lines.append(f"  _{ch.notes}_")
        lines.append("")

    # --- Content ---
    if report.content:
        c = report.content
        lines.append("🎥 *CONTENT*")
        lines.append(
            f"- TikTok videos: {c.tiktok_videos_created}, "
            f"scripts: {c.scripts_written}, "
            f"images: {c.image_variants_created}, "
            f"trends: {c.trends_detected}"
        )
        if c.notes:
            lines.append(f"  _{c.notes}_")
        lines.append("")

    # --- Life ---
    if report.life:
        l = report.life
        lines.append("🧠 *LIFE & ENERGY*")
        lines.append(
            f"- Focus: {l.completed_focus_minutes}/{l.planned_focus_minutes} dəq"
        )
        lines.append(
            f"- Workout: {'✅' if l.workout_completed else '❌'} "
            f"(plan: {'yes' if l.workout_planned else 'no'})"
        )
        lines.append(
            f"- Water: {l.water_completed_liters}/{l.water_target_liters} L"
        )
        if l.sleep_hours_last_night is not None:
            lines.append(f"- Sleep: {l.sleep_hours_last_night:.1f} saat")
        if l.notes:
            lines.append(f"  _{l.notes}_")
        lines.append("")

    # --- System ---
    if report.system_health:
        sys = report.system_health
        lines.append("🛰 *SYSTEM HEALTH*")
        lines.append(
            f"- Monitor service: {'✅ alive' if sys.monitor_service_alive else '❌ down'}"
        )
        lines.append(
            f"- Agent mesh: {'✅ alive' if sys.agent_mesh_alive else '❌ down'}"
        )
        lines.append(f"- HTTP status (monitor): {sys.http_status_code}")
        if sys.incidents_last_24h:
            lines.append("- Incidents last 24h:")
            for inc in sys.incidents_last_24h:
                lines.append(f"  • {inc}")
        else:
            lines.append("- Incidents last 24h: none ✅")
        lines.append("")

    if report.key_warnings:
        lines.append("⚠️ *WARNINGS*")
        for w in report.key_warnings:
            lines.append(f"- {w}")

    return "\n".join(lines)


def send_daily_report_via_telegram() -> bool:
    """
    Mətn hazırlayıb Telegram-a göndərir.
    Cron job məhz bu funksiyanı istifadə edir.
    """
    if not DEFAULT_CHAT_ID:
        print("DEFAULT_CHAT_ID environment variable is not set – skipping send.")
        return False

    text = generate_daily_report_text()

    try:
        send_telegram_message(DEFAULT_CHAT_ID, text)
        return True
    except Exception as e:  # noqa: BLE001
        print("Daily report Telegram send error:", e)
        return False
