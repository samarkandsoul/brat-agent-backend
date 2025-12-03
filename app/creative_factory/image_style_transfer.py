"""
Image style transfer skeleton.

Məqsəd:
- Mövcud məhsul şəkillərinə brend stilini "overlay" etmək üçün config hazırlamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class StyleTransferConfig:
    input_image_url: str
    brand_style: str
    intensity: float = 0.7  # 0–1 arası


@dataclass
class StyleTransferPlan:
    input_image_url: str
    operations: Dict[str, Any]


class ImageStyleTransferPlanner:
    def build_plan(self, cfg: StyleTransferConfig) -> StyleTransferPlan:
        ops: Dict[str, Any] = {
            "color_grading": "neutral",
            "grain": "none",
            "vignette": False,
            "intensity": cfg.intensity,
        }

        style = cfg.brand_style.lower()
        if "boho" in style:
            ops["color_grading"] = "warm_soft"
            ops["grain"] = "light"
        elif "luxury" in style:
            ops["color_grading"] = "rich_contrast"
            ops["vignette"] = True
        elif "minimal" in style:
            ops["color_grading"] = "clean_neutral"

        return StyleTransferPlan(
            input_image_url=cfg.input_image_url,
            operations=ops,
      )
