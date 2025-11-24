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


def create_product_from_prompt(raw: str) -> str:
    """
    Parse a simple text prompt and create a product.

    Expected format:
      TITLE | PRICE | OPTIONAL_IMAGE_URL

    Example:
      Samarkand Soul Ivory Tablecloth | 49.90 | https://image-url.jpg
    """
    raw = (raw or "").strip()
    if not raw:
        return (
            "Shopify add usage:\n"
            "  msp: shopify: add | Title | Price | OptionalImageURL\n"
        )

    parts = [p.strip() for p in raw.split("|")]
    if len(parts) < 2:
        return (
            "Shopify add error: I need at least Title and Price.\n"
            "Nümunə:\n"
            "  msp: shopify: add | Samarkand Soul Ivory Tablecloth | 49.90"
        )

    title = parts[0]
    price = parts[1]
    image_url = parts[2] if len(parts) > 2 else None

    description = (
        "<p>Premium Samarkand Soul tablecloth.</p>"
        "<p>Inspired by the soul of Samarkand, crafted for modern homes.</p>"
    )

    spec = ShopifyDemoProductSpec(
        title=title,
        description=description,
        price=price,
        tags=["samarkand soul", "tablecloth"],
        image_url=image_url,
    )
    return create_demo_product(spec)


def create_collection(name: str) -> str:
    """
    Create a simple manual collection for Samarkand Soul.
    """
    name = (name or "").strip()
    if not name:
        return (
            "Shopify collection usage:\n"
            "  msp: shopify: collection | Premium Tablecloths"
        )

    try:
        client = ShopifyAdminClient()
    except ShopifyConfigError as e:
        return f"Shopify config error: {e}"

    body_html = (
        f"<p>Curated Samarkand Soul collection: {name}."
        "</p><p>Premium home textile pieces for modern interiors.</p>"
    )
    data = client.create_collection(title=name, body_html=body_html)
    cid = data.get("custom_collection", {}).get("id")
    handle = data.get("custom_collection", {}).get("handle")

    return (
        "✅ Collection created in Shopify.\n"
        f"ID: {cid}\n"
        f"Handle: {handle}\n"
        f"Admin URL: /admin/collections/{cid}"
    )
