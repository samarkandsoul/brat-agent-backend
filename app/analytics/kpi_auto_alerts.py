"""
KPI auto-alert engine (skeleton)
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KPIThreshold:
    name: str
    min_value: float
    max_value: float


@dataclass
class KPIReport:
    name: str
    value: float


class KPIAutoAlerts:
    def check(self, thresholds: List[KPIThreshold], report: List[KPIReport]) -> Dict[str, str]:
        alerts = {}

        threshold_map = {t.name: t for t in thresholds}
        for r in report:
            t = threshold_map.get(r.name)
            if not t:
                continue

            if r.value < t.min_value:
                alerts[r.name] = "below_min"
            elif r.value > t.max_value:
                alerts[r.name] = "above_max"

        return alerts
