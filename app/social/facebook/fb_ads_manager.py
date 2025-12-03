"""
Facebook Ads manager skeleton.

Məqsəd:
- Campagin / adset / ad strukturlarını modelləşdirmək
- Real Meta Marketing API inteqrasiyasına hazır olmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class FBAdCreative:
    name: str
    primary_text: str
    headline: str
    description: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None


@dataclass
class FBAdSetConfig:
    name: str
    daily_budget: float
    optimization_goal: str
    billing_event: str
    targeting: Dict[str, object]


@dataclass
class FBCampaignConfig:
    name: str
    objective: str
    buying_type: str = "AUCTION"


class FacebookAdsManager:
    def create_campaign(self, cfg: FBCampaignConfig) -> Dict[str, object]:
        # TODO: real Meta API call
        return {"status": "stub", "campaign": cfg}

    def create_adset(self, campaign_id: str, cfg: FBAdSetConfig) -> Dict[str, object]:
        # TODO: real Meta API call
        return {"status": "stub", "campaign_id": campaign_id, "adset": cfg}

    def create_ads(self, adset_id: str, creatives: List[FBAdCreative]) -> Dict[str, object]:
        # TODO: real Meta API call
        return {
            "status": "stub",
            "adset_id": adset_id,
            "ads_count": len(creatives),
  }
