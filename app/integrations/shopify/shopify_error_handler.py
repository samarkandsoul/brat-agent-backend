from typing import Any
import logging

logger = logging.getLogger(__name__)


class ShopifyErrorHandler:
    """
    Shopify API xətalarını mərkəzləşdirilmiş şəkildə map edən helper.
    """

    def handle_error(self, error: Any) -> None:
        """
        Shopify-dan gələn error obyektini log et və lazım gəlsə
        xüsusi exception tipinə çevir.
        """
        # TODO: status kodlarına görə fərqli davranışlar
        logger.error("Shopify error: %r", error)
        # Hazırda sadəcə log edir, gələcəkdə retry / alert əlavə oluna bilər.
