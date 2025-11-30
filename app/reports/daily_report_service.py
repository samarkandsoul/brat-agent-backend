import datetime as dt
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
from app.config.settings import settings
from app.integrations.telegram_client import send_to_default_chat


# --------- DATA FETCH HELPERS (PLACEHOLDERS / ADAPT TO REAL CLIENTS) ---------- #


def fetch_sales_metrics() -> Optional[SalesMetrics]:
    """
    Fetch last 24h sales metrics from Shopify (or your data source).

    TODO: Replace placeholder with real integration using shopify_client.
    """
    # ---- PLACEHOLDER EXAMPLE (dummy data) ----
    return SalesMetrics(
        total_revenue=185.0,
        currency=settings.DEFAULT_CURRENCY,
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
    Query Samarkand Monitor API for system health.
    """
    url = settings.MONITOR_STATUS_URL
    if not url:
        return None

    try:
        resp = requests.get(url, timeout=5)
        status_code = resp.status_code
        data = (
            resp.json()
            if resp.headers.get("content-type", "").startswith("application/json")
            else {}
        )
    except Exception:  # noqa: BLE001
        return SystemHealthMetrics(
            monitor_service_alive=False,
            agent_mesh_alive=False,
            http_status_code=0,
            incidents_last_24h=["Monitor service unreachable."],
        )

    monitor_ok = bool(data.get("monitor_service", {}).get("alive", True))
    agent_mesh_ok = bool(data.get("agent_mesh", {}).get("alive", True))
    incidents_raw = data.get("incidents", [])
    incidents = incidents_raw if isinstance(incidents_raw, list) else []

    return SystemHealthMetrics(
        monitor_service_alive=monitor_ok,
        agent_mesh_alive=agent_mesh_ok,
        http_status_code=status_code,
        incidents_last_24h=incidents,
    )


# --------- BUILD & FORMAT REPORT ---------- #


def build_daily_report() -> DailyReport:
    now = dt.datetime.utcnow()

    sales = fetch_sales_metrics()
    ads = fetch_ads_metrics()
    content = fetch_content_metrics()
    life = fetch_life_metrics()
    system = fetch_system_health()

    return DailyReport(
        generated_at_utc=now,
        sales_metrics=sales,
        ads_channels=ads,
        content_metrics=content,
        life_metrics=life,
        system_health=system,
    )


def generate_daily_report_text() -> str:
    report = build_daily_report()
    ts = report.generated_at_utc.strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []
    lines.append(f"📊 *Samarkand Soul — Daily Command Report*")
    lines.append(f"_Generated at: {ts}_")
    lines.append("")

    # Sales
    if report.sales_metrics:
        s = report.sales_metrics
        lines.append("💰 *Sales (last 24h)*")
        lines.append(
            f"- Revenue: *{s.total_revenue:.2f} {s.currency}* "
            f"(orders: {s.orders_count})"
        )
        lines.append(
            f"- CR: {s.conversion_rate:.2f}% | AOV: {s.avg_order_value:.2f} {s.currency}"
        )
        lines.append(
            f"- ATC: {s.atc_rate:.2f}% | Checkout drop: {s.checkout_drop_rate:.2f}%"
        )
        lines.append("")

    # Ads
    if report.ads_channels:
        lines.append("📣 *Ads Performance*")
        for ch in report.ads_channels:
            lines.append(
                f"- *{ch.channel_name}*: Spend {ch.spend:.2f}, "
                f"Rev {ch.revenue:.2f}, ROAS {ch.roas:.2f}"
            )
            lines.append(
                f"  CTR {ch.ctr:.2f}% | CPC {ch.cpc:.2f} | CPM {ch.cpm:.2f}"
            )
            if ch.best_creatives:
                lines.append("  Best creatives:")
                for c in ch.best_creatives:
                    lines.append(f"    • {c}")
            if ch.notes:
                lines.append(f"  _{ch.notes}_")
        lines.append("")

    # Content
    c = report.content_metrics
    lines.append("🎥 *Content Production*")
    lines.append(
        f"- TikTok videos: {c.tiktok_videos_created} | Scripts: {c.scripts_written}"
    )
    lines.append(f"- Image variants: {c.image_variants_created}")
    lines.append(f"- Trends detected: {c.trends_detected}")
    if c.notes:
        lines.append(f"_Note: {c.notes}_")
    lines.append("")

    # Life
    l = report.life_metrics
    lines.append("🧬 *Life & Energy*")
    lines.append(
        f"- Focus: {l.completed_focus_minutes}/{l.planned_focus_minutes} min"
    )
    lines.append(
        f"- Workout: {'✅' if l.workout_completed else '❌'} "
        f"(planned: {'yes' if l.workout_planned else 'no'})"
    )
    lines.append(
        f"- Water: {l.water_completed_liters:.1f}/{l.water_target_liters:.1f} L"
    )
    lines.append(f"- Sleep last night: {l.sleep_hours_last_night:.1f} h")
    if l.notes:
        lines.append(f"_Note: {l.notes}_")
    lines.append("")

    # System health
    if report.system_health:
        sys = report.system_health
        lines.append("🖥 *System Health*")
        lines.append(
            f"- Monitor service: {'🟢 Alive' if sys.monitor_service_alive else '🔴 Down'}"
        )
        lines.append(
            f"- Agent mesh: {'🟢 Alive' if sys.agent_mesh_alive else '🔴 Down'}"
        )
        lines.append(f"- HTTP status: {sys.http_status_code}")
        if sys.incidents_last_24h:
            lines.append("  Incidents (last 24h):")
            for inc in sys.incidents_last_24h:
                lines.append(f"    • {inc}")
    else:
        lines.append("🖥 *System Health*")
        lines.append("- _No monitor status available (MONITOR_STATUS_URL not set)._")

    return "\n".join(lines)


def send_daily_report_via_telegram() -> bool:
    """
    Build + format + send to DEFAULT_CHAT_ID.
    Render cron job could trigger /daily-report/send which calls this.
    """
    text = generate_daily_report_text()
    return send_to_default_chat(text)
