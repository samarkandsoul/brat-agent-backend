"""
Profit calculator (skeleton)
"""

from dataclasses import dataclass


@dataclass
class ProfitInput:
    revenue: float
    product_cost: float
    ad_spend: float
    shipping_cost: float = 0.0
    extra_fees: float = 0.0


@dataclass
class ProfitResult:
    gross_profit: float
    net_profit: float
    margin: float


class ProfitCalculator:
    def calculate(self, cfg: ProfitInput) -> ProfitResult:
        gross = cfg.revenue - cfg.product_cost
        net = gross - cfg.ad_spend - cfg.shipping_cost - cfg.extra_fees
        margin = net / cfg.revenue if cfg.revenue else 0

        return ProfitResult(gross_profit=gross, net_profit=net, margin=margin)
