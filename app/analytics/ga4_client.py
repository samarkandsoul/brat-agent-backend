"""
Google Analytics 4 data client (skeleton)
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class GA4QueryConfig:
    start_date: str
    end_date: str
    metrics: List[str]
    dimensions: List[str]


class GA4Client:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def run_query(self, cfg: GA4QueryConfig) -> Dict[str, Any]:
        """
        Skeleton GA4 query executor.
        Real API call yoxdur, sadəcə struktur.
        """
        return {
            "query": {
                "start_date": cfg.start_date,
                "end_date": cfg.end_date,
                "metrics": cfg.metrics,
                "dimensions": cfg.dimensions,
            },
            "rows": [],
            "summary": {"status": "ok"},
      }
