from typing import Dict, Any
from app.integrations.shopify_client import ShopifyClient


class SeoOptimizer:
    """
    Product üçün SEO title, description, handle və tags optimizasiyası.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def build_seo_fields(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Daxili product məlumatından SEO field-ları çıxar.
        """
        # TODO: real SEO qaydaları
        return {
            "metafields": [],
            "tags": product.get("tags", []),
        }

    def apply_seo(self, product_id: int, product: Dict[str, Any]) -> None:
        """
        SEO field-ları Shopify product-a tətbiq et.
        """
        # TODO: Shopify SEO/metafield update çağırışları
        raise NotImplementedError("SeoOptimizer.apply_seo implement olunmayıb.")
