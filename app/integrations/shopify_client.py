# app/integrations/shopify_client.py

import os
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


# ==========================================================
#  Shopify CONFIG (single source of truth)
# ==========================================================
SHOPIFY_STORE_DOMAIN = os.environ.get("SHOPIFY_STORE_DOMAIN", "").strip()
SHOPIFY_ADMIN_ACCESS_TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "").strip()
SHOPIFY_API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2024-01").strip()


class ShopifyConfigError(Exception):
    """Raised when Shopify config is missing or invalid."""
    pass


def _ensure_config() -> None:
    """
    Ensure Shopify config exists.
    Used by both functional helpers and ShopifyAdminClient.
    """
    if not SHOPIFY_STORE_DOMAIN or not SHOPIFY_ADMIN_ACCESS_TOKEN:
        raise ShopifyConfigError(
            "Shopify config is missing. "
            "Check SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN env vars."
        )


def _shopify_base_url() -> str:
    return f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"


def _shopify_url(path: str) -> str:
    """Build full Shopify Admin REST URL."""
    path = path.lstrip("/")
    return f"{_shopify_base_url()}/{path}"


def _shopify_headers() -> dict:
    return {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ==========================================================
#  OPTIONAL CLASS CLIENT (for future usage)
# ==========================================================
class ShopifyAdminClient:
    """
    Minimal Shopify Admin API client.

    Uses:
      - SHOPIFY_STORE_DOMAIN
      - SHOPIFY_ADMIN_ACCESS_TOKEN

    This class is NOT required by MSP, but can be used
    in other parts of the system if needed.
    """

    def __init__(self) -> None:
        _ensure_config()
        self.base_url = _shopify_base_url()
        self.token = SHOPIFY_ADMIN_ACCESS_TOKEN

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.token,
        }

        resp = requests.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            timeout=30,
        )

        if not resp.ok:
            raise RuntimeError(
                f"Shopify API error: {resp.status_code} {resp.text}"
            )

        return resp.json()

    def ping(self) -> bool:
        """
        Simple health check: tries to list products (first page).
        Returns True if request succeeds.
        """
        try:
            _ = self._request("GET", "/products.json", params={"limit": 1})
            return True
        except Exception as e:  # pylint: disable=broad-except
            print(f"[ShopifyAdminClient] ping failed: {e}")
            return False

    def create_basic_product(
        self,
        title: str,
        body_html: str,
        tags: Optional[List[str]] = None,
        price: str = "19.99",
        status: str = "draft",
        image_src: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a minimal product in Shopify.

        NOTE:
        - By default products are created as DRAFT (not live).
        - You can manually publish them from Shopify admin.
        """
        merged_tags = (tags or []) + ["samarkand soul", "auto-generated"]

        payload: Dict[str, Any] = {
            "product": {
                "title": title,
                "body_html": body_html,
                "status": status,       # "draft" by default
                "published": False,     # never auto-publish
                "tags": ", ".join(merged_tags),
                "variants": [
                    {
                        "price": price,
                        "inventory_management": "shopify",
                        "inventory_policy": "deny",
                    }
                ],
            }
        }

        if image_src:
            payload["product"]["images"] = [{"src": image_src}]

        data = self._request("POST", "/products.json", json=payload)
        print(
            "[ShopifyAdminClient] Created product:",
            data.get("product", {}).get("id"),
        )
        return data

    def create_or_update_coming_soon_page(
        self,
        title: str,
        body_html: str,
    ) -> Dict[str, Any]:
        """
        Creates or updates a 'coming-soon' page.
        """
        pages_data = self._request("GET", "/pages.json", params={"limit": 250})
        pages = pages_data.get("pages", [])

        existing = next((p for p in pages if p.get("handle") == "coming-soon"), None)

        if existing:
            page_id = existing["id"]
            payload = {
                "page": {
                    "id": page_id,
                    "title": title,
                    "body_html": body_html,
                }
            }
            data = self._request("PUT", f"/pages/{page_id}.json", json=payload)
            print("[ShopifyAdminClient] Updated coming-soon page:", page_id)
            return data

        payload = {
            "page": {
                "title": title,
                "body_html": body_html,
                "handle": "coming-soon",
                "published": True,
            }
        }
        data = self._request("POST", "/pages.json", json=payload)
        print(
            "[ShopifyAdminClient] Created coming-soon page:",
            data.get("page", {}).get("id"),
        )
        return data

    def create_collection(
        self,
        title: str,
        body_html: str = "",
    ) -> Dict[str, Any]:
        """
        Creates a simple manual custom collection.
        """
        payload = {
            "custom_collection": {
                "title": title,
                "body_html": body_html,
                "published": True,
            }
        }

        data = self._request("POST", "/custom_collections.json", json=payload)
        print(
            "[ShopifyAdminClient] Created collection:",
            data.get("custom_collection", {}).get("id"),
        )
        return data


# ==========================================================
#  Data classes used by MSP
# ==========================================================
@dataclass
class ShopifyDemoProductSpec:
    title: str
    description: str
    price: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None


# ==========================================================
#  Public helpers used by MSP (KEEP NAMES SAME)
# ==========================================================
def test_shopify_connection() -> str:
    """
    Simple health-check: call GET /shop.json
    Used by MSP with 'msp: shopify: test'
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

    IMPORTANT:
    - Product is created as DRAFT (not visible in storefront).
    - You must manually publish it after review.
    """
    try:
        _ensure_config()

        merged_tags = (spec.tags or []) + ["samarkand soul", "demo", "auto-generated"]

        payload = {
            "product": {
                "title": spec.title,
                "body_html": spec.description,
                "status": "draft",          # do not auto-activate
                "published": False,         # not visible until you publish
                "variants": [
                    {
                        "price": spec.price,
                        "sku": "DEMO-PRODUCT",
                    }
                ],
                "tags": merged_tags,
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
            "✅ Demo product created in Shopify (DRAFT).\n"
            f"ID: {pid}\n"
            f"Handle: {handle}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL (after you publish): {storefront_url}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: Demo product exception: {e}"


def setup_coming_soon_page() -> str:
    """
    Creates (or reuses) a 'Coming Soon' product for Samarkand Soul.

    Goal:
      - Title: 'Samarkand Soul — Coming Soon'
      - Handle: 'samarkand-soul-coming-soon'
      - Status: active (informational product)
    """
    try:
        _ensure_config()

        title = "Samarkand Soul — Coming Soon"
        handle = "samarkand-soul-coming-soon"

        # 1) Try to find existing product by title, then match handle.
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
            "status": "active",          # this one can be visible
            "published": True,
            "tags": ["coming-soon", "samarkand soul"],
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


def create_product_from_prompt(raw_prompt: str) -> str:
    """
    Very lightweight helper: parse 'Title | Price | OptionalImageURL'
    and create a simple DRAFT product.

    Trigger: msp: shopify: add | Title | Price | OptionalImageURL
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
                "status": "draft",      # keep it safe
                "published": False,     # you decide when to publish
                "variants": [{"price": price}],
                "tags": ["samarkand soul", "auto-generated"],
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
            "✅ Product created in Shopify (DRAFT).\n"
            f"Title: {title}\n"
            f"Price: {price}\n"
            f"ID: {pid}\n"
            f"Admin URL: {admin_url}\n"
            f"Storefront URL (after you publish): {storefront_url}"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error: create_product_from_prompt exception: {e}"


def create_collection(name: str) -> str:
    """
    Creates a manual collection with the given name.

    Trigger: msp: shopify: collection | Collection Name
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
