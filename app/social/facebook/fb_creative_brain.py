"""
Facebook creative brain skeleton.

Məqsəd:
- Primary text, headline, description üçün variantlar
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class FBCreativeContext:
    product_name: str
    main_benefit: str
    objection: str
    language: str = "az"


class FacebookCreativeBrain:
    def generate_primary_text(self, ctx: FBCreativeContext) -> str:
        return f"{ctx.product_name} ilə {ctx.main_benefit}. {ctx.objection} problemini rahat həll et!"

    def generate_headline(self, ctx: FBCreativeContext) -> str:
        return f"{ctx.product_name} – gündəlik lüks"

    def generate_description(self, ctx: FBCreativeContext) -> str:
        return "Sayı məhduddur, indi sifariş et."

    def generate_all(self, ctx: FBCreativeContext) -> List[str]:
        return [
            self.generate_primary_text(ctx),
            self.generate_headline(ctx),
            self.generate_description(ctx),
      ]
