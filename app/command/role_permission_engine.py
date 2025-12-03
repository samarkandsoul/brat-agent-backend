"""
Role-based permission engine (skeleton)

Hər rol üçün icazə verilən komandalar siyahısı saxlanılır.
"""

from typing import Dict, List


class RolePermissionEngine:
    def __init__(self) -> None:
        # role → allowed command names
        self._role_map: Dict[str, List[str]] = {}

    def set_permissions(self, role: str, commands: List[str]) -> None:
        self._role_map[role] = commands

    def add_permission(self, role: str, command: str) -> None:
        self._role_map.setdefault(role, [])
        if command not in self._role_map[role]:
            self._role_map[role].append(command)

    def is_allowed(self, role: str, command: str) -> bool:
        allowed = self._role_map.get(role, [])
        # “admin” üçün sadə shortcut – istənilən komandaya icazə
        if role == "admin":
            return True
        return command in allowed
