"""
Google Merchant Center sync skeleton.

Məqsəd:
- Məhsulları GMC feed formatına gətirmək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class GMCProduct:
    id: str
    title: str
    description: str
    image_link: str
    link: str
    price: float
    currency: str = "USD"
    availability: str = "in stock"


class GMCSyncService:
    def build_feed_row(self, p: GMCProduct) -> Dict[str, str]:
        return {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "image_link": p.image_link,
            "link": p.link,
            "price": f"{p.price:.2f} {p.currency}",
            "availability": p.availability,
        }

    def build_feed(self, products: List[GMCProduct]) -> List[Dict[str, str]]:
        return [self.build_feed_row(p) for p in products]

    def sync(self, products: List[GMCProduct]) -> Dict[str, object]:
        feed = self.build_feed(products)
        # TODO: real HTTP upload to GMC
        return {
            "status": "stub",
            "items_count": len(feed),
  }
