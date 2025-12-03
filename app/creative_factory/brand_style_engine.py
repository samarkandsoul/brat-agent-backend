"""
Brand style engine skeleton.

Məqsəd:
- Brend üçün konsistent stil qaydalarını mərkəzləşdirmək
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BrandStyleProfile:
    name: str
    color_palette: Dict[str, str]  # primary / secondary / accent hex
    typography: Dict[str, str]     # heading / body font adları
    tone_of_voice: str             # "calm", "playful", "luxury"
    visual_keywords: str           # "minimal, natural light, cozy" və s.


class BrandStyleEngine:
    def __init__(self, default_profile: BrandStyleProfile):
        self._profiles: Dict[str, BrandStyleProfile] = {
            default_profile.name: default_profile
        }
        self._active = default_profile.name

    def register_profile(self, profile: BrandStyleProfile) -> None:
        self._profiles[profile.name] = profile

    def set_active_profile(self, name: str) -> None:
        if name not in self._profiles:
            raise ValueError(f"Unknown brand style profile: {name}")
        self._active = name

    @property
    def active_profile(self) -> BrandStyleProfile:
        return self._profiles[self._active]

    def to_prompt_fragments(self) -> Dict[str, Any]:
        """
        Creative agent-lər üçün müxtəlif prompt parçalarını çıxarır.
        """
        p = self.active_profile
        return {
            "colors": f"Color palette: {p.color_palette}",
            "typography": f"Fonts: {p.typography}",
            "tone": f"Tone of voice: {p.tone_of_voice}",
            "visuals": f"Visual keywords: {p.visual_keywords}",
      }
