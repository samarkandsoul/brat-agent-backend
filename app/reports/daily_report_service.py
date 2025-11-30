# app/reports/daily_report_service.py

from __future__ import annotations

import os
from dataclasses import asdict
from datetime import datetime, timezone
from typing import List, Tuple

from app.reports.daily_report_models import (
    DailyReport,
    DailyReportItem,
    SalesMetrics,
    AdsChannelMetrics,
    ContentProductionMetrics,
    LifeMetrics,
    SystemHealthMetrics,
)
from app.integrations.telegram_client import send_telegram_message
from app.integrations.shopify_sales.sales_service import (
    get_shopify_sales_metrics_safely,
)

# Telegram üçün default chat id
DEFAULT_CHAT_ID: int = int(os.getenv("DEFAULT_CHAT_ID", "0") or 0)


# ==========================================================
#  BLOK QURAN FUNKSİYALAR
# ==========================================================

def _build_sales_block() -> Tuple[SalesMetrics, List[str]]:
    """
    Shopify satış məlumatlarını oxuyur.
    Əgər hər hansı problem olsa, DEMO rəqəmlər qaytarır və warning-lər verir.
    """
    sales_metrics, warnings = get_shopify_sales_metrics_safely()
    return sales_metrics, warnings


def _build_ads_block() -> List[AdsChannelMetrics]:
    """
    Reklam kanalları üçün hələ DEMO məlumat.
    Gələcəkdə Meta/TikTok API-lərindən real data gələcək.
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


# ==========================================================
#  ƏSAS REPORT BUILDER
# ==========================================================

def build_daily_report() -> DailyReport:
    """
    Bütün blokları birləşdirib DailyReport obyektini yaradır.
    Bu model artıq:
      - generated_at_utc
      - summary, stats, items
      - dərin bloklar (sales, ads, content, life, system_health)
      - headline + warnings
    sahələrini dəstəkləyir.
    """
    now_utc = datetime.now(timezone.utc)
    generated_at_utc = now_utc.isoformat()
    date_iso = now_utc.date().isoformat()

    # 1) Sales – Shopify üzərindən
    sales, sales_warnings = _build_sales_block()

    # 2) Ads (DEMO)
    ads_channels = _build_ads_block()

    # 3) Content (DEMO)
    content = _build_content_block()

    # 4) Life (DEMO)
    life = _build_life_block()

    # 5) System health
    system = _build_system_health_block()

    # Sadə headline və summary
    headline = "Samarkand Soul – Daily Report (DEMO + Shopify sales)"
    summary = "Core metrics for sales, ads, content, life & system health."

    # Sadə stats dict (gələcəkdə UI üçün)
    stats = {
        "total_revenue": sales.total_revenue,
        "orders_count": sales.orders_count,
        "ads_channels": len(ads_channels),
    }

    # Sadə item list (monitor UI və ya gələcək mobil view üçün)
    items: List[DailyReportItem] = [
        DailyReportItem(title="Total Revenue", value=f"{sales.total_revenue:.2f} {sales.currency}"),
        DailyReportItem(title="Orders", value=sales.orders_count),
        DailyReportItem(title="Conversion Rate", value=f"{sales.conversion_rate:.2f}%"),
    ]

    key_warnings: List[str] = []
    key_warnings.extend(sales_warnings)

    return DailyReport(
        generated_at_utc=generated_at_utc,
        date_iso=date_iso,
        summary=summary,
        stats=stats,
        items=items,
        sales=sales,
        ads_channels=ads_channels,
        content=content,
        life=life,
        system_health=system,
        headline=headline,
        key_warnings=key_warnings,
    )


# ==========================================================
#  FORMATLANMIŞ MƏTN (Telegram üçün)
# ==========================================================

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
            f"(orders: {s.orders_count}, CR: {s.conversion_rate:.2f}%)"
        )
        if s.avg_order_value is not None:
            lines.append(f"- AOV: {s.avg_order_value:.2f} {s.currency}")
        if s.atc_rate is not None:
            lines.append(f"- Add-to-cart rate: {s.atc_rate:.2f}%")
        if s.checkout_drop_rate is not None:
            lines.append(f"- Checkout drop: {s.checkout_drop_rate:.2f}%")
        lines.append("")

    # --- Ads ---
    if report.ads_channels:
        lines.append("📣 *ADS & TRAFFIC*")
        for ch in report.ads_channels:
            lines.append(
                f"- {ch.channel_name}: spend {ch.spend:.2f}, "
                f"revenue {ch.revenue:.2f}"
            )
            lines.append(
                f"  impressions {ch.impressions}, clicks {ch.clicks}, "
                f"CTR {ch.ctr:.2f}%"
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

    # --- Warnings ---
    if report.key_warnings:
        lines.append("⚠️ *WARNINGS*")
        for w in report.key_warnings:
            lines.append(f"- {w}")

    return "\n".join(lines)


# ==========================================================
#  TELEGRAM GÖNDƏR
# ==========================================================

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
