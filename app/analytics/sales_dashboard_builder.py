"""
Sales dashboard builder (skeleton)
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DashboardInput:
    total_sales: float
    total_orders: int
    ad_spend: float


class SalesDashboardBuilder:
    def build(self, inp: DashboardInput) -> Dict[str, Any]:
        return {
            "metrics": {
                "total_sales": inp.total_sales,
                "total_orders": inp.total_orders,
                "average_order_value": inp.total_sales / inp.total_orders if inp.total_orders else 0,
                "ad_spend": inp.ad_spend,
                "roas": inp.total_sales / inp.ad_spend if inp.ad_spend else 0,
            }
            }
