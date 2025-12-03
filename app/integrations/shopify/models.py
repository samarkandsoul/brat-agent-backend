"""
Shopify domain modelləri (skeleton).

Məqsəd:
- Bütün Shopify ilə bağlı dataları vahid modellərdən keçirmək
- Orchestrator, agentlər və servis-lər eyni "dildə" danışsın
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict


# -------------------------
# Əsas köməkçi modellər
# -------------------------


@dataclass
class Money:
    amount: float
    currency: str = "USD"


@dataclass
class Image:
    src: str
    alt: Optional[str] = None


# -------------------------
# Product / Variant modelləri
# -------------------------


@dataclass
class Variant:
    sku: str
    price: Money
    title: Optional[str] = None
    available: Optional[int] = None  # stok sayı
    options: Dict[str, str] = field(default_factory=dict)  # {"Size": "M", "Color": "Black"}


@dataclass
class Product:
    id: Optional[int]
    title: str
    description: str
    handle: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    images: List[Image] = field(default_factory=list)
    variants: List[Variant] = field(default_factory=list)
    collections: List[str] = field(default_factory=list)  # kolleksiya adları və ya id-ləri


# -------------------------
# Order modelləri
# -------------------------


@dataclass
class Address:
    first_name: str
    last_name: str
    address1: str
    city: str
    country: str
    zip: str
    phone: Optional[str] = None


@dataclass
class Customer:
    id: Optional[int]
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class LineItem:
    product_id: Optional[int]
    variant_id: Optional[int]
    sku: Optional[str]
    quantity: int
    price: Money
    title: Optional[str] = None


@dataclass
class Order:
    id: Optional[int]
    name: str  # "#1001" kimi
    customer: Optional[Customer]
    items: List[LineItem]
    subtotal_price: Money
    total_price: Money
    currency: str
    financial_status: str  # "paid", "pending" və s.
    fulfillment_status: Optional[str]  # "fulfilled", "unfulfilled" və s.
    shipping_address: Optional[Address] = None
    billing_address: Optional[Address] = None
    raw_payload: Dict = field(default_factory=dict)  # istəsən tam Shopify JSON-u da saxlayırsan
