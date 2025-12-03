from typing import Any, Dict, List
from app.integrations.shopify_client import ShopifyClient


class ShippingProfileManager:
    """
    Çatdırılma profilləri və dərəcələrini idarə edən service.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def ensure_shipping_profiles(self, profiles: List[Dict[str, Any]]) -> None:
        """
        Lazımi shipping profillərini yarad / yenilə.
        """
        # TODO: Shopify shipping profiles API
        raise NotImplementedError("ShippingProfileManager.ensure_shipping_profiles implement olunmayıb.")
