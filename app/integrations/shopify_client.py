# app/integrations/shopify_client.py

import os
import json
from dataclasses import dataclass
from typing import List, Optional

import requests


# ==========================================================
#  BASIC SHOPIFY CONFIG
# ==========================================================

SHOPIFY_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "").strip()
SHOPIFY_ADMIN_ACCESS_TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "").strip()
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-01").strip()


def _ensure_config() -> None:
    """
    Ensures Shopify env vars are present.

    Required:
      - SHOPIFY_STORE_DOMAIN  (e.g. samarkand-soul.myshopify.com)
      - SHOPIFY_ADMIN_ACCESS_TOKEN  (Admin API access token)
    """
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
#  DATA CLASSES
# ==========================================================

@dataclass
class ShopifyDemoProductSpec:
    title: str
    description: str
    price: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


# ==========================================================
#  HEALTH CHECK  (msp: shopify: test)
# ==========================================================

def test_shopify_connection() -> str:
    """
    Simple health-check: GET /shop.json

    Telegram:
      msp: shopify: test
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


# ==========================================================
#  DEMO PRODUCT  (msp: shopify: demo)
# ==========================================================

def create_demo_product(spec: ShopifyDemoProductSpec) -> str:
    """
    Create a simple demo product in Shopify.

    Telegram:
      msp: shopify: demo
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

    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: Demo product exception: {e}"


# ==========================================================
#  COMING SOON PRODUCT  (msp: shopify: comingsoon)
# ==========================================================

def setup_coming_soon_product() -> str:
    """
    Creates or updates a 'Samarkand Soul — Coming Soon' product.

    Telegram:
      msp: shopify: comingsoon
    """
    try:
        _ensure_config()

        title = "Samarkand Soul — Coming Soon"
        handle = "samarkand-soul-coming-soon"

        # Try to find existing product by title/handle
        search_url = _shopify_url("products.json")
        resp = requests.get(
            search_url,
            headers=_shopify_headers(),
            params={"title": title, "limit": 50},
            timeout=20,
        )

        if resp.status_code not in (200, 201):
            existing_product = None
        else:
            items = resp.json().get("products", [])
            existing_product = None
            for p in items:
                if p.get("handle") == handle or p.get("title") == title:
                    existing_product = p
                    break

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

        # Update existing
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

    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: setup_coming_soon_product exception: {e}"


# Backwards-compat: old name
def setup_coming_soon_page() -> str:
    """
    Backwards-compatible wrapper for older DS code.
    """
    return setup_coming_soon_product()


# ==========================================================
#  PRODUCT FROM PROMPT  (msp: shopify: add | ...)
# ==========================================================

def create_product_from_prompt(raw_prompt: str) -> str:
    """
    Parse 'Title | Price | OptionalImageURL' and create a simple product.

    IMPORTANT:
      • Products are created as DRAFT with tag 'NEEDS_APPROVAL'.
      • They are NOT published to Online Store automatically.

    Telegram:
      msp: shopify: add | Samarkand Soul Ikat Tablecloth | 79.90 | https://...
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
                # Agent-created products must be manually approved by Zahid.
                "status": "draft",
                "published": False,
                "variants": [{"price": price}],
                "tags": ["samarkand soul", "ds-auto", "NEEDS_APPROVAL"],
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
            "✅ Product CREATED as DRAFT in Shopify.\n"
            "Status: draft (NEEDS_MANUAL_APPROVAL)\n"
            f"Title: {title}\n"
            f"Price: {price}\n"
            f"ID: {pid}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL (after publish): {storefront_url}"
        )

    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: create_product_from_prompt exception: {e}"


# ==========================================================
#  COLLECTION  (msp: shopify: collection | Name)
# ==========================================================

def create_collection(name: str) -> str:
    """
    Creates a manual collection.

    Telegram:
      msp: shopify: collection | Samarkand Soul Tablecloths
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

    except Exception as e:  # pylint: disable-broad-except
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
    """
    Helper to quickly create a demo collection + products
    for layout / testing purposes.
    """
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

    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: bootstrap_samarkand_demo_store exception: {e}"


# ==========================================================
#  BASIC STORE STRUCTURE  (msp: shopify: structure_basic)
# ==========================================================

def _create_or_update_page(title: str, handle: str, body_html: str) -> str:
    """
    Internal helper to create or update a Shopify Page by handle.
    """
    url_list = _shopify_url("pages.json")
    resp = requests.get(
        url_list,
        headers=_shopify_headers(),
        params={"limit": 250},
        timeout=20,
    )

    if resp.status_code not in (200, 201):
        raise RuntimeError(
            f"Page list failed: {resp.status_code} {resp.text[:400]}"
        )

    pages = resp.json().get("pages", [])
    existing = next((p for p in pages if p.get("handle") == handle), None)

    if existing:
        page_id = existing["id"]
        update_url = _shopify_url(f"pages/{page_id}.json")
        payload = {"page": {"id": page_id, "title": title, "body_html": body_html}}
        resp2 = requests.put(
            update_url,
            headers=_shopify_headers(),
            data=json.dumps(payload),
            timeout=20,
        )
        if resp2.status_code not in (200, 201):
            raise RuntimeError(
                f"Page update failed: {resp2.status_code} {resp2.text[:400]}"
            )
        return f"updated: {handle}"
    else:
        create_url = _shopify_url("pages.json")
        payload = {
            "page": {
                "title": title,
                "handle": handle,
                "body_html": body_html,
                "published": True,
            }
        }
        resp2 = requests.post(
            create_url,
            headers=_shopify_headers(),
            data=json.dumps(payload),
            timeout=20,
        )
        if resp2.status_code not in (200, 201):
            raise RuntimeError(
                f"Page create failed: {resp2.status_code} {resp2.text[:400]}"
            )
        return f"created: {handle}"


def setup_basic_store_structure() -> str:
    """
    Creates/updates core pages for Samarkand Soul brand.

    Telegram:
      msp: shopify: structure_basic

    Daxildə:
      - About Samarkand Soul
      - Shipping & Returns
      - Privacy Policy
      - Terms of Service
      - Contact
    """
    try:
        _ensure_config()

        changes: List[str] = []

        about_body = """
<h2>About Samarkand Soul</h2>
<p>Samarkand Soul weaves the soul of history into modern home rituals.
Premium tablecloths, calm luxury aesthetics and honest storytelling.</p>
"""
        changes.append(
            _create_or_update_page(
                title="About Samarkand Soul",
                handle="about-samarkand-soul",
                body_html=about_body,
            )
        )

        shipping_body = """
<h2>Shipping & Returns</h2>
<p>We ship worldwide from our trusted partners. Standard processing time
is 2–5 business days. For detailed shipping zones and return rules,
please see the policy on this page or contact our support.</p>
"""
        changes.append(
            _create_or_update_page(
                title="Shipping & Returns",
                handle="shipping-and-returns",
                body_html=shipping_body,
            )
        )

        privacy_body = """
<h2>Privacy Policy</h2>
<p>We respect your privacy. We only use your data to process orders and
improve your experience. We never sell personal data to third parties.</p>
"""
        changes.append(
            _create_or_update_page(
                title="Privacy Policy",
                handle="privacy-policy",
                body_html=privacy_body,
            )
        )

        terms_body = """
<h2>Terms of Service</h2>
<p>By using our store, you agree to our terms of service. Please review
this page for details about orders, payments and limitations.</p>
"""
        changes.append(
            _create_or_update_page(
                title="Terms of Service",
                handle="terms-of-service",
                body_html=terms_body,
            )
        )

        contact_body = """
<h2>Contact</h2>
<p>If you have any questions about Samarkand Soul, your order or our
products, you can reach us via email or the contact form on this page.</p>
"""
        changes.append(
            _create_or_update_page(
                title="Contact",
                handle="contact",
                body_html=contact_body,
            )
        )

        return (
            "✅ Basic Samarkand Soul store structure created/updated.\n"
            "Pages:\n- " + "\n- ".join(changes)
        )

    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: setup_basic_store_structure exception: {e}"


# ==========================================================
#  AUTODS STUBS (FUTURE INTEGRATION)
# ==========================================================

def autods_search_stub(niche: str) -> str:
    """
    Placeholder for AutoDS product search.
    """
    return (
        "[ESCALATION]\n"
        "Reason: AutoDS API is not integrated yet.\n"
        "Action: Configure AutoDS API (endpoint + token) in backend.\n"
        "Summary: Once AutoDS API is available, MSP can auto-search products "
        f"for niche: {niche}"
    )


# ==========================================================
#  SINGLE PAGE UPDATE (used by: msp: shopify: update_page | handle | BODY_HTML)
# ==========================================================

_PAGE_TITLE_MAP = {
    "privacy-policy": "Privacy Policy",
    "terms-of-service": "Terms of Service",
    "shipping-and-returns": "Shipping & Returns",
    "about-samarkand-soul": "About Samarkand Soul",
    "contact": "Contact",
}


def overwrite_page_html(handle: str, body_html: str, title: Optional[str] = None) -> str:
    """
    Overwrite or create a single Shopify Page by handle.

    Used by MSP bridge:
      msp: shopify: update_page | privacy-policy | <HTML or generated text>

    MSP tərəfi GPT ilə HTML generasiya edib bura ötürür.
    """
    try:
        _ensure_config()
        h = (handle or "").strip().lower()
        if not h:
            return "MSP error: overwrite_page_html: handle is empty."

        page_title = title or _PAGE_TITLE_MAP.get(h) or h.replace("-", " ").title()

        result = _create_or_update_page(
            title=page_title,
            handle=h,
            body_html=body_html,
        )

        return (
            "✅ Page updated in Shopify.\n"
            f"Handle: {h}\n"
            f"Title: {page_title}\n"
            f"Result: {result}"
        )
    except Exception as e:  # pylint: disable-broad-except
        return f"MSP error: overwrite_page_html exception: {e}"
