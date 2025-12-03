"""
Creative quality checker skeleton.

Məqsəd:
- Videonun / vizualın bəzi sadə keyfiyyət qaydalarına uyğunluğunu yoxlamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class CreativeChecklistResult:
    passed: bool
    score: float
    details: Dict[str, Any]


class CreativeQualityChecker:
    def run_checklist(
        self,
        hook_text: str,
        duration_sec: float,
        has_clear_offer: bool,
        has_branding: bool,
    ) -> CreativeChecklistResult:
        details: Dict[str, Any] = {}

        # 1 – Hook uzunluğu
        details["hook_ok"] = len(hook_text.strip()) > 0 and len(hook_text) <= 120

        # 2 – Duration
        details["duration_ok"] = 8 <= duration_sec <= 45

        # 3 – Offer
        details["offer_ok"] = has_clear_offer

        # 4 – Branding
        details["branding_ok"] = has_branding

        # Score (sadə)
        score = sum(1 for v in details.values() if v) / len(details)

        return CreativeChecklistResult(
            passed=score >= 0.75,
            score=score,
            details=details,
        )

    def summarize_issues(self, result: CreativeChecklistResult) -> List[str]:
        messages: List[str] = []
        if not result.details.get("hook_ok", False):
            messages.append("Hook ya yoxdur, ya da çox uzundur.")
        if not result.details.get("duration_ok", False):
            messages.append("Video müddəti 8–45 saniyə aralığında deyil.")
        if not result.details.get("offer_ok", False):
            messages.append("Aydın təklif (offer) görünmür.")
        if not result.details.get("branding_ok", False):
            messages.append("Brend elementi (logo, ad, vizual stil) çatışmır.")
        return messages
