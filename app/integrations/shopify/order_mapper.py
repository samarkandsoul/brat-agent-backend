"""
Order Mapper

Məqsəd:
- Shopify-dan gələn xam order JSON-un
  bizim `Order` modelinə map olunması
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.integrations.shopify.models import (
    Money,
    Address,
    Customer,
    LineItem,
    Order,
)


class OrderMapper:
    """
    Brat sistemi ilə Shopify sifarişləri arasında "tərcüməçi".

    İstiqamət:
    - raw Shopify JSON -> Order dataclass
    """

    def _parse_money(self, value: Optional[str], currency: str) -> Money:
        if value is None:
            return Money(amount=0.0, currency=currency)
        try:
            amount = float(value)
        except ValueError:
            amount = 0.0
        return Money(amount=amount, currency=currency)

    def _parse_address(self, raw: Optional[Dict[str, Any]]) -> Optional[Address]:
        if not raw:
            return None
        return Address(
            first_name=raw.get("first_name", ""),
            last_name=raw.get("last_name", ""),
            address1=raw.get("address1", ""),
            city=raw.get("city", ""),
            country=raw.get("country", ""),
            zip=raw.get("zip", ""),
            phone=raw.get("phone"),
        )

    def _parse_customer(self, raw: Optional[Dict[str, Any]]) -> Optional[Customer]:
        if not raw:
            return None
        return Customer(
            id=raw.get("id"),
            email=raw.get("email", ""),
            first_name=raw.get("first_name"),
            last_name=raw.get("last_name"),
        )

    def _parse_line_items(self, raw_items: List[Dict[str, Any]], currency: str) -> List[LineItem]:
        items: List[LineItem] = []
        for item in raw_items:
            price = self._parse_money(item.get("price"), currency)
            items.append(
                LineItem(
                    product_id=item.get("product_id"),
                    variant_id=item.get("variant_id"),
                    sku=item.get("sku"),
                    quantity=int(item.get("quantity", 0)),
                    price=price,
                    title=item.get("title"),
                )
            )
        return items

    def raw_to_order(self, raw: Dict[str, Any]) -> Order:
        """
        Shopify order JSON → Order modeli.

        Gözlənilən əsas sahələr:
          - id, name, customer, line_items, subtotal_price,
            total_price, currency, financial_status, fulfillment_status,
            shipping_address, billing_address
        """
        currency = raw.get("currency") or raw.get("presentment_currency") or "USD"

        subtotal = self._parse_money(raw.get("subtotal_price"), currency)
        total = self._parse_money(raw.get("total_price"), currency)

        customer = self._parse_customer(raw.get("customer"))
        shipping_address = self._parse_address(raw.get("shipping_address"))
        billing_address = self._parse_address(raw.get("billing_address"))

        items = self._parse_line_items(raw.get("line_items", []), currency)

        return Order(
            id=raw.get("id"),
            name=raw.get("name", ""),
            customer=customer,
            items=items,
            subtotal_price=subtotal,
            total_price=total,
            currency=currency,
            financial_status=raw.get("financial_status", ""),
            fulfillment_status=raw.get("fulfillment_status"),
            shipping_address=shipping_address,
            billing_address=billing_address,
            raw_payload=raw,
        )

    def raw_list_to_orders(self, rows: List[Dict[str, Any]]) -> List[Order]:
        """
        Bir neçə xam order JSON → Order list.
        """
        return [self.raw_to_order(row) for row in rows]
