"""
File Utils – sadə fayl oxu/yazı köməkçiləri.
"""

import json
from typing import Any


class FileUtils:
    @staticmethod
    def read_json(path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json(path: str, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def read_text(path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_text(path: str, text: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
