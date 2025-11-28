# app/agents/ds/ds03_shopify_agent.py

"""
DS-03 — Shopify Agent

High-level orchestrator for all Shopify operations.
HTTP və Shopify Admin API ilə birbaşa işləri
`app/integrations/shopify_client.py` faylı görür,
bu agent isə MSP/Agent Brain tərəfdən sadə komandalar alır.

Bu agentdən istifadə edən əsas komandalar (MSP üçün):
  - shopify.test
  - shopify.demo_product
  - shopify.coming_soon
  - shopify.add_product_from_prompt
  - shopify.create_collection
  - shopify.setup_basic_structure
  - shopify.update_page
"""

from __future__ import annotations

from typing import Optional

# ✅ DÜZGÜN IMPORT – artıq `app.integrations` paketindən gəlir
from ...integrations import shopify_client


# ==========================================================
#  PUBLIC COMMAND WRAPPERS (used by MSP / Agent Brain)
# ==========================================================


def cmd_test_connection() -> str:
    """
    DS-03: Check Shopify connection health.
    """
    return shopify_client.test_shopify_connection()


def cmd_create_demo_product() -> str:
    """
    DS-03: Create a standard demo product for layout testing.

    Bu funksiya daxilində sabit bir demo məhsul spesifikasiyası istifadə olunur,
    yəni Telegram-dan əlavə parametrlər göndərməyə ehtiyac yoxdur.
    """
    spec = shopify_client.ShopifyDemoProductSpec(
        title="Samarkand Soul Demo Tablecloth",
        description=(
            "<p>Internal demo product for Samarkand Soul store layout testing. "
            "Not for real customers.</p>"
        ),
        price="39.90",
        tags=["samarkand soul", "demo", "internal"],
        image_url=None,
    )
    return shopify_client.create_demo_product(spec)


def cmd_setup_coming_soon() -> str:
    """
    DS-03: Create or update 'Samarkand Soul — Coming Soon' product.
    """
    # integration modulunda həm köhnə, həm yeni ad yoxlanır
    if hasattr(shopify_client, "setup_coming_soon_product"):
        return shopify_client.setup_coming_soon_product()
    if hasattr(shopify_client, "setup_coming_soon_page"):
        return shopify_client.setup_coming_soon_page()
    return (
        "MSP error (DS-03): No 'setup_coming_soon_*' function found in shopify_client."
    )


def cmd_create_product_from_prompt(raw_prompt: str) -> str:
    """
    DS-03: Create product from a raw prompt.

    Format (MSP tərəfi üçün):
      'Title | Price | OptionalImageURL'
    """
    return shopify_client.create_product_from_prompt(raw_prompt)


def cmd_create_collection(name: str) -> str:
    """
    DS-03: Create a manual collection with given name.
    """
    return shopify_client.create_collection(name)


def cmd_setup_basic_store_structure() -> str:
    """
    DS-03: Create/Update basic static pages for the store.

    Requires that `shopify_client.setup_basic_store_structure()` exists.
    """
    if not hasattr(shopify_client, "setup_basic_store_structure"):
        return (
            "MSP error (DS-03): 'setup_basic_store_structure' is not defined "
            "in shopify_client. Please update integration module."
        )
    return shopify_client.setup_basic_store_structure()


def cmd_update_page(handle: str, body_html: str) -> str:
    """
    DS-03: Overwrite a single Shopify page's HTML by handle.

    Example handle values:
      - 'privacy-policy'
      - 'terms-of-service'
      - 'shipping-and-returns'
      - 'about-samarkand-soul'
      - 'contact'
    """
    if not hasattr(shopify_client, "overwrite_page_html"):
        return (
            "MSP error (DS-03): 'overwrite_page_html' is not defined "
            "in shopify_client. Please update integration module."
        )
    return shopify_client.overwrite_page_html(handle=handle, body_html=body_html)


# ==========================================================
#  GENERIC DISPATCHER FOR MSP
# ==========================================================

def handle_shopify_command(action: str, payload: Optional[str] = None) -> str:
    """
    High-level dispatcher that MSP/Telegram komandalari üçün istifadə oluna bilər.

    Expected `action` values:
      - 'test'
      - 'demo'
      - 'comingsoon'
      - 'add'
      - 'collection'
      - 'structure_basic'
      - 'update_page'

    `payload` formatları:
      - action == 'add':
          payload -> 'Title | Price | OptionalImageURL'
      - action == 'collection':
          payload -> 'Collection Name'
      - action == 'update_page':
          payload -> 'handle | BODY_HTML'
    """
    act = (action or "").strip().lower()

    try:
        if act == "test":
            return cmd_test_connection()

        if act == "demo":
            return cmd_create_demo_product()

        if act == "comingsoon":
            return cmd_setup_coming_soon()

        if act == "add":
            if not payload:
                return (
                    "MSP error (DS-03): Missing payload for 'add'.\n"
                    "Expected: Title | Price | OptionalImageURL"
                )
            return cmd_create_product_from_prompt(payload)

        if act == "collection":
            name = (payload or "").strip()
            if not name:
                return (
                    "MSP error (DS-03): Missing collection name.\n"
                    "Use format: msp: shopify: collection | Name"
                )
            return cmd_create_collection(name)

        if act == "structure_basic":
            return cmd_setup_basic_store_structure()

        if act == "update_page":
            if not payload:
                return (
                    "MSP error (DS-03): Missing payload for 'update_page'.\n"
                    "Use: msp: shopify: update_page | handle | BODY_HTML"
                )
            parts = [p.strip() for p in payload.split("|", 1)]
            if len(parts) < 2:
                return (
                    "MSP error (DS-03): Invalid payload for 'update_page'.\n"
                    "Use: msp: shopify: update_page | handle | BODY_HTML"
                )
            handle, body_html = parts[0], parts[1]
            return cmd_update_page(handle, body_html)

        # Unknown action
        return (
            "MSP error (DS-03): Unknown Shopify action.\n"
            "Supported actions: test, demo, comingsoon, add, "
            "collection, structure_basic, update_page"
        )

    except Exception as e:  # pylint: disable=broad-except
        return f"MSP error (DS-03): unhandled exception: {e}"
