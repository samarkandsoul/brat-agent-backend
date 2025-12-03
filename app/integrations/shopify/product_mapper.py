from typing import Any, Dict
from app.integrations.shopify_client import ShopifyClient


class ProductMapper:
    """
    Brat daxili product modelini Shopify product strukturuna map edən servis.

    TODO:
      - Daxili product schema-nı dəqiqləşdir
      - Shopify API üçün lazımi field-ları map et
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def to_shopify_payload(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Daxili product dict -> Shopify product payload
        """
        # TODO: real mapping
        payload: Dict[str, Any] = {
            "title": product.get("title"),
            "body_html": product.get("description"),
            "status": product.get("status", "active"),
        }
        return payload

    def upsert_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mövcudsa update, yoxdursa create.
        """
        payload = self.to_shopify_payload(product)
        # TODO: burada client.create_or_update_product istifadə et
        raise NotImplementedError("Product upsert hələ implement olunmayıb.")
