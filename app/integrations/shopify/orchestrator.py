"""
Shopify Orchestrator (beynə yaxın skeleton)

Məqsəd:
- Bütün Shopify ilə bağlı yüksək səviyyəli əməliyyatları tək yerdə toplamaq
- Aşağı səviyyə klient (ShopifyClient) + mapper-lər + servis-lərlə
  üst səviyyə biznes axını arasında körpü olmaq
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional

from app.integrations.shopify_client import ShopifyClient
from app.integrations.shopify.models import Product, Order
from app.integrations.shopify.product_mapper import ProductMapper
from app.integrations.shopify.order_mapper import OrderMapper
from app.integrations.shopify.inventory_sync_service import InventorySyncService, InventorySyncResult
from app.integrations.shopify.pricing_rules_engine import (
    PricingRulesEngine,
    PricingSuggestionBatch,
)


class ShopifyOrchestrator:
    """
    Brat sistemində "Shopify ilə danışan general".

    Hazırda edə bildikləri:
      - Məhsulları çəkir (client → ProductMapper → Product modeli)
      - Product modelindən çıxış edib Shopify product yaratmaq / yeniləmək
      - Sifarişləri çəkib Order modelinə map etmək
      - Daxili stock xəritəsindən çıxış edib inventory sync üçün skeleton axın
      - Məhsullar üçün qiymət təklifləri hesablamaq üçün PricingRulesEngine istifadə etmək
    """

    def __init__(
        self,
        client: ShopifyClient,
        product_mapper: Optional[ProductMapper] = None,
        order_mapper: Optional[OrderMapper] = None,
        inventory_sync_service: Optional[InventorySyncService] = None,
        pricing_rules_engine: Optional[PricingRulesEngine] = None,
    ) -> None:
        self.client = client
        self.product_mapper = product_mapper or ProductMapper()
        self.order_mapper = order_mapper or OrderMapper()
        self.inventory_sync_service = inventory_sync_service or InventorySyncService(client)
        self.pricing_rules_engine = pricing_rules_engine or PricingRulesEngine()

    # -----------------------------
    # PRODUCT AXINI
    # -----------------------------

    def fetch_products(self, limit: int = 50) -> List[Product]:
        """
        Shopify-dan məhsulları çəkib Product modelinə map edir.
        """
        raw_products: List[Dict[str, Any]] = self.client.list_products(limit=limit)
        products: List[Product] = self.product_mapper.raw_list_to_products(raw_products)
        return products

    def upsert_product(self, product: Product) -> Dict[str, Any]:
        """
        Daxili Product modelindən çıxış edib Shopify product yaradır / yeniləyir.
        """
        payload = self.product_mapper.product_to_payload(product)

        if product.id is None:
            # YENİ məhsul yarat
            result = self.client.create_product(payload)
        else:
            # MÖVCUD məhsulu yenilə
            result = self.client.update_product(product.id, payload)

        return result

    # -----------------------------
    # ORDER AXINI
    # -----------------------------

    def fetch_recent_orders(self, limit: int = 50, status: str = "any") -> List[Order]:
        """
        Shopify-dan son sifarişləri çəkib Order modelinə map edir.
        """
        raw_orders: List[Dict[str, Any]] = self.client.list_orders(limit=limit, status=status)
        orders: List[Order] = self.order_mapper.raw_list_to_orders(raw_orders)
        return orders

    def sync_orders_to_internal(self) -> int:
        """
        Son sifarişləri çəkib daxili sistemə yazan end-to-end axın.

        TODO:
          - fetch_recent_orders
          - daxili DB/analytics servisinə yaz
        """
        # Hələlik sadəcə heç nə etmir və 0 qaytarır
        return 0

    # -----------------------------
    # INVENTORY AXINI
    # -----------------------------

    def sync_inventory_from_internal(self, stock_map: Dict[str, int]) -> Dict[str, Any]:
        """
        SKU → qalıq sayı xəritəsindən çıxış edib Shopify-də stokları yeniləyir.

        stock_map nümunə:
          {
            "SKU-123": 10,
            "SKU-456": 0,
          }
        """
        result: InventorySyncResult = self.inventory_sync_service.sync_from_stock_map(stock_map)

        return {
            "attempted": result.attempted,
            "success": result.success,
            "failed": result.failed,
            "raw_response": result.raw_response,
        }

    # -----------------------------
    # PRICE AXINI
    # -----------------------------

    def recalculate_prices_for_products(
        self,
        product_ids: Optional[list] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Məhsullar üçün qiyməti qaydalara əsasən yenidən hesablayır.

        Hazır skeleton mərhələsində:
          - product_ids istifadə olunmur, sadəcə fetch_products(limit) çağırılır.
          - PricingRulesEngine sadə təkliflər qaytarır.
        Gələcəkdə:
          - product_ids filter
          - cost məlumatı ilə real marja hesablaması
          - təkliflərin Shopify-a tətbiqi (upsert_product)
        """
        # Hazırda product_ids ignored – skeleton mərhələsidir
        products: List[Product] = self.fetch_products(limit=limit)
        batches: List[PricingSuggestionBatch] = self.pricing_rules_engine.suggest_for_products(products)

        # Sadə qaytarılacaq struktur – gələcəkdə daha detallı ola bilər
        response_products: List[Dict[str, Any]] = []

        for batch in batches:
            product_info = {
                "product_id": batch.product_id,
                "handle": batch.handle,
                "suggestions": [],
            }
            for s in batch.suggestions:
                product_info["suggestions"].append(
                    {
                        "sku": s.sku,
                        "old_price": s.old_price.amount,
                        "old_currency": s.old_price.currency,
                        "suggested_price": s.suggested_price.amount,
                        "suggested_currency": s.suggested_price.currency,
                        "reason": s.reason,
                    }
                )
            response_products.append(product_info)

        return {
            "total_products": len(response_products),
            "products": response_products,
            "note": "Skeleton pricing suggestions only, not applied to Shopify yet.",
      }
