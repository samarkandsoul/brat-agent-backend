"""
ShopifyClient – Shopify API ilə danışan əsas low-level klient.

Bu versiya:
- Əsas məhsul və sifariş əməliyyatlarını real HTTP ilə edir:
    - list_products
    - get_product
    - create_product
    - update_product
    - list_orders
    - get_order
- Qalan method-lar hələ NotImplementedError olaraq qalır
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class ShopifyConfig:
    """
    Shopify konfiqurasiya modeli.

    Adətən bu dəyərlər ENV-dən gələcək:

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
    Shopify REST API üçün low-level klient.

    Qaydalar:
      - Bütün HTTP çağırışlar yalnız BU class-dan keçməlidir
      - Qalan modullar (orchestrator, mapper, sync service və s.) HTTP detalını görməməlidir
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

    def _headers(self) -> Dict[str, str]:
        """
        Shopify üçün standart header-lər.
        """
        return {
            "X-Shopify-Access-Token": self.config.access_token,
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Internal HTTP helper.

        Səhv olarsa Exception atır – yüksək səviyyədə GlobalErrorHandler tutacaq.
        """
        url = self._build_url(path)
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers=self._headers(),
            params=params,
            json=json,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data

    # -----------------------------
    # PRODUCTS
    # -----------------------------

    def list_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Shopify product siyahısını çəkir.

        Endpoint:
          GET /products.json?limit={limit}
        """
        data = self._request(
            method="GET",
            path="/products.json",
            params={"limit": limit},
        )
        # Shopify product-ları "products" açarında qaytarır
        return data.get("products", [])

    def get_product(self, product_id: int) -> Dict[str, Any]:
        """
        Tək bir product-u id ilə çəkir.

        Endpoint:
          GET /products/{id}.json
        """
        data = self._request(
            method="GET",
            path=f"/products/{product_id}.json",
        )
        return data.get("product", {})

    def create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Yeni product yaradılması üçün:

          POST /products.json
          Body: {"product": {...}}
        """
        data = self._request(
            method="POST",
            path="/products.json",
            json=payload,
        )
        return data.get("product", {})

    def update_product(self, product_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mövcud product-un yenilənməsi üçün:

          PUT /products/{id}.json
          Body: {"product": {...}}
        """
        data = self._request(
            method="PUT",
            path=f"/products/{product_id}.json",
            json=payload,
        )
        return data.get("product", {})

    # -----------------------------
    # ORDERS
    # -----------------------------

    def list_orders(self, limit: int = 50, status: str = "any") -> List[Dict[str, Any]]:
        """
        Sifariş siyahısını çəkir.

        Endpoint:
          GET /orders.json?limit={limit}&status={status}
        """
        data = self._request(
            method="GET",
            path="/orders.json",
            params={"limit": limit, "status": status},
        )
        return data.get("orders", [])

    def get_order(self, order_id: int) -> Dict[str, Any]:
        """
        Tək bir sifarişi id ilə çəkir.

        Endpoint:
          GET /orders/{id}.json
        """
        data = self._request(
            method="GET",
            path=f"/orders/{order_id}.json",
        )
        return data.get("order", {})

    # -----------------------------
    # INVENTORY
    # -----------------------------

    def update_inventory_bulk(self, stock_map: Dict[str, int]) -> Dict[str, Any]:
        """
        SKU → quantity xəritəsini götürüb stokları yeniləyən bulk update skeleton.

        Diqqət:
          Shopify inventory API kifayət qədər kompleksdir (inventory_item_id, location_id və s.).
          Bu mərhələdə yalnız skeleton saxlayırıq.

        Gələcəkdə:
          - SKU → inventory_item_id map-i qurulacaq
          - /inventory_levels/adjust.json və s. endpoint-lərdən istifadə ediləcək.
        """
        raise NotImplementedError("ShopifyClient.update_inventory_bulk hələ implement olunmayıb.")

    # -----------------------------
    # COLLECTIONS
    # -----------------------------

    def list_collections(self) -> List[Dict[str, Any]]:
        """
        Kolleksiya siyahısını çəkən skeleton method.

        Gələcək implementasiya:
          GET /custom_collections.json və ya /smart_collections.json
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

        Gələcəkdə buraya real implementasiya əlavə olunacaq.
        """
        raise NotImplementedError("ShopifyClient.create_or_update_metafield hələ implement olunmayıb.")

    # -----------------------------
    # WEBHOOKS
    # -----------------------------

    def register_webhook(self, topic: str, callback_url: str) -> Dict[str, Any]:
        """
        Shopify webhook-larını qeydiyyatdan keçirmək üçün skeleton.

        Gələcəkdə buraya real implementasiya əlavə olunacaq.
        """
        raise NotImplementedError("ShopifyClient.register_webhook hələ implement olunmayıb.")

    # -----------------------------
    # HEALTHCHECK
    # -----------------------------

    def health_check(self) -> bool:
        """
        Sadə healthcheck.

        Real versiyada:
          - kiçik bir sorğu ilə API-ni yoxlamaq olar.
        Skeleton versiyada:
          - yalnız config-in doluluğunu yoxlayırıq.
        """
        return bool(self.config.store_domain and self.config.access_token)
