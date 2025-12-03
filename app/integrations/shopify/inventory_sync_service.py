"""
Inventory Sync Service

Məqsəd:
- Daxili stok xəritəsindən (SKU -> quantity) çıxış edib
  Shopify-də stokları yeniləmək üçün yüksək səviyyə servis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from app.integrations.shopify_client import ShopifyClient


@dataclass
class InventorySyncResult:
    attempted: int
    success: int
    failed: int
    raw_response: Dict[str, Any]


class InventorySyncService:
    """
    Inventory sinxronizasiyası üçün skeleton servis.

    Axın:
      1) Daxili sistemdən SKU -> quantity xəritəsi gəlir
      2) ShopifyClient.update_inventory_bulk(...) çağırılır
      3) Nəticə InventorySyncResult formatına salınır
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def sync_from_stock_map(self, stock_map: Dict[str, int]) -> InventorySyncResult:
        """
        SKU → quantity xəritəsini götürür və ShopifyClient-ə ötürür.

        Gələcəkdə:
          - Nəticəyə görə hansı SKU-lar uğurlu, hansılar uğursuz loglanacaq
        """
        # ShopifyClient hələ NotImplementedError atır, bu normaldır –
        # arxitektura səviyyəsində skeleton qururuq.
        raw = self.client.update_inventory_bulk(stock_map)

        attempted = len(stock_map)
        # Skeleton-da hamısını success kimi qəbul edirik – real versiyada raw cavaba baxacağıq.
        success = attempted
        failed = 0

        return InventorySyncResult(
            attempted=attempted,
            success=success,
            failed=failed,
            raw_response=raw,
        )
