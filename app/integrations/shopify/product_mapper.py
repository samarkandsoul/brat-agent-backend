"""
Product Mapper

Məqsəd:
- Shopify-dan gələn xam product JSON-un
  bizim `Product` modelinə map olunması
- Bizim `Product` modelindən çıxış edib
  Shopify API üçün uyğun payload hazırlanması
"""

from __future__ import annotations

from typing import Any, Dict, List

from app.integrations.shopify.models import (
    Money,
    Image,
    Variant,
    Product,
)


class ProductMapper:
    """
    Brat sistemi ilə Shopify arasında "tərcüməçi".

    İstiqamətlər:
    - raw Shopify JSON -> Product dataclass
    - Product dataclass -> Shopify API payload (dict)
    """

    # -----------------------------
    # RAW → MODEL (Shopify → Brat)
    # -----------------------------

    def raw_to_product(self, raw: Dict[str, Any]) -> Product:
        """
        Shopify product JSON → Product modeli.

        Gözlənilən raw struktur təxmini:
        {
          "id": ...,
          "title": "...",
          "body_html": "...",
          "handle": "...",
          "tags": "tag1, tag2",
          "images": [{"src": "...", "alt": "..."}, ...],
          "variants": [
            {
              "id": ...,
              "sku": "...",
              "price": "29.99",
              "inventory_quantity": 10,
              "title": "Default Title",
              # options və s.
            }
          ]
        }
        """
        product_id = raw.get("id")

        # Tags Shopify-də string kimi gəlir: "tag1, tag2"
        tags_str = raw.get("tags", "") or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]

        # Şəkillər
        images: List[Image] = []
        for img in raw.get("images", []):
            images.append(
                Image(
                    src=img.get("src", ""),
                    alt=img.get("alt") or img.get("alt_text") or None,
                )
            )

        # Variantlar
        variants: List[Variant] = []
        for var in raw.get("variants", []):
            price_str = var.get("price", "0.0") or "0.0"
            try:
                price_value = float(price_str)
            except ValueError:
                price_value = 0.0

            variants.append(
                Variant(
                    sku=var.get("sku") or "",
                    price=Money(amount=price_value, currency=raw.get("currency", "USD")),
                    title=var.get("title"),
                    available=var.get("inventory_quantity"),
                    # Sadə placeholder – gələcəkdə option1/2/3-dən xəritə qurmaq olar
                    options={},
                )
            )

        return Product(
            id=product_id,
            title=raw.get("title", ""),
            description=raw.get("body_html", "") or "",
            handle=raw.get("handle"),
            tags=tags,
            images=images,
            variants=variants,
            collections=[],  # Gələcəkdə ayrı API ilə doldurmaq olar
        )

    def raw_list_to_products(self, rows: List[Dict[str, Any]]) -> List[Product]:
        """
        Bir neçə xam product JSON → Product list.
        """
        return [self.raw_to_product(row) for row in rows]

    # -----------------------------
    # MODEL → PAYLOAD (Brat → Shopify)
    # -----------------------------

    def product_to_payload(self, product: Product) -> Dict[str, Any]:
        """
        Product modeli → Shopify product payload.

        Shopify API-nin gözlədiyi əsas struktur:
        {
          "product": {
            "title": ...,
            "body_html": ...,
            "handle": ...,
            "tags": "tag1, tag2",
            "variants": [...],
            "images": [...]
          }
        }
        """
        tags_str = ",".join(product.tags) if product.tags else ""

        images_payload = [
            {"src": img.src, **({"alt": img.alt} if img.alt else {})}
            for img in product.images
        ]

        variants_payload: List[Dict[str, Any]] = []
        for var in product.variants:
            variants_payload.append(
                {
                    "sku": var.sku,
                    "price": f"{var.price.amount:.2f}",
                    "inventory_quantity": var.available,
                    # TODO: options → option1/2/3 mapping
                }
            )

        product_dict: Dict[str, Any] = {
            "title": product.title,
            "body_html": product.description,
            "tags": tags_str,
            "images": images_payload,
        }

        if product.handle:
            product_dict["handle"] = product.handle

        if variants_payload:
            product_dict["variants"] = variants_payload

        return {"product": product_dict}
