"""
Facebook catalog sync skeleton.

Məqsəd:
- Shopify / daxili məhsul bazasını Facebook catalog ilə sinxron saxlamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CatalogProduct:
    external_id: str  # Shopify product id
    title: str
    description: str
    image_url: str
    price: float
    currency: str = "USD"


class FacebookCatalogSync:
    def build_feed_payload(self, products: List[CatalogProduct]) -> List[Dict[str, object]]:
        """
        Real versiyada: Facebook catalog feed formatına uyğunlaşdırma.
        """
        return [
            {
                "id": p.external_id,
                "title": p.title,
                "description": p.description,
                "image_url": p.image_url,
                "price": f"{p.price:.2f} {p.currency}",
            }
            for p in products
        ]

    def sync(self, products: List[CatalogProduct]) -> Dict[str, object]:
        """
        Hal-hazırda sadəcə payload qaytarır – gələcəkdə HTTP upload olacaq.
        """
        payload = self.build_feed_payload(products)
        return {
            "status": "stub",
            "items_count": len(payload),
      }
