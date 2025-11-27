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
    except Exception as e:
        return f"MSP error: Shopify connection exception: {e}"


def create_demo_product(spec: ShopifyDemoProductSpec) -> str:
    """Create a simple demo product in Shopify."""
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
            f"Storefront URL: {storefront_url}"
        )

    except Exception as e:
        return f"MSP error: Demo product exception: {e}"


# ==========================================================
#  COMING SOON PAGE / PRODUCT
# ==========================================================
def setup_coming_soon_page() -> str:
    """Creates or updates the 'Coming Soon' product."""
    try:
        _ensure_config()

        title = "Samarkand Soul — Coming Soon"
        handle = "samarkand-soul-coming-soon"

        search_url = _shopify_url("products.json")
        resp = requests.get(
            search_url,
            headers=_shopify_headers(),
            params={"title": title, "limit": 50},
            timeout=20,
        )

        existing_product = None
        if resp.status_code in (200, 201):
            items = resp.json().get("products", [])
            for p in items:
                if p.get("handle") == handle or p.get("title") == title:
                    existing_product = p
                    break

        body_html = """
            <p><strong>Samarkand Soul is coming soon.</strong></p>
            <p>Premium handmade home textiles inspired by Samarkand.</p>
            <p>Leave your email to be the first to know.</p>
        """

        product_data = {
            "title": title,
            "body_html": body_html,
            "handle": handle,
            "status": "active",
            "published": True,
            "tags": ["coming-soon", "samarkand soul", "launch"],
            "variants": [{"price": "0.00", "sku": "COMING-SOON"}],
        }

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
            action = "updated"
            if resp2.status_code not in (200, 201):
                return (
                    "MSP error: Coming Soon UPDATE failed.\n"
                    f"Status: {resp2.status_code}\n"
                    f"Body: {resp2.text[:800]}"
                )
            product = resp2.json().get("product", {})

        else:
            create_url = _shopify_url("products.json")
            payload = {"product": product_data}
            resp2 = requests.post(
                create_url,
                headers=_shopify_headers(),
                data=json.dumps(payload),
                timeout=20,
            )
            action = "created"
            if resp2.status_code not in (200, 201):
                return (
                    "MSP error: Coming Soon CREATION failed.\n"
                    f"Status: {resp2.status_code}\n"
                    f"Body: {resp2.text[:800]}"
                )
            product = resp2.json().get("product", {})

        pid = product.get("id")
        storefront_url = f"/products/{handle}"

        return (
            f"✅ Coming Soon product {action}.\n"
            f"ID: {pid}\n"
            f"Storefront URL: {storefront_url}"
        )

    except Exception as e:
        return f"MSP error: setup_coming_soon_page exception: {e}"


# ==========================================================
#  PRODUCT CREATION FROM PROMPT
# ==========================================================
def create_product_from_prompt(raw_prompt: str) -> str:
    """Parse: Title | Price | OptionalImageURL"""
    try:
        _ensure_config()

        parts = [p.strip() for p in raw_prompt.split("|")]
        if len(parts) < 2:
            return (
                "MSP error: Invalid format.\n"
                "Use: msp: shopify: add | Title | Price | OptionalImageURL"
            )

        title, price = parts[0], parts[1]
        image_url = parts[2] if len(parts) > 2 else None

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

        return (
            "✅ Product created.\n"
            f"ID: {pid}\n"
            f"Handle: {handle}"
        )

    except Exception as e:
        return f"MSP error: create_product_from_prompt exception: {e}"


# ==========================================================
#  COLLECTION CREATION
# ==========================================================
def create_collection(name: str) -> str:
    """Creates a manual collection."""
    try:
        _ensure_config()

        payload = {"custom_collection": {"title": name, "published": True}}
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
        return f"✅ Collection created: {coll.get('title')} (ID: {coll.get('id')})"

    except Exception as e:
        return f"MSP error: create_collection exception: {e}"


# ==========================================================
#  SAMARKAND SOUL DEMO STORE BOOTSTRAP
# ==========================================================
def _find_collection_by_title(title: str) -> Optional[dict]:
    _ensure_config()
    url = _shopify_url("custom_collections.json")
    resp = requests.get(
        url,
        headers=_shopify_headers(),
        params={"title": title, "limit": 50},
        timeout=20,
    )
    if resp.status_code not in (200, 201):
        return None

    items = resp.json().get("custom_collections", [])
    for coll in items:
        if coll.get("title") == title:
            return coll
    return None


def _create_or_get_collection_id(title: str) -> Optional[int]:
    try:
        existing = _find_collection_by_title(title)
        if existing:
            return existing.get("id")

        payload = {"custom_collection": {"title": title, "published": True}}
        url = _shopify_url("custom_collections.json")
        resp = requests.post(
            url,
            headers=_shopify_headers(),
            data=json.dumps(payload),
            timeout=20,
        )
        if resp.status_code not in (200, 201):
            return None

        coll = resp.json().get("custom_collection", {})
        return coll.get("id")

    except Exception:
        return None


def _create_simple_product(title: str, price: str, body_html: str, tags=None):
    try:
        _ensure_config()
        payload = {
            "product": {
                "title": title,
                "body_html": body_html,
                "status": "active",
                "published": True,
                "variants": [{"price": price}],
                "tags": tags or ["samarkand soul", "demo"],
            }
        }
        url = _shopify_url("products.json")
        resp = requests.post(
            url, headers=_shopify_headers(), data=json.dumps(payload), timeout=20
        )
        if resp.status_code not in (200, 201):
            return None
        return resp.json().get("product", {})
    except Exception:
        return None


def _attach_product_to_collection(product_id: int, collection_id: int) -> bool:
    try:
        _ensure_config()
        payload = {
            "collect": {
                "product_id": product_id,
                "collection_id": collection_id,
            }
        }
        url = _shopify_url("collects.json")
        resp = requests.post(
            url, headers=_shopify_headers(), data=json.dumps(payload), timeout=20
        )
        return resp.status_code in (200, 201)
    except Exception:
        return False


def bootstrap_samarkand_demo_store() -> str:
    try:
        _ensure_config()

        collection_title = "Samarkand Soul Tablecloths"
        collection_id = _create_or_get_collection_id(collection_title)

        if not collection_id:
            return f"MSP error: Could not create/find '{collection_title}'."

        demo_specs = [
            {
                "title": "Samarkand Soul Demo Tablecloth",
                "price": "39.90",
                "body": "<p>Demo tablecloth used for store layout testing.</p>",
            },
            {
                "title": "Samarkand Soul Test Product",
                "price": "39.90",
                "body": "<p>Internal test product.</p>",
            },
            {
                "title": "Samarkand Soul™ Ikat Tablecloth — Ritual of the Table",
                "price": "39.90",
                "body": "<p>Signature Ikat concept.</p>",
            },
        ]

        list_url = _shopify_url("products.json")
        resp_list = requests.get(
            list_url,
            headers=_shopify_headers(),
            params={"limit": 250},
            timeout=20,
        )

        existing_by_title = {}
        if resp_list.status_code in (200, 201):
            for p in resp_list.json().get("products", []):
                existing_by_title[p.get("title", "").strip()] = p

        created_products = []

        for spec in demo_specs:
            title = spec["title"]

            if title in existing_by_title:
                product = existing_by_title[title]
            else:
                product = _create_simple_product(
                    title=title,
                    price=spec["price"],
                    body_html=spec["body"],
                    tags=["samarkand soul", "demo"],
                )
                if not product:
                    continue

            pid = product.get("id")
            if pid:
                _attach_product_to_collection(pid, collection_id)
                created_products.append(f"- {title} (ID: {pid})")

        result = [
            "✅ Samarkand Soul demo store bootstrap completed.",
            f"Main collection ID: {collection_id}",
        ]

        if created_products:
            result.append("Products:")
            result.extend(created_products)
        else:
            result.append("Warning: No products were created or attached.")

        return "\n".join(result)

    except Exception as e:
        return f"MSP error: bootstrap_samarkand_demo_store exception: {e}"
