"""
Brat Command Registry (skeleton)

Burada bütün mövcud komandalar sistemə qeyd olunur.
Real handler-ləri sonra əlavə edəcəyik.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Any


@dataclass
class CommandDefinition:
    name: str
    description: str
    handler: Optional[Callable[[Dict[str, Any]], Any]] = None
    requires_auth: bool = True


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: Dict[str, CommandDefinition] = {}

    def register(self, cmd: CommandDefinition) -> None:
        self._commands[cmd.name] = cmd

    def get(self, name: str) -> Optional[CommandDefinition]:
        return self._commands.get(name)

    def list_commands(self) -> Dict[str, str]:
        """
        Komanda adı → qısa təsvir map-i.
        """
        return {name: c.description for name, c in self._commands.items()}
