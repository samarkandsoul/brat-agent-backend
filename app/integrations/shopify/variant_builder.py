from typing import Any, Dict, List
from app.integrations.shopify_client import ShopifyClient


class VariantBuilder:
    """
    Ölçü, rəng və s. kombinasiyalardan Shopify variant-ları yaradır.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def build_variants(self, base_product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Daxili product məlumatından variant siyahısı hazırla.
        """
        # TODO: variant generasiyası qaydalarını yaz
        raise NotImplementedError("VariantBuilder.build_variants implement olunmayıb.")

    def sync_variants(self, product_id: int, variants: List[Dict[str, Any]]) -> None:
        """
        Variant-ları Shopify-da sync et.
        """
        # TODO: Shopify variant API çağırışları
        raise NotImplementedError("VariantBuilder.sync_variants implement olunmayıb.")
