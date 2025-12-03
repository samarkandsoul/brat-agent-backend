"""
Pricing Rules Engine (skeleton)

Məqsəd:
- Məhsullar və variantları üçün qiymət təklifləri hesablamaq
- Hələ real biznes qaydaları yoxdur, sadə skeleton məntiqindən istifadə olunur
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional

from app.integrations.shopify.models import Product, Variant, Money


@dataclass
class PricingContext:
    """
    Bir məhsul üçün qiymət hesablamaq üçün kontekst.
    Gələcəkdə:
      - cost_by_sku (məhsul maya dəyəri)
      - target_margin
      - max_discount və s. sahələr genişləndirilə bilər.
    """

    product: Product
    cost_by_sku: Dict[str, float] = None
    target_margin: float = 0.3  # 30% marja hədəfi
    max_discount: float = 0.5   # maksimum 50% endirim (placeholder)


@dataclass
class PricingSuggestion:
    sku: str
    old_price: Money
    suggested_price: Money
    reason: str


@dataclass
class PricingSuggestionBatch:
    product_id: Optional[int]
    handle: Optional[str]
    suggestions: List[PricingSuggestion]


class PricingRulesEngine:
    """
    Sadə skeleton pricing engine.

    İndi:
      - Hər variant üçün sadəcə mövcud qiyməti saxlayır və "no_change" deyir.
    Gələcəkdə:
      - cost_by_sku + target_margin əsasında yeni qiymətlər hesablanacaq.
    """

    def suggest_for_product(self, ctx: PricingContext) -> PricingSuggestionBatch:
        suggestions: List[PricingSuggestion] = []

        cost_by_sku = ctx.cost_by_sku or {}

        for var in ctx.product.variants:
            cost = cost_by_sku.get(var.sku)

            # Skeleton məntiq:
            # əgər cost bilinmirsə → qiyməti dəyişmirik
            if cost is None or cost <= 0:
                suggested_price = var.price
                reason = "no_cost_info_keep_price"
            else:
                # Gələcəkdə burada real formullar olacaq.
                # İndi sadəcə cost * (1 + target_margin) + round
                base_amount = cost * (1 + ctx.target_margin)
                suggested_price = Money(
                    amount=round(base_amount, 2),
                    currency=var.price.currency,
                )
                reason = "target_margin_rule"

            suggestions.append(
                PricingSuggestion(
                    sku=var.sku,
                    old_price=var.price,
                    suggested_price=suggested_price,
                    reason=reason,
                )
            )

        return PricingSuggestionBatch(
            product_id=ctx.product.id,
            handle=ctx.product.handle,
            suggestions=suggestions,
        )

    def suggest_for_products(self, products: List[Product]) -> List[PricingSuggestionBatch]:
        """
        Bir neçə məhsul üçün sadə skeleton təklif generasiyası.
        Hazırda cost map istifadə etmir (hamı üçün no_cost_info_keep_price olacaq).
        Gələcəkdə:
          - məhsul və SKU-lara görə cost xəritəsi qoşulacaq.
        """
        batches: List[PricingSuggestionBatch] = []
        for product in products:
            ctx = PricingContext(product=product)
            batch = self.suggest_for_product(ctx)
            batches.append(batch)
        return batches
