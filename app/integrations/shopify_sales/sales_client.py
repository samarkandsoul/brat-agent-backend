import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

# Mövcud Shopify client-dən config util-ləri istifadə edirik
from app.integrations.shopify_client import (
    _shopify_url,
    _shopify_headers,
    _ensure_config,
)


def fetch_orders_last_24h() -> List[Dict[str, Any]]:
    """
    Shopify Admin API-dən son 24 saatın orders-lərini çəkir.

    Qeyd:
    - Hazırda max 250 order çəkirik (Samarkand Soul-un ilk mərhələsi üçün kifayətdir).
    """

    _ensure_config()

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    created_at_min = since.isoformat()

    url = _shopify_url("orders.json")
    params = {
        "status": "any",
        "limit": 250,
        "created_at_min": created_at_min,
        # Bizə hazırda ancaq əsas metriklər lazımdır
        "fields": "id,created_at,total_price,current_total_price,currency,financial_status",
    }

    resp = requests.get(
        url,
        headers=_shopify_headers(),
        params=params,
        timeout=20,
    )

    if resp.status_code not in (200, 201):
        raise RuntimeError(
            f"Shopify orders API failed: {resp.status_code} {resp.text[:400]}"
        )

    data = resp.json()
    orders = data.get("orders", [])
    if not isinstance(orders, list):
        raise RuntimeError("Unexpected Shopify orders payload (orders is not a list).")

    return orders
