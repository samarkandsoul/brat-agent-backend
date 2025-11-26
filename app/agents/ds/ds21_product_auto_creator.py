# app/agents/ds/ds21_product_auto_creator.py

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.llm.brat_gpt import brat_gpt_chat


@dataclass
class ProductIdea:
    """Structured product idea coming from MSP / Zahid Brat."""
    title_seed: str
    style_brief: str = ""
    price_hint: str = ""
    extra_info: str = ""


@dataclass
class ProductPlan:
    """
    Final structured plan returned by DS-21.

    Not all fields are currently pushed into Shopify (DS-03),
    but they are all useful for manual refinement + future automation.
    """
    title: str
    subtitle: str
    description_html: str
    bullet_points: str
    tags: str
    metafields: str
    collection: str
    seo_title: str
    seo_description: str
    price: str
    image_prompt: str
    raw_json: Dict[str, Any]


class ProductAutoCreator:
    """
    DS-21 — Product Auto Creator

    Mission:
      Take a rough product idea from Zahid Brat,
      use MAMOS-aware Brat GPT to design a full product concept,
      then call the DS-03 Shopify Agent to actually create
      a product record (title + price) in Shopify.

    Current version:
      • Uses LLM to generate a rich product plan (title, copy, tags, etc.).
      • Sends a minimal "Title | Price | OptionalImageURL" string
        to DS-03 `create_product_from_prompt`.
      • Returns a human-readable summary for Telegram,
        plus the raw JSON data in case we want to log or store it.
    """

    def __init__(self) -> None:
        # Lazy import here to avoid circular imports on module load
        try:
            from app.agents.ds.ds03_shopify_agent import create_product_from_prompt
        except Exception:  # pylint: disable=broad-except
            create_product_from_prompt = None  # type: ignore[assignment]

        self._create_product_from_prompt = create_product_from_prompt

    # =========================
    #  PUBLIC API
    # =========================
    def create_full_product(self, idea: ProductIdea) -> str:
        """
        High-level orchestrator.

        1) Ask Brat GPT (MAMOS-aware) to build a JSON product plan.
        2) Parse JSON safely into ProductPlan.
        3) Call DS-03 Shopify Agent to create a basic product.
        4) Return a clean summary text for Telegram.
        """
        llm_json = self._ask_llm_for_plan(idea)
        plan = self._parse_plan(llm_json)

        shopify_result = self._create_shopify_product(plan)

        # Build final summary for Telegram
        summary_lines = [
            "MSP / DS21 — PRODUCT-AUTO-CREATOR reply:",
            "",
            "Title:",
            f"{plan.title}",
            "",
            "Subtitle:",
            f"{plan.subtitle}",
            "",
            "Price:",
            plan.price or "(no price provided by LLM)",
            "",
            "Main Description (HTML-ready):",
            plan.description_html,
            "",
            "Key Bullets (can be used in sections):",
            plan.bullet_points,
            "",
            "Suggested Tags:",
            plan.tags,
            "",
            "Suggested Metafields (Color / Shape / Fabric etc.):",
            plan.metafields,
            "",
            "Suggested Collection:",
            plan.collection,
            "",
            "SEO Title:",
            plan.seo_title,
            "",
            "SEO Description:",
            plan.seo_description,
            "",
            "Image Prompt (for future AI visuals):",
            plan.image_prompt,
            "",
            "Shopify agent result:",
            shopify_result,
        ]

        return "\n".join(summary_lines)

    # =========================
    #  STEP 1 — LLM product plan
    # =========================
    def _ask_llm_for_plan(self, idea: ProductIdea) -> str:
        """
        Ask Brat GPT (with MAMOS doctrine) to return a JSON product plan.

        We explicitly ask for **pure JSON** with a fixed schema.
        """
        user_prompt = f"""
You are DS-21 Product Auto Creator inside the Samarkand Soul ecosystem.

Your job:
  • Take the rough product idea below.
  • Design a PREMIUM Samarkand Soul product concept.
  • Return ONLY valid JSON. No markdown, no explanation, no comments.

JSON SCHEMA (all values MUST be strings):

{{
  "title": "...",
  "subtitle": "...",
  "description_html": "...",        // 2–4 short paragraphs, HTML <p> tags
  "bullet_points": "...",           // bullet list in markdown or plain text
  "tags": "...",                    // comma-separated tags
  "metafields": "...",              // suggestions for Color, Shape, Fabric etc.
  "collection": "...",              // e.g. "Premium Tablecloths"
  "seo_title": "...",
  "seo_description": "...",
  "price": "...",                   // final price as a string, e.g. "39.90"
  "image_prompt": "..."             // prompt for future AI product images
}}

Rough product idea from Zahid Brat:

Title seed: {idea.title_seed}
Style / story: {idea.style_brief}
Price hint: {idea.price_hint}
Extra info: {idea.extra_info}

Rules:
  • Obey the Samarkand Soul MAMOS doctrine (premium, calm, honest, story-driven).
  • Keep everything focused on an ikat-style premium tablecloth line.
  • Respond ONLY with raw JSON that matches the schema.
"""
        return brat_gpt_chat(
            user_prompt=user_prompt,
            agent_role="DS-21 Product Auto Creator",
            model="gpt-4o-mini",
            temperature=0.6,
        )

    # =========================
    #  STEP 2 — Parse JSON safely
    # =========================
    def _parse_plan(self, llm_json: str) -> ProductPlan:
        """
        Convert the JSON string from LLM into a ProductPlan.
        If parsing fails, fall back to a very simple plan.
        """
        data: Dict[str, Any] = {}

        if llm_json:
            # Try to extract JSON even if the model wrapped it in text
            text = llm_json.strip()
            try:
                # If the text contains extra words, grab the first {...} block
                if not text.startswith("{"):
                    start = text.find("{")
                    end = text.rfind("}")
                    if start != -1 and end != -1 and end > start:
                        text = text[start : end + 1]

                data = json.loads(text)
            except Exception:
                data = {}

        def get(key: str, default: str = "") -> str:
            val = data.get(key, default)
            return str(val) if val is not None else default

        # Build ProductPlan with graceful fallbacks
        title = get("title", "Samarkand Soul Ikat Tablecloth")
        subtitle = get("subtitle", "Ritual of the Table")
        price = get("price", "")

        return ProductPlan(
            title=title,
            subtitle=subtitle,
            description_html=get(
                "description_html",
                "<p>Premium Samarkand Soul ikat tablecloth, bringing the spirit of history into your modern home.</p>",
            ),
            bullet_points=get(
                "bullet_points",
                "- Premium Uzbek ikat fabric\n- Warm, minimalist design\n- Perfect for daily rituals and special dinners",
            ),
            tags=get(
                "tags",
                "samarkand soul, ikat, tablecloth, handmade, premium textile, home decor",
            ),
            metafields=get(
                "metafields",
                "Color: e.g. warm sand / deep blue; Shape: rectangular; Fabric: cotton ikat",
            ),
            collection=get("collection", "Premium Tablecloths"),
            seo_title=get("seo_title", f"{title} — Samarkand Soul"),
            seo_description=get(
                "seo_description",
                "A premium ikat tablecloth from Samarkand Soul, weaving the soul of history into your modern table.",
            ),
            price=price,
            image_prompt=get(
                "image_prompt",
                "minimalist product shot of a premium Uzbek ikat tablecloth on a wooden table in warm natural light",
            ),
            raw_json=data,
        )

    # =========================
    #  STEP 3 — Shopify bridge
    # =========================
    def _create_shopify_product(self, plan: ProductPlan) -> str:
        """
        Call DS-03 Shopify Agent (if available) to create a minimal product.

        Because DS-03 currently exposes only `create_product_from_prompt`
        with the format "Title | Price | OptionalImageURL",
        we respect that contract and let DS-03 handle the rest.

        Later we can extend this to also push description, SEO, metafields, etc.
        """
        if self._create_product_from_prompt is None:
            return (
                "Shopify integration not available (DS-03 create_product_from_prompt "
                "could not be imported). Product was NOT created in Shopify."
            )

        # Build the prompt string expected by DS-03
        title = plan.title
        price = plan.price or "39.90"
        # For now we do not send an image URL (future: AI-generated assets)
        prompt_str = f"{title} | {price} | "

        try:
            result = self._create_product_from_prompt(prompt_str)  # type: ignore[misc]
            return str(result)
        except Exception as e:  # pylint: disable=broad-except
            return f"Shopify product creation failed: {e}"
