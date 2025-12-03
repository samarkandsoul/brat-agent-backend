"""
Animation engine skeleton.

Məqsəd:
- Sadə animasiya preset-lərinin (pan, zoom, parallax və s.) planını çıxarmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AnimationStep:
    type: str           # "zoom_in", "pan_left", "fade_in" və s.
    start_time: float   # saniyə
    end_time: float     # saniyə
    intensity: float = 1.0


@dataclass
class AnimationPlan:
    duration_sec: float
    steps: List[AnimationStep]


class AnimationEngine:
    def build_plan_for_product_showcase(self, duration_sec: float = 20.0) -> AnimationPlan:
        steps: List[AnimationStep] = [
            AnimationStep(type="fade_in", start_time=0.0, end_time=1.0, intensity=1.0),
            AnimationStep(type="slow_zoom_in", start_time=1.0, end_time=8.0, intensity=0.6),
            AnimationStep(type="pan_right", start_time=8.0, end_time=12.0, intensity=0.5),
            AnimationStep(type="zoom_out", start_time=12.0, end_time=18.0, intensity=0.7),
            AnimationStep(type="fade_out", start_time=18.0, end_time=duration_sec, intensity=1.0),
        ]
        return AnimationPlan(duration_sec=duration_sec, steps=steps)

    def to_timeline_dict(self, plan: AnimationPlan) -> Dict[str, List[Dict[str, float]]]:
        """
        Sadə serializasiya – başqa servislər rahat oxusun deyə.
        """
        return {
            "duration_sec": plan.duration_sec,
            "steps": [
                {
                    "type": s.type,
                    "start": s.start_time,
                    "end": s.end_time,
                    "intensity": s.intensity,
                }
                for s in plan.steps
            ],
      }
