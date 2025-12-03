"""
Instagram hashtag engine skeleton.

Məqsəd:
- Nişə uyğun hashtag paketləri yaratmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class HashtagRequest:
    niche: str
    language: str = "az"
    max_tags: int = 25


class InstagramHashtagEngine:
    def generate_hashtags(self, req: HashtagRequest) -> List[str]:
        """
        Sadə placeholder – real versiyada:
        - lokasiya + niş + trend dataları nəzərə alınacaq
        """
        base = req.niche.lower().replace(" ", "")
        tags = [
            f"#{base}",
            f"#{base}az",
            "#butik",
            "#onlinealisveris",
            "#evdekor",
        ]
        return tags[: req.max_tags]
