from typing import Dict, Any
from app.integrations.shopify_client import ShopifyClient


class InventorySyncService:
    """
    Stok səviyyələrinin Shopify ↔ daxili sistem arasında sinxron saxlanması.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def pull_inventory(self) -> Dict[str, Any]:
        """
        Shopify-dan stok məlumatını çək.
        """
        # TODO: inventory API çağırışı
        raise NotImplementedError("InventorySyncService.pull_inventory implement olunmayıb.")

    def push_inventory(self, inventory: Dict[str, Any]) -> None:
        """
        Daxili stok məlumatını Shopify-a push et.
        """
        # TODO: update çağırışları
        raise NotImplementedError("InventorySyncService.push_inventory implement olunmayıb.")
