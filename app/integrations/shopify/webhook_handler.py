from typing import Any, Dict


class WebhookHandler:
    """
    Shopify webhook-larını (order created, product updated və s.) emal edən layer.
    """

    def handle_event(self, topic: str, payload: Dict[str, Any]) -> None:
        """
        Render/backend tərəfindən çağırılacaq əsas giriş nöqtəsi.
        """
        # TODO: topic-ə görə route et: orders/create, orders/fulfilled və s.
        raise NotImplementedError("WebhookHandler.handle_event implement olunmayıb.")
