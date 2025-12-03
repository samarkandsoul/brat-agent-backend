"""
Product Mapper

Brat agentlərindən gələn məhsul datasını
Shopify API üçün uyğun struktura çevirən skeleton.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class BratProductPayload:
  title: str
  description: str
  price: float
  currency: str = "USD"
  sku: Optional[str] = None
  tags: Optional[List[str]] = None
  images: Optional[List[str]] = None
  options: Optional[Dict[str, List[str]]] = None  # {"Size": ["S","M"]}


@dataclass
class ShopifyProductPayload:
  title: str
  body_html: str
  variants: List[Dict[str, Any]]
  images: List[Dict[str, Any]]
  tags: str


class ProductMapper:
  """Brat → Shopify məhsul map-ləmə beyni."""

  def from_raw(self, raw: Dict[str, Any]) -> BratProductPayload:
    # TODO: input validation + error handling
    return BratProductPayload(
      title=(raw.get("title") or "").strip(),
      description=(raw.get("description") or "").strip(),
      price=float(raw.get("price", 0.0)),
      currency=raw.get("currency", "USD"),
      sku=raw.get("sku"),
      tags=raw.get("tags") or [],
      images=raw.get("images") or [],
      options=raw.get("options") or {},
    )

  def to_shopify(self, brat: BratProductPayload) -> ShopifyProductPayload:
    # TODO: multi-variant dəstəyi, inventory, taxes və s.
    variant = {
      "price": str(brat.price),
      "sku": brat.sku or "",
    }
    images = [{"src": url} for url in (brat.images or [])]
    tags_str = ",".join(brat.tags or [])

    return ShopifyProductPayload(
      title=brat.title,
      body_html=brat.description,
      variants=[variant],
      images=images,
      tags=tags_str,
    )

  def map_raw_to_shopify(self, raw: Dict[str, Any]) -> Dict[str, Any]:
    brat_payload = self.from_raw(raw)
    shopify_payload = self.to_shopify(brat_payload)

    return {
      "product": {
        "title": shopify_payload.title,
        "body_html": shopify_payload.body_html,
        "variants": shopify_payload.variants,
        "images": shopify_payload.images,
        "tags": shopify_payload.tags,
      }
  }
