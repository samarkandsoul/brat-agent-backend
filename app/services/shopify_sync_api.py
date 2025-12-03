"""
Shopify Sync Service API (skeleton)

This service exposes a small HTTP API for:
- Fetching products
- Fetching recent orders
- Running pricing suggestions
- Syncing inventory from an internal stock map

Intended to be deployed as a separate Render service (brat-shopify-sync).
"""

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.integrations.shopify_client import ShopifyClient, ShopifyConfig
from app.integrations.shopify.orchestrator import ShopifyOrchestrator
from app.integrations.shopify.models import Product, Order


# -----------------------------
# Pydantic request models
# -----------------------------


class InventoryItem(BaseModel):
    sku: str
    quantity: int


class InventorySyncRequest(BaseModel):
    items: List[InventoryItem]


class RecalculatePricesRequest(BaseModel):
    product_ids: Optional[List[int]] = None
    limit: int = 50


# -----------------------------
# Orchestrator factory
# -----------------------------


def create_shopify_orchestrator() -> ShopifyOrchestrator:
    """
    Create a ShopifyOrchestrator instance using ENV configuration.
    """
    cfg = ShopifyConfig(
        api_key=os.getenv("SHOPIFY_API_KEY", ""),
        access_token=os.getenv("SHOPIFY_ACCESS_TOKEN", ""),
        store_domain=os.getenv("SHOPIFY_STORE_DOMAIN", ""),
        api_version=os.getenv("SHOPIFY_API_VERSION", "2024-01"),
    )

    if not cfg.access_token or not cfg.store_domain:
        # We still create the client, but healthcheck will fail.
        # This prevents hard crashes at import time.
        pass

    client = ShopifyClient(config=cfg)
    return ShopifyOrchestrator(client=client)


app = FastAPI(title="Brat Shopify Sync Service")

shopify_orch = create_shopify_orchestrator()


# -----------------------------
# Health endpoint
# -----------------------------


@app.get("/health")
def health() -> Dict[str, Any]:
    """
    Basic healthcheck for Render and monitor service.
    """
    shopify_ok = False
    try:
        shopify_ok = shopify_orch.client.health_check()
    except Exception:
        shopify_ok = False

    status = "ok" if shopify_ok else "degraded"

    return {
        "status": status,
        "shopify_ok": shopify_ok,
    }


# -----------------------------
# Products endpoints
# -----------------------------


@app.get("/shopify/products")
def list_products(limit: int = 20) -> Dict[str, Any]:
    """
    Fetch products from Shopify and return them as dictionaries.

    WARNING:
      This is primarily for debugging / monitoring.
      In production, you may want summarised views instead.
    """
    try:
        products: List[Product] = shopify_orch.fetch_products(limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "count": len(products),
        "products": [asdict(p) for p in products],
    }


# -----------------------------
# Orders endpoints
# -----------------------------


@app.get("/shopify/orders")
def list_orders(limit: int = 20, status: str = "any") -> Dict[str, Any]:
    """
    Fetch recent orders from Shopify.
    """
    try:
        orders: List[Order] = shopify_orch.fetch_recent_orders(limit=limit, status=status)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "count": len(orders),
        "orders": [asdict(o) for o in orders],
    }


# -----------------------------
# Pricing endpoints
# -----------------------------


@app.post("/shopify/recalculate-prices")
def recalculate_prices(payload: RecalculatePricesRequest) -> Dict[str, Any]:
    """
    Run pricing suggestion flow.

    Note:
      Currently this only returns suggestions and does NOT apply them
      back to Shopify. That will be a future step.
    """
    try:
        result = shopify_orch.recalculate_prices_for_products(
            product_ids=payload.product_ids,
            limit=payload.limit,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return result


# -----------------------------
# Inventory endpoints
# -----------------------------


@app.post("/shopify/sync-inventory")
def sync_inventory(payload: InventorySyncRequest) -> Dict[str, Any]:
    """
    Sync internal stock map (sku -> quantity) to Shopify.

    This expects a simple JSON body, e.g.:

      {
        "items": [
          {"sku": "SKU-123", "quantity": 10},
          {"sku": "SKU-456", "quantity": 0}
        ]
      }
    """
    stock_map: Dict[str, int] = {item.sku: item.quantity for item in payload.items}

    try:
        result = shopify_orch.sync_inventory_from_internal(stock_map=stock_map)
    except NotImplementedError as exc:
        # Inventory bulk update is not implemented yet in ShopifyClient
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return result
