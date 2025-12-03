"""
Performance Max reporting service (skeleton)
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PMAXReportConfig:
    start_date: str
    end_date: str
    include_assets: bool = False


class PMAXReportingService:
    def generate(self, cfg: PMAXReportConfig) -> Dict[str, Any]:
        return {
            "report_period": {
                "start": cfg.start_date,
                "end": cfg.end_date,
            },
            "include_assets": cfg.include_assets,
            "rows": [],
        }
