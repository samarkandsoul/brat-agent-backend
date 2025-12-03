# app/services/tiktok_growth_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict


app = FastAPI(
    title="Brat TikTok Growth API",
    version="0.1.1",
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
    Bütün TikTok agentlərini idarə edən üst qatda orkestr class.
    (ad_script_lab, creative_brain, hashtag_brain və s.)
    Hal-hazırda skeleton formadadır.
    """

    def __init__(self) -> None:
        # Gələcəkdə real agent modullarını burada instanslaşdıracağıq.
        pass

    async def generate_idea(self, req: TikTokIdeaRequest) -> TikTokPostPlan:
        dummy_hashtags = ["#tiktok", "#samarkandsoul", "#bratengine"]

        return TikTokPostPlan(
            hook="This is a placeholder hook for your product.",
            script="This is a placeholder script. Real script engine will be wired soon.",
            caption="Placeholder caption for your TikTok video.",
            hashtags=dummy_hashtags,
            sound_hint="Use a trending sound in your niche.",
        )

    async def schedule_post(self, req: ScheduleRequest) -> Dict[str, str]:
        return {
            "status": "scheduled_fake",
            "video_url": req.video_url,
            "schedule_at": req.schedule_at or "ASAP",
            "timezone": req.timezone or "UTC",
        }


# Global orchestrator instance
orchestrator = TikTokGrowthOrchestrator()


# --------- Health & Status Endpoints --------- #

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Render monitor & agent-brain heartbeat endpoint.
    """
    return {"status": "ok", "service": "tiktok_growth"}


@app.get("/status")
async def status_check() -> Dict[str, str]:
    """
    Servisin vəziyyətini bildirən endpoint.
    Monitor və orchestrator üçün lazımlıdır.
    """
    return {
        "service": "tiktok_growth",
        "uptime": "running",
        "mode": "live",
        "version": "0.1.1"
    }


# --------- Main TikTok Endpoints --------- #

@app.post("/tiktok/idea", response_model=TikTokPostPlan)
async def create_tiktok_idea(req: TikTokIdeaRequest):
    try:
        return await orchestrator.generate_idea(req)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/tiktok/schedule")
async def schedule_tiktok_post(req: ScheduleRequest):
    try:
        return await orchestrator.schedule_post(req)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))
