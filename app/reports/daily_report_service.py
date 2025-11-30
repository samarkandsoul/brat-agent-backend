import datetime as dt
import os
from typing import Optional, List

import requests

from app.reports.daily_report_models import (
    DailyReport,
    SalesMetrics,
    AdsChannelMetrics,
    ContentProductionMetrics,
    LifeMetrics,
    SystemHealthMetrics,
)
from app.integrations.telegram_client import send_telegram_message

# If you already have Shopify/monitor clients, import them here:
# from app.integrations.shopify_client import get_last_24h_sales_metrics
# from app.integrations.monitor_client import fetch_monitor_status

MONITOR_STATUS_URL = os.getenv("MONITOR_STATUS_URL")  # e.g. https://samarkand-monitor.onrender.com/health


# --------- DATA FETCH HELPERS (PLACEHOLDERS / ADAPT TO REAL CLIENTS) ---------- #


def fetch_sales_metrics() -> Optional[SalesMetrics]:
    """
    Fetch last 24h sales metrics from Shopify (or your data source).

    TODO: Replace placeholder with real integration using shopify_client.
    """
    # ---- PLACEHOLDER EXAMPLE (dummy data) ----
    # Here you should call your real Shopify service.
    return SalesMetrics(
        total_revenue=185.0,
        currency="USD",
        orders_count=4,
        conversion_rate=2.8,
        avg_order_value=46.25,
        atc_rate=5.3,
        checkout_drop_rate=12.1,
    )


def fetch_ads_metrics() -> List[AdsChannelMetrics]:
    """
    Fetch ads metrics (Meta, TikTok, etc.) from your KPI/ads agents.

    TODO: integrate with ds12_kpi_analytics_agent or your data store.
    """
    # ---- PLACEHOLDER EXAMPLE ----
    meta = AdsChannelMetrics(
        channel_name="Meta",
        spend=40.0,
        revenue=60.0,
        impressions=8000,
        clicks=150,
        ctr=1.875,
        cpc=0.27,
        cpm=5.0,
        roas=1.5,
        best_creatives=["Angle: Heritage + Modern Table", "UGC #003"],
        notes="ROAS slightly weak; keep best creative, pause worst 2 adsets.",
    )
    tiktok = AdsChannelMetrics(
        channel_name="TikTok",
        spend=25.0,
        revenue=80.0,
        impressions=5000,
        clicks=135,
        ctr=2.7,
        cpc=0.19,
        cpm=5.0,
        roas=3.2,
        best_creatives=["Video: Tablecloth Folding Trick"],
        notes="Strong ROAS; scale winning creative 20–30%.",
    )
    return [meta, tiktok]


def fetch_content_metrics() -> ContentProductionMetrics:
    """
    Fetch how many videos/scripts/images were produced by content agents.

    TODO: connect to your content pipeline or task DB.
    """
    return ContentProductionMetrics(
        tiktok_videos_created=2,
        scripts_written=3,
        image_variants_created=4,
        trends_detected=2,
        notes="Today focused on TikTok hooks around 'hosting guests' theme.",
    )


def fetch_life_metrics() -> LifeMetrics:
    """
    Fetch Zahid's life/health/time data from LIFE agents.

    TODO: later integrate with life01-05 agents or Notion/Sheets.
    """
    return LifeMetrics(
        planned_focus_minutes=180,
        completed_focus_minutes=120,
        workout_planned=True,
        workout_completed=False,
        water_target_liters=2.5,
        water_completed_liters=1.4,
        sleep_hours_last_night=7.2,
        notes="Energy OK; main risk = unfinished workout. Aim to complete in evening.",
    )


def fetch_system_health() -> Optional[SystemHealthMetrics]:
    """
    Query your monitor service for system health.

    If you already have Samarkand Monitor API, call it here.
    """
    if not MONITOR_STATUS_URL:
        return None

    try:
        resp = requests.get(MONITOR_STATUS_URL, timeout=5)
        status_code = resp.status_code
        if resp.headers.get("content-type", "").startswith("application/json"):
            data = resp.json()
        else:
            data = {}
    except Exception:  # noqa: BLE001
        # If monitor call fails, return "red" health.
        return SystemHealthMetrics(
            monitor_service_alive=False,
            agent_mesh_alive=False,
            http_status_code=0,
            incidents_last_24h=["Monitor service unreachable."],
        )

    # Adjust key names to your real monitor JSON
    monitor_ok = bool(data.get("monitor_service", {}).get("alive", True))
    agent_mesh_ok = bool(data.get("agent_mesh", {}).get("alive", True))
    incidents = data.get("incidents", []) if isinstance(data.get("incidents"), list) else []

    return SystemHealthMetrics(
        monitor_service_alive=monitor_ok,
        agent_mesh_alive=agent_mesh_ok,
        http_status_code=status_code,
        incidents_last_24h=incidents,
    )


# ---------- REPORT BUILDER ---------- #


def build_daily_report() -> DailyReport:
    """
    Aggregate all metrics into a DailyReport object.
    """
    today = dt.datetime.utcnow().date().isoformat()

    sales = fetch_sales_metrics()
    ads = fetch_ads_metrics()
    content = fetch_content_metrics()
    life = fetch_life_metrics()
    sys_health = fetch_system_health()

    headline_parts: List[str] = []
    key_warnings: List[str] = []

    if sales:
        if sales.total_revenue == 0:
            headline_parts.append("No sales in last 24h.")
        else:
            headline_parts.append(
                f"Last 24h revenue: {sales.total_revenue:.2f} {sales.currency} "
                f"({sales.orders_count} orders, {sales.conversion_rate:.1f}% CR)."
            )
        if sales.checkout_drop_rate and sales.checkout_drop_rate > 10:
            key_warnings.append(
                f"High checkout drop: {sales.checkout_drop_rate:.1f}% → run ds10_checkout_funnel_optimizer."
            )

    for ch in ads:
        if ch.roas is not None and ch.roas < 1.2:
            key_warnings.append(f"Weak ROAS on {ch.channel_name}: {ch.roas:.2f}.")
        if ch.roas is not None and ch.roas >= 2.5:
            headline_parts.append(f"{ch.channel_name} ads performing strong (ROAS {ch.roas:.2f}).")

    if sys_health and (not sys_health.monitor_service_alive or not sys_health.agent_mesh_alive):
        key_warnings.append("System health issue: monitor or agent-mesh not fully alive.")

    if life and life.workout_planned and not life.workout_completed:
        key_warnings.append("Workout planned but not completed yet. Protect health system, Brat.")

    headline = " ".join(headline_parts) if headline_parts else "Daily system status summary."

    return DailyReport(
        date_iso=today,
        sales=sales,
        ads_channels=ads,
        content=content,
        life=life,
        system_health=sys_health,
        headline=headline,
        key_warnings=key_warnings,
    )


# ---------- FORMAT REPORT AS TEXT ---------- #


def format_report_as_text(report: DailyReport) -> str:
    """
    Build the human-readable Brat-style daily report for Telegram.
    """
    lines: List[str] = []

    lines.append("🧠 *Samarkand Soul – Daily Command Report*")
    lines.append(f"Date (UTC): `{report.date_iso}`\n")

    # 1) Sales
    if report.sales:
        s = report.sales
        lines.append("🛒 *1. Sales & Shopify*")
        lines.append(
            f"- Revenue (24h): *{s.total_revenue:.2f} {s.currency}*  "
            f"({s.orders_count} orders, {s.conversion_rate:.1f}% CR)"
        )
        if s.avg_order_value is not None:
            lines.append(f"- AOV: {s.avg_order_value:.2f} {s.currency}")
        if s.atc_rate is not None:
            lines.append(f"- Add-to-cart rate: {s.atc_rate:.1f}%")
        if s.checkout_drop_rate is not None:
            lines.append(f"- Checkout drop: {s.checkout_drop_rate:.1f}%")
        lines.append("")

    # 2) Ads
    if report.ads_channels:
        lines.append("🎯 *2. Ads & Creatives*")
        for ch in report.ads_channels:
            roas_str = f"{ch.roas:.2f}" if ch.roas is not None else "N/A"
            lines.append(
                f"- *{ch.channel_name}*: spend {ch.spend:.2f}, revenue {ch.revenue:.2f}, "
                f"CTR {ch.ctr:.2f}%, ROAS {roas_str}"
            )
            if ch.best_creatives:
                lines.append("  • Best creatives: " + "; ".join(ch.best_creatives))
            if ch.notes:
                lines.append(f"  • Note: {ch.notes}")
        lines.append("")

    # 3) Content
    if report.content:
        c = report.content
        lines.append("🎥 *3. Content Factory*")
        lines.append(f"- TikTok videos created: {c.tiktok_videos_created}")
        lines.append(f"- Scripts written: {c.scripts_written}")
        lines.append(f"- Image variants: {c.image_variants_created}")
        lines.append(f"- Trends detected: {c.trends_detected}")
        if c.notes:
            lines.append(f"- Note: {c.notes}")
        lines.append("")

    # 4) Life / Health
    if report.life:
        l = report.life
        lines.append("💊 *4. Zahid Brat – Life & Energy*")
        lines.append(
            f"- Focus: {l.completed_focus_minutes}/{l.planned_focus_minutes} minutes completed"
        )
        if l.workout_planned:
            lines.append(
                f"- Workout: {'✅ completed' if l.workout_completed else '❌ pending'}"
            )
        else:
            lines.append("- Workout: —")
        lines.append(
            f"- Water: {l.water_completed_liters:.1f}/{l.water_target_liters:.1f} L"
        )
        if l.sleep_hours_last_night is not None:
            lines.append(f"- Sleep last night: {l.sleep_hours_last_night:.1f} h")
        if l.notes:
            lines.append(f"- Note: {l.notes}")
        lines.append("")

    # 5) System health
    if report.system_health:
        h = report.system_health
        lines.append("🖥 *5. System Health*")
        lines.append(f"- Monitor service: {'✅ Alive' if h.monitor_service_alive else '❌ Down'}")
        lines.append(f"- Agent mesh: {'✅ Alive' if h.agent_mesh_alive else '❌ Down'}")
        lines.append(f"- HTTP status: {h.http_status_code}")
        if h.incidents_last_24h:
            lines.append("- Incidents (last 24h):")
            for inc in h.incidents_last_24h:
                lines.append(f"  • {inc}")
        lines.append("")

    # Summary & warnings
    if report.headline:
        lines.append(f"📌 *Summary*: {report.headline}")
    if report.key_warnings:
        lines.append("\n⚠️ *Key Warnings*")
        for w in report.key_warnings:
            lines.append(f"- {w}")

    return "\n".join(lines)


# ---------- PUBLIC HELPERS ---------- #


def generate_daily_report_text() -> str:
    """
    Build report object and return formatted text (for preview or logs).
    """
    report = build_daily_report()
    return format_report_as_text(report)


def send_daily_report_via_telegram() -> bool:
    """
    Build and send the daily report to Telegram. Returns True on success.
    """
    text = generate_daily_report_text()
    return send_telegram_message(text)
