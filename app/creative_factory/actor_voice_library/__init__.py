"""
Actor & voice profile library skeleton.

Məqsəd:
- Voiceover / UGC üçün personaj profillərini saxlamaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ActorVoiceProfile:
    name: str
    gender: str
    age_range: str           # "20-30", "30-40" və s.
    energy_level: str        # "calm", "high", "warm"
    accent: str              # "Azeri", "Neutral English", və s.
    description: str


class ActorVoiceLibrary:
    def __init__(self) -> None:
        self._profiles: Dict[str, ActorVoiceProfile] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.add_profile(
            ActorVoiceProfile(
                name="calm_host",
                gender="female",
                age_range="25-35",
                energy_level="calm",
                accent="Azeri",
                description="Sakit, etibarlı, ev ab-havası yaradan səs.",
            )
        )
        self.add_profile(
            ActorVoiceProfile(
                name="hype_friend",
                gender="male",
                age_range="20-30",
                energy_level="high",
                accent="Azeri",
                description="Dost tonunda, sürətli, TikTok üçün enerjili səs.",
            )
        )

    def add_profile(self, profile: ActorVoiceProfile) -> None:
        self._profiles[profile.name] = profile

    def get(self, name: str) -> ActorVoiceProfile:
        return self._profiles[name]

    def list_all(self) -> List[ActorVoiceProfile]:
        return list(self._profiles.values())
