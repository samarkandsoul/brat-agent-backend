"""
Image generator skeleton.

Məqsəd:
- Məhsul + brend stilinə görə vizual brief yaratmaq
- Sonradan real image model / API ilə birləşəcək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ImagePromptInput:
    product_name: str
    product_description: str
    brand_style: str  # "minimal", "luxury", "boho", və s.
    format_ratio: str = "4:5"  # IG / TikTok üçün rahat format
    use_real_photos: bool = True


@dataclass
class ImagePromptResult:
    prompt_text: str
    negative_prompt: str
    metadata: Dict[str, Any]


class ImageGenerator:
    def build_prompt(self, cfg: ImagePromptInput) -> ImagePromptResult:
        base = (
            f"{cfg
