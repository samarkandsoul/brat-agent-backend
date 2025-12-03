"""
Retention analysis engine (skeleton)
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class OrderData:
    customer_id: str
    order_date: str


class RetentionAnalysis:
    def compute_cohorts(self, orders: List[OrderData]) -> Dict[str, int]:
        """
        Sadə cohort hesablaması — skeleton
        """
        cohorts: Dict[str, int] = {}

        for order in orders:
            month = order.order_date[:7]
            cohorts[month] = cohorts.get(month, 0) + 1

        return cohorts
