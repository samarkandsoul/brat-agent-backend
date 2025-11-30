from typing import List, Dict, Any, Tuple, Optional

from app.reports.daily_report_models import SalesMetrics
from app.integrations.shopify_sales.sales_client import fetch_orders_last_24h
from app.config.settings import settings


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:  # noqa: BLE001
        return 0.0


def build_sales_metrics_from_orders(orders: List[Dict[str, Any]]) -> SalesMetrics:
    """
    Shopify orders list-dən Samarkand Soul üçün satış metriklərini hesablayır.
    """

    total_revenue = 0.0
    currency = settings.DEFAULT_CURRENCY or "USD"

    for o in orders:
        price = (
            o.get("current_total_price")
            or o.get("total_price")
            or 0
        )
        total_revenue += _to_float(price)

        cur = o.get("currency")
        if cur:
            currency = cur

    orders_count = len(orders)
    avg_order_value = total_revenue / orders_count if orders_count else 0.0

    # Hələlik sessions/visits datamız yoxdur, ona görə CR = 0.0 saxlayırıq.
    conversion_rate = 0.0

    return SalesMetrics(
        total_revenue=round(total_revenue, 2),
        currency=currency,
        orders_count=orders_count,
        conversion_rate=conversion_rate,
        avg_order_value=round(avg_order_value, 2) if orders_count else 0.0,
        atc_rate=None,
        checkout_drop_rate=None,
    )


def get_shopify_sales_metrics_safely() -> Tuple[Optional[SalesMetrics], Optional[str]]:
    """
    Daily Report üçün təhlükəsiz wrapper:
      - Uğurlu olarsa: (SalesMetrics, None)
      - Xəta olarsa: (None, "error message...")
    """
    try:
        orders = fetch_orders_last_24h()
        metrics = build_sales_metrics_from_orders(orders)
        return metrics, None
    except Exception as e:  # noqa: BLE001
        return None, f"Shopify sales error: {e}"
