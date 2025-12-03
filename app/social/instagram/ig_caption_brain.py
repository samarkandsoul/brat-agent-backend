"""
Instagram caption brain skeleton.

Məqsəd:
- Verilən input brifə görə caption variantları generasiya etmək
- Hashtag engine ilə birlikdə işləmək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class CaptionContext:
    product_name: str
    main_benefit: str
    brand_tone: str  # "playful", "luxury", "minimalist" və s.
    language: str = "az"


class InstagramCaptionBrain:
    def generate_hook(self, ctx: CaptionContext) -> str:
        """
        İlk cümlə – scroll-u dayandıran hook.
        """
        # TODO: real LLM prompt inteqrasiyası
        return f"{ctx.product_name} ilə {ctx.main_benefit} keşf et!"

    def generate_body(self, ctx: CaptionContext) -> str:
        """
        Məhsulun faydalarını izah edən əsas hissə.
        """
        # TODO: real LLM prompt inteqrasiyası
        return f"{ctx.brand_tone} üslubunda qısa izah (stub)."

    def generate_cta(self, ctx: CaptionContext) -> str:
        """
        Call-to-action hissəsi.
        """
        return "Link bio-da • Sifariş üçün DM yaz 😊"

    def generate_full_caption(self, ctx: CaptionContext) -> str:
        """
        Tam caption generator – hook + body + CTA.
        """
        parts: List[str] = [
            self.generate_hook(ctx),
            "",
            self.generate_body(ctx),
            "",
            self.generate_cta(ctx),
        ]
        return "\n".join(parts)
