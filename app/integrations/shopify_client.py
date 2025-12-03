"""
ShopifyClient – Shopify API ilə danışan əsas low-level klient (skeleton).

Məqsəd:
- Bütün HTTP çağırışlar yalnız bu class vasitəsilə getsin
- Qalan modullar (orchestrator, mapper, sync service və s.) sadəcə
  bu interface ilə işləsin, HTTP detalını görməsin
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ShopifyConfig:
    """
    Shopify konfiqurasiya modeli.

    Nümunə ENV-lər:
      SHOPIFY_API_KEY
      SHOPIFY_ACCESS_TOKEN
      SHOPIFY_STORE_DOMAIN
      SHOPIFY_API_VERSION
    """

    api_key: str
    access_token: str
    store_domain: str  # misal: "my-shop.myshopify.com"
    api_version: str = "2024-01"


class ShopifyClient:
    """
    Shopify REST API üçün low-level klient skeleton.

    Vacib: Bu mərhələdə heç bir real HTTP çağırışı implement etmirik.
    Bütün method-lar NotImplementedError atır.
    Sonrakı mərhələdə bu method-ların içini dolduracağıq.
    """

    def __init__(self, config: ShopifyConfig) -> None:
        self.config = config

    # -----------------------------
    # Daxili köməkçi util-lər
    # -----------------------------

    def _build_url(self, path: str) -> str:
        """
        API üçün baza URL generatoru.
        Misal:
          path="/products.json" ->
          "https://{store_domain}/admin/api/{version}/products.json"
        """
        base = f"https://{self.config.store_domain}/admin/api/{self.config.api_version}"
        if not path.startswith("/"):
            path = "/" + path
        return base + path

    # -----------------------------
    # PRODUCTS
    # -----------------------------

    def list_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Shopify product siyahısını çəkir.

        Gözlənilən struktur (sadələşdirilmiş):
          [
            {
              "id": ...,
              "title": "...",
              "body_html": "...",
              "handle": "...",
              "tags": "tag1, tag2",
              "images": [...],
              "variants": [...],
              ...
            },
            ...
          ]
        """
        raise NotImplementedError("ShopifyClient.list_products hələ implement olunmayıb.")

    def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Tək bir product-u id ilə çəkir.
        """
        raise NotImplementedError("ShopifyClient.get_product hələ implement olunmayıb.")

    def create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Yeni product yaradılması üçün POST /products.json

        Gözlənən payload:
          {"product": {...}}
        """
        raise NotImplementedError("ShopifyClient.create_product hələ implement olunmayıb.")

    def update_product(self, product_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mövcud product-un yenilənməsi üçün PUT /products/{id}.json
        """
        raise NotImplementedError("ShopifyClient.update_product hələ implement olunmayıb.")

    # -----------------------------
    # ORDERS
    # -----------------------------

    def list_orders(self, limit: int = 50, status: str = "any") -> List[Dict[str, Any]]:
        """
        Sifariş siyahısını çəkir.

        status:
          - "open"
          - "closed"
          - "cancelled"
          - "any" (default)
        """
        raise NotImplementedError("ShopifyClient.list_orders hələ implement olunmayıb.")

    def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Tək bir sifarişi id ilə çəkir.
        """
        raise NotImplementedError("ShopifyClient.get_order hələ implement olunmayıb.")

    # -----------------------------
    # INVENTORY
    # -----------------------------

    def update_inventory_bulk(self, stock_map: Dict[str, int]) -> Dict[str, Any]:
        """
        SKU → quantity xəritəsini götürüb stokları yeniləyən bulk update skeleton.

        Gələcəkdə:
          - SKU → inventory_item_id xəritəsi
          - inventory_levels API çağırışları
        """
        raise NotImplementedError("ShopifyClient.update_inventory_bulk hələ implement olunmayıb.")

    # -----------------------------
    # COLLECTIONS
    # -----------------------------

    def list_collections(self) -> List[Dict[str, Any]]:
        """
        Kolleksiya siyahısını çəkən skeleton method.
        """
        raise NotImplementedError("ShopifyClient.list_collections hələ implement olunmayıb.")

    # -----------------------------
    # METAFIELDS
    # -----------------------------

    def create_or_update_metafield(
        self,
        owner_resource: str,
        owner_id: int,
        namespace: str,
        key: str,
        value: str,
        value_type: str = "single_line_text_field",
    ) -> Dict[str, Any]:
        """
        Metafield yaratmaq / yeniləmək üçün skeleton.

        Gələcəkdə metafield_manager bu method-dan istifadə edəcək.
        """
        raise NotImplementedError("ShopifyClient.create_or_update_metafield hələ implement olunmayıb.")

    # -----------------------------
    # WEBHOOKS
    # -----------------------------

    def register_webhook(self, topic: str, callback_url: str) -> Dict[str, Any]:
        """
        Shopify webhook-larını qeydiyyatdan keçirmək üçün skeleton.
        """
        raise NotImplementedError("ShopifyClient.register_webhook hələ implement olunmayıb.")

    # -----------------------------
    # HEALTHCHECK
    # -----------------------------

    def health_check(self) -> bool:
        """
        Sadə healthcheck.

        Real versiyada:
          - kiçik bir /shop.json və ya /products?limit=1 sorğusu atmaq olar
        Skeleton versiyada:
          - sadəcə konfiqın mövcudluğunu yoxlayırıq
        """
        return bool(self.config.store_domain and self.config.access_token)
