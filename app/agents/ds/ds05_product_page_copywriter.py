# app/agents/ds/ds05_product_page_copywriter.py

from dataclasses import dataclass
from typing import Optional

from app.agents.core.agent_brain import AgentBrain


@dataclass
class ProductPageCopySpec:
    product_name: str
    niche: Optional[str] = None
    target_customer: Optional[str] = None
    main_benefit: Optional[str] = None
    extra_notes: Optional[str] = None


# Unified brain for DS-05
brain = AgentBrain(
    agent_code="ds05",
    agent_label="PRODUCT-PAGE-COPYWRITER",
    default_model="gpt-4o-mini",
    default_temperature=0.55,
)


def _build_prompt(spec: ProductPageCopySpec) -> str:
    lines = [f"Product name: {spec.product_name}"]
    if spec.niche:
        lines.append(f"Niche / category: {spec.niche}")
    if spec.target_customer:
        lines.append(f"Target customer: {spec.target_customer}")
    if spec.main_benefit:
        lines.append(f"Main benefit to highlight: {spec.main_benefit}")
    if spec.extra_notes:
        lines.append(f"Extra notes from Zahid Brat: {spec.extra_notes}")

    context_block = "\n".join(lines)

    return f"""
You are writing a Shopify product page for the official Samarkand Soul store.

Write copy that:
- feels premium, calm, soulful and sincere
- protects the brand image (no cheap marketing promises)
- focuses on texture, feeling, story and use cases
- is short enough for a real product page (not an essay)

Structure:

1) Short title line (not product name, but a poetic line)
2) 2–3 sentence main description paragraph
3) Bullet list:
   - key material / quality points
   - emotional / lifestyle benefits
4) One short closing line about Samarkand Soul brand feeling.

Here is the product briefing:

{context_block}

Write the text in the same language as the user prompt.
Do NOT invent fake certifications, guarantees or discounts.
""".strip()


def generate_product_page_copy_from_text(raw_body: str) -> str:
    """
    Helper used by MSP.

    Expected format:
        Product name | Niche | Target customer | Main benefit | Extra notes

    Only the first field (product name) is required.
    """
    parts = [p.strip() for p in raw_body.split("|")]
    while len(parts) < 5:
        parts.append("")

    spec = ProductPageCopySpec(
        product_name=parts[0],
        niche=parts[1] or None,
        target_customer=parts[2] or None,
        main_benefit=parts[3] or None,
        extra_notes=parts[4] or None,
    )

    prompt = _build_prompt(spec)
    reply = brain.ask(user_prompt=prompt)

    return reply
