"""
Instagram reel generator skeleton.

Məqsəd:
- TikTok creative pipeline ilə oxşar, amma IG üçün optimallaşmış reel brifləri
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ReelIdea:
    hook: str
    scenes: List[str]
    cta: str


class InstagramReelGenerator:
    def generate_reel_idea(self, product_name: str, main_benefit: str) -> ReelIdea:
        """
        Sadə text brif – video factory sonradan bunu istifadə edəcək.
        """
        hook = f"{product_name} ilə {main_benefit}? Gəlin 5 saniyəyə göstərim."
        scenes = [
            "1) Problem momenti (qısa, real həyat)",
            "2) Məhsulun istifadə anı",
            "3) Nəticə / əvvəl-sonra",
        ]
        cta = "Daha çox misal üçün profilə keç 💫"
        return ReelIdea(hook=hook, scenes=scenes, cta=cta)
