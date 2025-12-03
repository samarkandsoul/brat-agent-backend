"""
Command payload validator (skeleton)

Sadə schema sistemi: hər komanda üçün tələb olunan field-ləri saxlayırıq.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class CommandSchema:
    required_fields: List[str] = field(default_factory=list)


class CommandValidator:
    def __init__(self) -> None:
        # command_name → schema
        self._schemas: Dict[str, CommandSchema] = {}

    def register_schema(self, command_name: str, schema: CommandSchema) -> None:
        self._schemas[command_name] = schema

    def validate(self, command_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        schema = self._schemas.get(command_name)
        if not schema:
            # Schema yoxdursa, “pass-through” edirik
            return {"ok": True, "missing_fields": []}

        missing = [f for f in schema.required_fields if f not in payload]
        return {
            "ok": len(missing) == 0,
            "missing_fields": missing,
  }
