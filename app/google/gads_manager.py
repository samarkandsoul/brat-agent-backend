"""
Google Ads manager skeleton.

Məqsəd:
- Sadə kampaniya / ad group / ad modelləri
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class GAdsCampaignConfig:
    name: str
    objective: str  # SALES, LEADS və s.
    budget_daily: float


@dataclass
class GAdsAdGroupConfig:
    name: str
    bidding_strategy: str
    keywords: List[str]


@dataclass
class GAdsTextAd:
    headline_1: str
    headline_2: str
    description: str
    final_url: str


class GAdsManager:
    def create_campaign(self, cfg: GAdsCampaignConfig) -> Dict[str, Any]:
        return {
            "status": "stub",
            "campaign": cfg,
        }

    def create_ad_group(self, campaign_id: str, cfg: GAdsAdGroupConfig) -> Dict[str, Any]:
        return {
            "status": "stub",
            "campaign_id": campaign_id,
            "ad_group": cfg,
        }

    def create_text_ads(self, ad_group_id: str, ads: List[GAdsTextAd]) -> Dict[str, Any]:
        return {
            "status": "stub",
            "ad_group_id": ad_group_id,
            "ads_count": len(ads),
  }
