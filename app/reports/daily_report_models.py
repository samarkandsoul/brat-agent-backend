from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SalesMetrics:
    total_revenue: float
    currency: str
    orders_count: int
    conversion_rate: float  # percent (0–100)
    avg_order_value: Optional[float] = None
    atc_rate: Optional[float] = None
    checkout_drop_rate: Optional[float] = None


@dataclass
class AdsChannelMetrics:
    channel_name: str  # e.g. "Meta", "TikTok"
    spend: float
    revenue: float
    impressions: int
    clicks: int
    ctr: float  # percent (0–100)
    cpc: Optional[float] = None
    cpm: Optional[float] = None
    roas: Optional[float] = None
    best_creatives: List[str] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class ContentProductionMetrics:
    tiktok_videos_created: int = 0
    scripts_written: int = 0
    image_variants_created: int = 0
    trends_detected: int = 0
    notes: Optional[str] = None


@dataclass
class LifeMetrics:
    planned_focus_minutes: int = 0
    completed_focus_minutes: int = 0
    workout_planned: bool = False
    workout_completed: bool = False
    water_target_liters: float = 0.0
    water_completed_liters: float = 0.0
    sleep_hours_last_night: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class SystemHealthMetrics:
    monitor_service_alive: bool
    agent_mesh_alive: bool
    http_status_code: int
    incidents_last_24h: List[str] = field(default_factory=list)


@dataclass
class DailyReport:
    date_iso: str
    sales: Optional[SalesMetrics] = None
    ads_channels: List[AdsChannelMetrics] = field(default_factory=list)
    content: Optional[ContentProductionMetrics] = None
    life: Optional[LifeMetrics] = None
    system_health: Optional[SystemHealthMetrics] = None
    headline: Optional[str] = None
    key_warnings: List[str] = field(default_factory=list)
