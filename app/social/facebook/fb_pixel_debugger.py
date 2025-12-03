"""
Facebook pixel debugger skeleton.

Məqsəd:
- Göndərilən pixel event-lərinin daxili yoxlanması
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PixelEvent:
    name: str
    payload: Dict[str, object]


class FacebookPixelDebugger:
    REQUIRED_FIELDS = {
        "Purchase": ["value", "currency"],
        "AddToCart": ["content_ids"],
        "ViewContent": ["content_ids"],
    }

    def validate_event(self, event: PixelEvent) -> List[str]:
        errors: List[str] = []
        required = self.REQUIRED_FIELDS.get(event.name, [])
        for field in required:
            if field not in event.payload:
                errors.append(f"Missing field '{field}' for event '{event.name}'")
        return errors

    def debug_event(self, event: PixelEvent) -> Dict[str, object]:
        errors = self.validate_event(event)
        return {
            "event": event.name,
            "is_valid": not errors,
            "errors": errors,
      }
