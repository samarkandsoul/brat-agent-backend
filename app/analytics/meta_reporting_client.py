"""
Meta Ads Reporting client (skeleton)
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class MetaAdsQuery:
    fields: List[str]
    level: str
    date_range: Dict[str, str]


class MetaReportingClient:
    def run_report(self, query: MetaAdsQuery) -> Dict[str, Any]:
        return {
            "query": {
                "fields": query.fields,
                "level": query.level,
                "date_range": query.date_range,
            },
            "data": [],
            }
