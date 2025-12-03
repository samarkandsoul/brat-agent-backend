"""
Transitions lab skeleton.

Məqsəd:
- Kadrlar arası keçid preset-lərini saxlamaq (cut, fade, whip, match cut və s.)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class TransitionPreset:
    name: str          # "hard_cut", "soft_fade", "whip_pan" və s.
    duration_sec: float
    use_case: str      # "hook", "scene_change", "before_after"


class TransitionsLab:
    def default_presets(self) -> List[TransitionPreset]:
        return [
            TransitionPreset(name="hard_cut", duration_sec=0.0, use_case="fast_hook"),
            TransitionPreset(name="soft_fade", duration_sec=0.6, use_case="scene_change"),
            TransitionPreset(name="before_after_swipe", duration_sec=0.4, use_case="before_after"),
            TransitionPreset(name="whip_pan", duration_sec=0.3, use_case="dynamic_movement"),
        ]

    def pick_for_before_after(self) -> TransitionPreset:
        for preset in self.default_presets():
            if preset.use_case == "before_after":
                return preset
        return self.default_presets()[0]
