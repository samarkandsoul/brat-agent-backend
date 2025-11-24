# app/agents/ds/ds03_shopify_agent.py

from dataclasses import dataclass
from typing import Optional, List

from app.integrations.shopify_client import ShopifyAdminClient, ShopifyConfigError


@dataclass
class ShopifyDemoProductSpec:
    title: str
    description: str
    price: str = "29.90"
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


def test_shopify_connection() -> str:
    """
    Simple health check for Shopify.
    MSP can call this to verify that env and API work.
    """
    try:
        client = ShopifyAdminClient()
    except ShopifyConfigError as e:
        return f"Shopify config error: {e}"

    ok = client.ping()
    if ok:
        return "✅ Shopify connection OK. Admin API is accessible."
    return "❌ Shopify ping failed. Check logs and credentials."


def create_demo_product(spec: ShopifyDemoProductSpec) -> str:
    """
    Creates a simple demo product in Shopify.
    """
    try:
        client = ShopifyAdminClient()
    except ShopifyConfigError as e:
        return f"Shopify config error: {e}"

    data = client.create_basic_product(
        title=spec.title,
        body_html=spec.description,
        tags=spec.tags or ["samarkand soul", "demo"],
        price=spec.price,
        image_src=spec.image_url,
        status="draft",
    )

    product = data.get("product", {})
    pid = product.get("id")
    handle = product.get("handle")
    url_part = handle or pid

    return (
        "✅ Demo product created in Shopify.\n"
        f"ID: {pid}\n"
        f"Handle: {handle}\n"
        f"Admin URL: /admin/products/{pid}\n"
        f"Storefront URL (if published later): /products/{url_part}"
    )


def setup_coming_soon_page() -> str:
    """
    Creates or updates a 'coming soon' page for Samarkand Soul.
    """
    try:
        client = ShopifyAdminClient()
    except ShopifyConfigError as e:
        return f"Shopify config error: {e}"

    title = "Samarkand Soul · Coming Soon"
    body_html = """
    <div style="text-align:center; padding: 40px 20px;">
      <h1 style="font-family:serif; font-size: 32px; margin-bottom: 16px;">
        Samarkand Soul is opening soon.
      </h1>
      <p style="font-size: 18px; max-width: 600px; margin: 0 auto 16px;">
        Premium home textile inspired by the soul of Samarkand.
        We are preparing our first limited collection.
      </p>
      <p style="font-size: 16px; color: #555;">
        Follow our journey on TikTok and join the early members of Samarkand Soul.
      </p>
    </div>
    """

    client.create_or_update_coming_soon_page(title=title, body_html=body_html)
    return "✅ 'Coming Soon' page is created/updated in Shopify (handle: /pages/coming-soon)."
