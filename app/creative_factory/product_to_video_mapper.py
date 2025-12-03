"""
Product → video concept mapper skeleton.

Məqsəd:
- Məhsul datasından müxtəlif video ideyaları çıxarmaq
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ProductInfo:
    name: str
    main_benefit: str
    key_features: List[str]
    use_case: str  # "table setup", "gift", "daily use" və s.


@dataclass
class VideoConcept:
    hook: str
    storyline: str
    call_to_action: str
    recommended_duration_sec: int


class ProductToVideoMapper:
    def generate_concepts(self, product: ProductInfo) -> List[VideoConcept]:
        concepts: List[VideoConcept] = []

        # 1 – Problem / solution
        concepts.append(
            VideoConcept(
                hook=f"Masanda ruh yoxdur? {product.name} ilə sına!",
                storyline=(
                    "Sıradan masa görüntüsü göstər, sonra Samarkand stilinə keçid. "
                    "Əvvəl / sonrası müqayisə, detallara zoom."
                ),
                call_to_action="Linkə kliklə, masanı Samarkand səviyyəsinə qaldır.",
                recommended_duration_sec=25,
            )
        )

        # 2 – Ritual / lifestyle
        concepts.append(
            VideoConcept(
                hook="Hər səhər eyni masa? Kiçik detal, böyük dəyişiklik.",
                storyline=(
                    "Səhər çayı / qəhvə ritualı, masa örtüyünün teksturasına fokus, "
                    "əl ilə toxunuş, yumşaq hərəkətlər."
                ),
                call_to_action="Sevdiyin rituala öz stilini əlavə et.",
                recommended_duration_sec=30,
            )
        )

        # 3 – Gifting
        concepts.append(
            VideoConcept(
                hook="‘Nə hədiyyə alım?’ sualına cavab.",
                storyline=(
                    "Hədiyyə paketi açılır, masa örtüyü çıxır, masa tez qurulur, "
                    "ailə / dostlar ətrafında toplaşır."
                ),
                call_to_action="Zövqlü və istifadə olunan hədiyyə vermək üçün profili yoxla.",
                recommended_duration_sec=30,
            )
        )

        return concepts
