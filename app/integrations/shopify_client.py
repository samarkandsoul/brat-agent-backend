# app/integrations/shopify_client.py

import os
import requests
from typing import Any, Dict, List, Optional


class ShopifyConfigError(Exception):
    """Raised when Shopify config is missing or invalid."""
    pass


class ShopifyAdminClient:
    """
    Minimal Shopify Admin API client.

    Uses:
      - SHOPIFY_STORE_URL
      - SHOPIFY_ADMIN_TOKEN

    Make sure these are set in Render environment.
    """

    def __init__(self) -> None:
        store_url = os.environ.get("SHOPIFY_STORE_URL")
        token = os.environ.get("SHOPIFY_ADMIN_TOKEN")

        if not store_url or not token:
            raise ShopifyConfigError(
                "SHOPIFY_STORE_URL or SHOPIFY_ADMIN_TOKEN is missing in env."
            )

        # normalize store url
        if not store_url.startswith("http"):
            store_url = f"https://{store_url}"

        # use a stable API version
        api_version = "2024-01"

        self.base_url = f"{store_url}/admin/api/{api_version}"
        self.token = token

    # ====== low-level request helper ======

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

    # ====== high-level helpers ======

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

        - title: product title
        - body_html: product description (HTML)
        - tags: list of tags
        - price: string, e.g. "29.90"
        - status: "draft" or "active"
        - image_src: optional image URL
        """
        payload: Dict[str, Any] = {
            "product": {
                "title": title,
                "body_html": body_html,
                "status": status,
                "tags": ", ".join(tags or []),
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
        print("[ShopifyAdminClient] Created product:", data.get("product", {}).get("id"))
        return data

    def create_or_update_coming_soon_page(
        self,
        title: str,
        body_html: str,
    ) -> Dict[str, Any]:
        """
        Creates or updates a 'coming-soon' page.

        Later we can link this from theme or navigation.
        """
        # 1) try to find existing page by handle
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

        # 2) create new page
        payload = {
            "page": {
                "title": title,
                "body_html": body_html,
                "handle": "coming-soon",
                "published": True,
            }
        }
        data = self._request("POST", "/pages.json", json=payload)
        print("[ShopifyAdminClient] Created coming-soon page:", data.get("page", {}).get("id"))
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
