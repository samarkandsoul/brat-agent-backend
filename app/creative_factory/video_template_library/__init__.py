"""
Video template library skeleton.

Məqsəd:
- Fərqli TikTok / IG / FB video şablonlarını mərkəzlə toplamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class VideoTemplateSpec:
    name: str
    platform: str         # "tiktok", "instagram", "facebook"
    duration_sec: int
    structure: List[str]  # ["hook", "problem", "solution", "cta"] kimi


class VideoTemplateLibrary:
    def __init__(self) -> None:
        self._templates: Dict[str, VideoTemplateSpec] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register(
            VideoTemplateSpec(
                name="before_after_transformation",
                platform="tiktok",
                duration_sec=25,
                structure=["hook", "before", "transition", "after", "cta"],
            )
        )
        self.register(
            VideoTemplateSpec(
                name="ritual_morning_coffee",
                platform="instagram",
                duration_sec=30,
                structure=["hook", "setup", "closeups", "text_overlay", "cta"],
            )
        )

    def register(self, spec: VideoTemplateSpec) -> None:
        self._templates[spec.name] = spec

    def get(self, name: str) -> VideoTemplateSpec:
        return self._templates[name]

    def list_for_platform(self, platform: str) -> List[VideoTemplateSpec]:
        return [t for t in self._templates.values() if t.platform == platform]
