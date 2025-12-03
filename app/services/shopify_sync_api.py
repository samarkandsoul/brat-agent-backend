# app/services/shopify_sync_api.py

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.integrations.shopify_client import ShopifyClient, ShopifyConfig


app = FastAPI(
    title="Brat Shopify Sync API",
    version="0.1.0",
    description="Service layer for orchestrating Shopify product & order sync.",
)


# ---------- DTO-lar (response modelləri) ---------- #


class ProductResponse(BaseModel):
    id: int
    title: str
    status: Optional[str] = None
    handle: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        extra = "allow"  # Shopify-dən gələn əlavə field-ləri də saxlasın


class OrderResponse(BaseModel):
    id: int
    name: Optional[str] = None
    financial_status: Optional[str] = None
    fulfillment_status: Optional[str] = None
    total_price: Optional[str] = None

    class Config:
        extra = "allow"


class HealthResponse(BaseModel):
    service: str
    shopify_config_ok: bool
    shop_url: Optional[str] = None
    api_version: Optional[str] = None


# ---------- Shopify klientini yığmaq üçün helper ---------- #


def _build_shopify_client() -> ShopifyClient:
    """
    ENV-dən konfiqurasiyanı götürüb ShopifyClient instansını qaytarır.

    Gözlənilən ENV-lər:
      SHOPIFY_API_KEY
      SHOPIFY_ACCESS_TOKEN
      SHOPIFY_STORE_DOMAIN
      SHOPIFY_API_VERSION (optional, default: 2024-01)
    """
    api_key = os.getenv("SHOPIFY_API_KEY", "")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
    store_domain = os.getenv("SHOPIFY_STORE_DOMAIN", "")
    api_version = os.getenv("SHOPIFY_API_VERSION", "2024-01")

    if not (access_token and store_domain):
        # Bu halda health endpoint-lə görəcəyik ki, config boşdur.
        raise RuntimeError("Shopify config is incomplete. Please check ENV variables.")

    cfg = ShopifyConfig(
        api_key=api_key,
        access_token=access_token,
        store_domain=store_domain,
        api_version=api_version,
    )
    return ShopifyClient(cfg)


# Bir dəfə yığırıq, service boyunca istifadə edirik
try:
    shopify_client: Optional[ShopifyClient] = _build_shopify_client()
except Exception:
    # ENV hələ tam deyilsə, health endpoint bunu göstərəcək
    shopify_client = None


# ---------- Health & meta endpoint-lər ---------- #


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Render monitor + backend üçün heartbeat.

    Burada həm də Shopify config-in doluluğunu yoxlayırıq.
    """
    global shopify_client  # noqa: PLW0603

    config_ok = bool(shopify_client and shopify_client.health_check())

    shop_url = None
    api_version = None
    if shopify_client is not None:
        shop_url = shopify_client.config.store_domain
        api_version = shopify_client.config.api_version

    return HealthResponse(
        service="shopify_sync",
        shopify_config_ok=config_ok,
        shop_url=shop_url,
        api_version=api_version,
    )


# ---------- Products endpoint-ləri ---------- #


@app.get("/shopify/products", response_model=List[ProductResponse])
async def list_products(limit: int = Query(20, ge=1, le=250)):
    """
    Shopify-dan məhsul siyahısını çəkir.

    Hazırda sadə pass-through edir:
      GET /products.json?limit={limit}
    """
    global shopify_client  # noqa: PLW0603

    if shopify_client is None:
        raise HTTPException(
            status_code=500,
            detail="Shopify client is not configured. Check ENV variables.",
        )

    try:
        products: List[Dict[str, Any]] = shopify_client.list_products(limit=limit)
        return products
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Shopify products error: {exc}") from exc


@app.get("/shopify/orders", response_model=List[OrderResponse])
async def list_orders(
    limit: int = Query(20, ge=1, le=250),
    status: str = Query("any"),
):
    """
    Shopify sifariş siyahısını çəkir.

    Hazırda:
      GET /orders.json?limit={limit}&status={status}
    """
    global shopify_client  # noqa: PLW0603

    if shopify_client is None:
        raise HTTPException(
            status_code=500,
            detail="Shopify client is not configured. Check ENV variables.",
        )

    try:
        orders: List[Dict[str, Any]] = shopify_client.list_orders(
            limit=limit,
            status=status,
        )
        return orders
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Shopify orders error: {exc}") from exc
