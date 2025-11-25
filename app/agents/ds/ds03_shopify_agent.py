import os
import json
from dataclasses import dataclass
from typing import List, Optional

import requests


# ==========================================================
#  Basic Shopify config
# ==========================================================
SHOPIFY_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "").strip()
SHOPIFY_ADMIN_ACCESS_TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "").strip()
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-01").strip()


def _ensure_config() -> None:
    if not SHOPIFY_STORE_DOMAIN or not SHOPIFY_ADMIN_ACCESS_TOKEN:
        raise RuntimeError(
            "Shopify config is missing. "
            "Check SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN env vars."
        )


def _shopify_url(path: str) -> str:
    """Build full Shopify Admin REST URL."""
    path = path.lstrip("/")
    return f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}/{path}"


def _shopify_headers() -> dict:
    return {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ==========================================================
#  Data classes
# ==========================================================
@dataclass
class ShopifyDemoProductSpec:
    title: str
    description: str
    price: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


# ==========================================================
#  Public helpers used by MSP
# ==========================================================
def test_shopify_connection() -> str:
    """
    Simple health-check: call GET /shop.json
    """
    try:
        _ensure_config()
        url = _shopify_url("shop.json")
        resp = requests.get(url, headers=_shopify_headers(), timeout=15)

        if resp.status_code != 200:
            return (
                "MSP error: Shopify connection FAILED.\n"
                f"Status: {resp.status_code}\n"
                f"Body: {resp.text[:500]}"
            )

        data = resp.json().get("shop", {})
        name = data.get("name", "(unknown)")
        domain = data.get("domain", "(unknown)")
        return (
            "✅ Shopify connection OK. Admin API is accessible.\n"
            f"Shop name: {name}\n"
            f"Domain: {domain}"
        )
    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: Shopify connection exception: {e}"


def create_demo_product(spec: ShopifyDemoProductSpec) -> str:
    """
    Create a simple demo product in Shopify.
    Called from MSP with `msp: shopify: demo`.
    """
    try:
        _ensure_config()

        payload = {
            "product": {
                "title": spec.title,
                "body_html": spec.description,
                "status": "active",
                "published": True,
                "variants": [
                    {
                        "price": spec.price,
                        "sku": "DEMO-PRODUCT",
                    }
                ],
                "tags": spec.tags or ["samarkand soul", "demo"],
            }
        }

        if spec.image_url:
            payload["product"]["images"] = [{"src": spec.image_url}]

        url = _shopify_url("products.json")
        resp = requests.post(
            url, headers=_shopify_headers(), data=json.dumps(payload), timeout=20
        )

        if resp.status_code not in (200, 201):
            return (
                "MSP error: Demo product creation failed.\n"
                f"Status: {resp.status_code}\n"
                f"Body: {resp.text[:800]}"
            )

        product = resp.json().get("product", {})
        pid = product.get("id")
        handle = product.get("handle")
        admin_url = f"/admin/products/{pid}" if pid else "unknown"
        storefront_url = f"/products/{handle}" if handle else "unknown"

        return (
            "✅ Demo product created in Shopify.\n"
            f"ID: {pid}\n"
            f"Handle: {handle}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL (if published later): {storefront_url}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: Demo product exception: {e}"


# ==========================================================
#  COMING SOON PAGE / PRODUCT
#  Trigger:  msp: shopify: comingsoon
# ==========================================================
def setup_coming_soon_page() -> str:
    """
    Creates (or reuses) a 'Coming Soon' product for Samarkand Soul.

    Goal:
      - Title: 'Samarkand Soul — Coming Soon'
      - Handle: 'samarkand-soul-coming-soon'
      - Status: active (visible in online store)
      - Price: 0 (informational product)
    """
    try:
        _ensure_config()

        title = "Samarkand Soul — Coming Soon"
        handle = "samarkand-soul-coming-soon"

        # 1) Try to find existing product by handle using REST search.
        # Shopify REST doesn't filter directly by handle, so we search by title
        # and then match handle in Python side. It is enough for our simple use-case.
        search_url = _shopify_url("products.json")
        resp = requests.get(
            search_url,
            headers=_shopify_headers(),
            params={"title": title, "limit": 50},
            timeout=20,
        )

        if resp.status_code not in (200, 201):
            # we won't fail hard, just log and continue creating a new one
            existing_product = None
        else:
            items = resp.json().get("products", [])
            existing_product = None
            for p in items:
                if p.get("handle") == handle or p.get("title") == title:
                    existing_product = p
                    break

        # 2) Build payload (used for both create & update)
        body_html = """
            <p><strong>Samarkand Soul is coming soon.</strong></p>
            <p>We are weaving the soul of Samarkand into modern home textiles:
            premium tablecloths, minimalist design, deep storytelling.</p>
            <p>Leave your email on the homepage to be the first to know when we launch.</p>
        """

        product_data = {
            "title": title,
            "body_html": body_html,
            "handle": handle,
            "status": "active",
            "published": True,
            "tags": ["coming-soon", "samarkand soul", "launch"],
            "variants": [
                {
                    "price": "0.00",
                    "sku": "COMING-SOON",
                }
            ],
        }

        # 3) Create or update
        if existing_product:
            pid = existing_product.get("id")
            update_url = _shopify_url(f"products/{pid}.json")
            payload = {"product": {"id": pid, **product_data}}
            resp2 = requests.put(
                update_url,
                headers=_shopify_headers(),
                data=json.dumps(payload),
                timeout=20,
            )

            if resp2.status_code not in (200, 201):
                return (
                    "MSP error: Coming Soon product UPDATE failed.\n"
                    f"Status: {resp2.status_code}\n"
                    f"Body: {resp2.text[:800]}"
                )

            product = resp2.json().get("product", {})
            action = "updated"
        else:
            create_url = _shopify_url("products.json")
            payload = {"product": product_data}
            resp2 = requests.post(
                create_url,
                headers=_shopify_headers(),
                data=json.dumps(payload),
                timeout=20,
            )

            if resp2.status_code not in (200, 201):
                return (
                    "MSP error: Coming Soon product CREATION failed.\n"
                    f"Status: {resp2.status_code}\n"
                    f"Body: {resp2.text[:800]}"
                )

            product = resp2.json().get("product", {})
            action = "created"

        pid = product.get("id")
        handle = product.get("handle", handle)
        admin_url = f"/admin/products/{pid}" if pid else "unknown"
        storefront_url = f"/products/{handle}" if handle else "unknown"

        return (
            f"✅ Coming Soon product {action} in Shopify.\n"
            f"ID: {pid}\n"
            f"Handle: {handle}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL: {storefront_url}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: setup_coming_soon_page exception: {e}"


# ==========================================================
#  Optional helper: create product from free-form prompt
#  Trigger: msp: shopify: add | Title | Price | OptionalImageURL
# ==========================================================
def create_product_from_prompt(raw_prompt: str) -> str:
    """
    Very lightweight helper: parse 'Title | Price | OptionalImageURL'
    and create a simple active product.
    """
    try:
        _ensure_config()

        parts = [p.strip() for p in raw_prompt.split("|")]
        if len(parts) < 2:
            return (
                "MSP error: Invalid format for 'shopify: add'.\n"
                "Use: msp: shopify: add | Title | Price | OptionalImageURL"
            )

        title = parts[0]
        price = parts[1]
        image_url = parts[2] if len(parts) > 2 and parts[2] else None

        payload = {
            "product": {
                "title": title,
                "body_html": f"<p>{title}</p>",
                "status": "active",
                "published": True,
                "variants": [{"price": price}],
            }
        }

        if image_url:
            payload["product"]["images"] = [{"src": image_url}]

        url = _shopify_url("products.json")
        resp = requests.post(
            url, headers=_shopify_headers(), data=json.dumps(payload), timeout=20
        )

        if resp.status_code not in (200, 201):
            return (
                "MSP error: Product creation failed.\n"
                f"Status: {resp.status_code}\n"
                f"Body: {resp.text[:800]}"
            )

        product = resp.json().get("product", {})
        pid = product.get("id")
        handle = product.get("handle")
        admin_url = f"/admin/products/{pid}" if pid else "unknown"
        storefront_url = f"/products/{handle}" if handle else "unknown"

        return (
            "✅ Product created in Shopify.\n"
            f"Title: {title}\n"
            f"Price: {price}\n"
            f"ID: {pid}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL: {storefront_url}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: create_product_from_prompt exception: {e}"


# ==========================================================
#  Optional: collection helper
#  Trigger: msp: shopify: collection | Collection Name
# ==========================================================
def create_collection(name: str) -> str:
    """
    Creates a manual collection with the given name.
    """
    try:
        _ensure_config()

        payload = {
            "custom_collection": {
                "title": name,
                "published": True,
            }
        }

        url = _shopify_url("custom_collections.json")
        resp = requests.post(
            url, headers=_shopify_headers(), data=json.dumps(payload), timeout=20
        )

        if resp.status_code not in (200, 201):
            return (
                "MSP error: Collection creation failed.\n"
                f"Status: {resp.status_code}\n"
                f"Body: {resp.text[:800]}"
            )

        coll = resp.json().get("custom_collection", {})
        cid = coll.get("id")
        handle = coll.get("handle")

        return (
            "✅ Collection created in Shopify.\n"
            f"Name: {name}\n"
            f"ID: {cid}\n"
            f"Handle: {handle}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: create_collection exception: {e}"
