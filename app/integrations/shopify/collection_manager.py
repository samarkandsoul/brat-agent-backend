from typing import List
from app.integrations.shopify_client import ShopifyClient


class CollectionManager:
    """
    Shopify kolleksiyalarını idarə edən servis.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def ensure_collections(self, names: List[str]) -> None:
        """
        Lazımi kolleksiyalar mövcud deyilsə yaradılmalıdır.
        """
        # TODO: mövcud kolleksiyaları çək + yarad/vahidləşdir
        raise NotImplementedError("CollectionManager.ensure_collections implement olunmayıb.")

    def assign_product_to_collections(self, product_id: int, collection_ids: List[int]) -> None:
        """
        Product-u verilən kolleksiyalara əlavə et.
        """
        # TODO: kolleksiya-şop ilişkiləri
        raise NotImplementedError(
            "CollectionManager.assign_product_to_collections implement olunmayıb."
      )
