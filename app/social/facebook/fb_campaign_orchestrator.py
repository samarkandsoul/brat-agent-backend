"""
Facebook campaign orchestrator skeleton.

Məqsəd:
- Creative brain + ads manager + catalog sync birlikdə işləsin
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .fb_ads_manager import (
    FacebookAdsManager,
    FBCampaignConfig,
    FBAdSetConfig,
    FBAdCreative,
)
from .fb_creative_brain import FacebookCreativeBrain, FBCreativeContext


@dataclass
class OrchestratorInput:
    product_name: str
    main_benefit: str
    objection: str
    niche: str
    daily_budget: float


class FacebookCampaignOrchestrator:
    def __init__(self, ads_manager: FacebookAdsManager, creative_brain: FacebookCreativeBrain):
        self.ads_manager = ads_manager
        self.creative_brain = creative_brain

    def launch_simple_campaign(self, req: OrchestratorInput) -> Dict[str, object]:
        """
        1) Campaign yaradır
        2) Adset qurur
        3) 1 dənə sadə creative ilə ad yaradır
        """
        campaign_cfg = FBCampaignConfig(
            name=f"{req.product_name} – Main",
            objective="SALES",
        )
        campaign_res = self.ads_manager.create_campaign(campaign_cfg)

        adset_cfg = FBAdSetConfig(
            name="Main Adset",
            daily_budget=req.daily_budget,
            optimization_goal="PURCHASE",
            billing_event="IMPRESSIONS",
            targeting={"niche": req.niche},
        )
        adset_res = self.ads_manager.create_adset(
            campaign_id=str(campaign_res.get("id", "stub_campaign")),
            cfg=adset_cfg,
        )

        creative_ctx = FBCreativeContext(
            product_name=req.product_name,
            main_benefit=req.main_benefit,
            objection=req.objection,
        )
        primary, headline, description = self.creative_brain.generate_all(creative_ctx)

        creatives: List[FBAdCreative] = [
            FBAdCreative(
                name="Main Creative",
                primary_text=primary,
                headline=headline,
                description=description,
            )
        ]
        ads_res = self.ads_manager.create_ads(
            adset_id=str(adset_res.get("id", "stub_adset")),
            creatives=creatives,
        )

        return {
            "campaign": campaign_res,
            "adset": adset_res,
            "ads": ads_res,
                 }
