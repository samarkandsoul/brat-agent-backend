# app/services/tiktok_growth_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict


app = FastAPI(
    title="Brat TikTok Growth API",
    version="0.1.0",
    description="Service layer for orchestrating TikTok growth agents.",
)


# --------- Basic DTOs (data models) --------- #

class TikTokIdeaRequest(BaseModel):
    product_id: Optional[str] = None
    offer: Optional[str] = None
    goal: str  # "sales", "traffic", "followers" və s.
    language: str = "en"
    notes: Optional[str] = None


class TikTokPostPlan(BaseModel):
    hook: str
    script: str
    caption: str
    hashtags: List[str]
    sound_hint: Optional[str] = None


class ScheduleRequest(BaseModel):
    video_url: str
    caption: str
    schedule_at: Optional[str] = None  # ISO datetime string
    timezone: Optional[str] = "UTC"


# --------- Orchestrator Skeleton --------- #

class TikTokGrowthOrchestrator:
    """
    Bu class tiktok_growth içindəki bütün agentləri
    (ad_script_lab, creative_brain, hashtag_brain, sound_trend_scanner və s.)
    üzərində üst-qat orkestr rolunu oynayacaq.

    İNDİLİK SKELETONDUR – içi sonradan real agent çağırışları ilə doldurulacaq.
    """

    def __init__(self) -> None:
        # Burada gələcəkdə real agent modullarını import edib
        # instance kimi saxlayacağıq.
        # Məs: self.script_lab = AdScriptLab(...)
        pass

    async def generate_idea(self, req: TikTokIdeaRequest) -> TikTokPostPlan:
        """
        Gələcəkdə:
        - ad_script_lab → hook + script
        - creative_brain → kreativ bucaq
        - hashtag_brain → hashtag listi
        - sound_trend_scanner → sound hint
        İndi isə sadəcə skeleton cavab qaytarır.
        """

        # TODO: real agent çağırışları əlavə ediləcək.
        dummy_hashtags = ["#tiktok", "#samarkandsoul", "#bratengine"]

        return TikTokPostPlan(
            hook="This is a placeholder hook for your product.",
            script="This is a placeholder script. Real script engine will be wired soon.",
            caption="Placeholder caption for your TikTok video.",
            hashtags=dummy_hashtags,
            sound_hint="Use a currently trending sound in your niche.",
        )

    async def schedule_post(self, req: ScheduleRequest) -> Dict[str, str]:
        """
        Gələcəkdə:
        - tiktok_post_scheduler agentini çağıracaq.
        Hal-hazırda sadəcə success mesajı qaytarır.
        """
        # TODO: real TikTok API integration.
        return {
            "status": "scheduled_fake",
            "video_url": req.video_url,
            "schedule_at": req.schedule_at or "ASAP",
            "timezone": req.timezone or "UTC",
        }


# Global orchestrator instance
orchestrator = TikTokGrowthOrchestrator()


# --------- Health & basic endpoints --------- #

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Render monitor, backend və monitor-ui üçün heartbeat endpoint.
    """
    return {"status": "ok", "service": "tiktok_growth"}


@app.post("/tiktok/idea", response_model=TikTokPostPlan)
async def create_tiktok_idea(req: TikTokIdeaRequest):
    """
    High-level endpoint:
    Bir product/offer üçün TikTok ideyası + script + caption skeletonu qaytarır.
    Hazırda dummy cavabdır, amma strukturu sabitdir.
    """
    try:
        return await orchestrator.generate_idea(req)
    except Exception as exc:  # noqa: BLE001
        # Burada gələcəkdə global_error_handler-ə pass edəcəyik.
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/tiktok/schedule")
async def schedule_tiktok_post(req: ScheduleRequest):
    """
    TikTok postunu planlamaq üçün skeleton endpoint.
    Gələcəkdə real TikTok API + tiktok_post_scheduler agentinə bağlanacaq.
    """
    try:
        result = await orchestrator.schedule_post(req)
        return result
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))
