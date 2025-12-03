"""
Brat Command Router (skeleton)

Gələn request → hansı komanda → hansı handler?
Burada qərar verilir.
"""

from typing import Dict, Any

from .command_registry import CommandRegistry
from .command_validator import CommandValidator
from .role_permission_engine import RolePermissionEngine


class CommandRouter:
    def __init__(
        self,
        registry: CommandRegistry,
        validator: CommandValidator,
        permission_engine: RolePermissionEngine,
    ) -> None:
        self.registry = registry
        self.validator = validator
        self.permission_engine = permission_engine

    def handle(self, user_role: str, command_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Əsas entrypoint – bütün Brat komanda trafiki buradan keçir.
        """
        # 1) Komanda mövcuddurmu?
        cmd_def = self.registry.get(command_name)
        if not cmd_def:
            return {"ok": False, "error": "UNKNOWN_COMMAND"}

        # 2) İcazə var?
        if not self.permission_engine.is_allowed(user_role, command_name):
            return {"ok": False, "error": "PERMISSION_DENIED"}

        # 3) Payload validdir?
        validation = self.validator.validate(command_name, payload)
        if not validation["ok"]:
            return {"ok": False, "error": "INVALID_PAYLOAD", "details": validation}

        # 4) Handler yoxdur → hələ implement olunmayıb
        if not cmd_def.handler:
            return {"ok": False, "error": "NOT_IMPLEMENTED"}

        # 5) Handler-i işə sal
        result = cmd_def.handler(payload)
        return {"ok": True, "result": result}
