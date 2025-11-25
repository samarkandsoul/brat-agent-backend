# app/agents/ds/ds02_drive_agent.py

from dataclasses import dataclass
from typing import List


@dataclass
class DriveNode:
    name: str
    slug: str
    level: int
    full_path: str


class DriveAgent:
    """
    DS-02 – DriveAgent

    Phase 1 (this version):
      - Takes a logical folder path as text.
      - Parses it into a structured tree.
      - Returns a nice markdown blueprint that you can use to
        create / check folders in Google Drive manually.

    Later Phase:
      - Replace the TODO section with real Google Drive API calls
        (service account or OAuth) and actually create folders.
    """

    def __init__(self) -> None:
        print("DriveAgent DS-02 initialised (architecture planner mode).")

    # ------------------------
    #  PUBLIC API
    # ------------------------
    def create_folder_path(self, path: str) -> str:
        """
        Main entrypoint used by MSP.

        Example input:
          "SamarkandSoulSystem / DS-01 - Market-Research-Master"

        Output:
          Markdown text with tree, slugs and next-step hints.
        """
        clean = (path or "").strip()
        if not clean:
            return (
                "DS-02 DriveAgent info:\n"
                "- Gələn path boşdur.\n"
                "- Nümunə istifadə:\n"
                "  `msp: drive SamarkandSoulSystem / DS-01 - Market-Research-Master`\n"
            )

        nodes = self._parse_path(clean)
        if not nodes:
            return (
                "DS-02 DriveAgent info:\n"
                "- Path parse etmək mümkün olmadı.\n"
                "- Gələn mətn: "
                f"`{clean}`\n"
            )

        lines: list[str] = []
        lines.append("# DS-02 – Drive Architecture Blueprint\n")
        lines.append(f"**Input path:** `{clean}`\n")
        lines.append(
            "Bu plan hazırda *logical blueprint* kimidir. "
            "Qovluqlar hələ real Google Drive-da yaradılmır – "
            "amma strukturu tam aydın görürük. 🚧\n"
        )

        lines.append("## Folder tree\n")
        for node in nodes:
            indent = "  " * node.level
            bullet = "-" if node.level == 0 else "*"
            lines.append(
                f"{indent}{bullet} **{node.name}**  "
                f"(slug: `{node.slug}`, level: {node.level}, path: `{node.full_path}`)"
            )

        lines.append("\n## Next steps\n")
        lines.append(
            "1. Bu strukturu Google Drive-da əl ilə və ya gələcək DS-02 API inteqrasiyası ilə yaradın.\n"
        )
        lines.append(
            "2. Eyni sluggardan istifadə etməklə bütün sistemlərdə eyni path-i qoruyun "
            "(Notion, ClickUp, Monitor və s.).\n"
        )
        lines.append(
            "3. Gələcəkdə DS-02-yə Google Drive icazələri verəndə bu funksiya "
            "bu blueprint-ə əsasən qovluqları avtomatik yaradacaq. 🔁\n"
        )

        return "\n".join(lines)

    # ------------------------
    #  INTERNAL HELPERS
    # ------------------------
    def _parse_path(self, raw: str) -> List[DriveNode]:
        """
        Split path by '/', '>' or '|' and normalise each segment.
        """
        # Normalise separators to '/'
        normalised = raw.replace(">", "/").replace("|", "/")
        parts = [p.strip() for p in normalised.split("/") if p.strip()]

        nodes: List[DriveNode] = []
        current_path_parts: list[str] = []

        for idx, part in enumerate(parts):
            current_path_parts.append(part)
            full_path = " / ".join(current_path_parts)
            slug = self._slugify(part)
            node = DriveNode(
                name=part,
                slug=slug,
                level=idx,
                full_path=full_path,
            )
            nodes.append(node)

        return nodes

    def _slugify(self, name: str) -> str:
        """
        Very small slug helper:
        - lowercase
        - spaces -> '-'
        - remove characters that often cause problems in paths.
        """
        import re

        s = name.lower()
        s = s.replace(" ", "-")
        # remove anything that is not letter, digit, dash or underscore
        s = re.sub(r"[^a-z0-9\-_]+", "", s)
        # collapse multiple dashes
        s = re.sub(r"-{2,}", "-", s).strip("-")
        return s or "node"
