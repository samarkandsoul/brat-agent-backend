from typing import List
from app.integrations.shopify_client import ShopifyClient


class MediaUploader:
    """
    Product şəkillərini və media fayllarını Shopify-a yükləyən modul.
    """

    def __init__(self, client: ShopifyClient) -> None:
        self.client = client

    def upload_product_images(self, product_id: int, image_urls: List[str]) -> None:
        """
        Verilən product üçün şəkil siyahısını yüklə.
        """
        # TODO: Shopify image API call-ları
        raise NotImplementedError("MediaUploader.upload_product_images implement olunmayıb.")
