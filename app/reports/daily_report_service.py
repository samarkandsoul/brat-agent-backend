import datetime as dt
import os
from typing import Optional, List

from app.reports.daily_report_models import (
    DailyReport,
    SalesMetrics,
    AdsChannelMetrics,
    ContentProductionMetrics,
    LifeMetrics,
    SystemHealthMetrics,
)

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

    import requests  # local import to avoid hard dependency

    try:
        resp = requests.get(MONITOR_STATUS_URL, timeout=5)
        status_code = resp.status_code
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
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
