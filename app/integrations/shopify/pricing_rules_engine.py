from typing import Any, Dict
from decimal import Decimal


class PricingRulesEngine:
    """
    70/30 modelinə uyğun price hesablayan sadə engine.
    """

    def calculate_price(self, base_cost: Decimal, rules: Dict[str, Any]) -> Decimal:
        """
        Məs: base_cost + margin + vergilər və s.
        """
        margin_pct = Decimal(rules.get("margin_pct", "0.7"))
        price = base_cost / (Decimal("1") - margin_pct)
        return price.quantize(Decimal("0.01"))
