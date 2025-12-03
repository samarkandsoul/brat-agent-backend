from typing import Any, Dict, List
from app.integrations.shopify_client import ShopifyClient


class MetafieldManager:
    """
    Shopify metafield-lərini (material, texniki info, daxili tag-lar və s.) idarə edir.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def build_metafields(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Daxili product məlumatını metafield-lərə çevir.
        """
        # TODO: metafield mapping qaydalarını yaz
        raise NotImplementedError("MetafieldManager.build_metafields implement olunmayıb.")

    def sync_metafields(self, product_id: int, metafields: List[Dict[str, Any]]) -> None:
        """
        Verilən product üçün metafield-ləri Shopify-a göndər.
        """
        # TODO: Shopify metafield API
        raise NotImplementedError("MetafieldManager.sync_metafields implement olunmayıb.")
