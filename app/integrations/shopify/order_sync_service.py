from typing import Any, Dict, List
from app.integrations.shopify_client import ShopifyClient


class OrderSyncService:
    """
    Shopify sifarişlərini Brat sisteminə sync edən servis.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def fetch_recent_orders(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Son N sifarişi Shopify-dan çək.
        """
        # TODO: Shopify orders API istifadə et
        raise NotImplementedError("OrderSyncService.fetch_recent_orders implement olunmayıb.")

    def sync_orders_to_internal(self, orders: List[Dict[str, Any]]) -> None:
        """
        Çəkilən sifarişləri daxili DB / analitika sisteminə yaz.
        """
        # TODO: daxili storage layer ilə inteqrasiya
        raise NotImplementedError("OrderSyncService.sync_orders_to_internal implement olunmayıb.")
