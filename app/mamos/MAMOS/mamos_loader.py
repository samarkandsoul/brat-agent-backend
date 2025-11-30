# app/mamos/MAMOS/mamos_loader.py

import os
from typing import Dict, List


class MAMOSLoader:
    """
    Samarkand Soul – MAMOS Unified Brain Loader

    Unified entry point for all agents to read the MAMOS doctrine.

    File layout this class expects:

        app/
          mamos/
            MAMOS/
              MAMOS_README.md
              mamos_loader.py
              PART_A_IDENTITY/...
              PART_D_OPERATIONS/...
              ...

    - MAMOS_README.md  → main constitution
    - all .md files in this MAMOS folder (and subfolders) → sub-doctrines
    """

    # Base filesystem configuration
    # __file__ = app/mamos/MAMOS/mamos_loader.py
    _BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    # All MAMOS .md files live in THIS folder and its subfolders
    _MAMOS_DIR = _BASE_PATH
    _MAMOS_README = os.path.join(_MAMOS_DIR, "MAMOS_README.md")

    # -------------------------------------------------------------------------
    # 1) Legacy method – main doctrine loader
    # -------------------------------------------------------------------------
    @staticmethod
    def load_mamos() -> str:
        """
        Load the main MAMOS constitution (MAMOS_README.md) and return as string.

        This is the canonical "single source of truth" used by all agents.
        On failure, returns a string starting with "[MAMOS ERROR]".
        """
        try:
            with open(MAMOSLoader._MAMOS_README, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:  # noqa: BLE001
            return f"[MAMOS ERROR] Could not load MAMOS_README.md: {e}"

    # -------------------------------------------------------------------------
    # 2) Load a specific document by relative path
    # -------------------------------------------------------------------------
    @staticmethod
    def load_document(relative_path: str) -> str:
        """
        Load a specific .md document inside the MAMOS folder.

        Examples:
            load_document("PART_A_IDENTITY/A1_Brand_Philosophy.md")
            load_document("PART_D_OPERATIONS/D2_1_Security_Framework.md")

        :param relative_path: path relative to the MAMOS folder (POSIX style "/")
        :return: file contents or an error message starting with "[MAMOS ERROR]"
        """
        doc_path = os.path.join(MAMOSLoader._MAMOS_DIR, *relative_path.split("/"))

        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:  # noqa: BLE001
            return f"[MAMOS ERROR] Could not load document '{relative_path}': {e}"

    # -------------------------------------------------------------------------
    # 3) List all .md documents under MAMOS
    # -------------------------------------------------------------------------
    @staticmethod
    def list_documents() -> List[str]:
        """
        Return relative paths of all .md documents inside the MAMOS folder.

        Example output:
            [
                "MAMOS_README.md",
                "PART_A_IDENTITY/A1_Brand_Philosophy.md",
                "PART_D_OPERATIONS/D2_1_Security_Framework.md",
                ...
            ]
        """
        documents: List[str] = []

        if not os.path.isdir(MAMOSLoader._MAMOS_DIR):
            return documents

        for root, _, files in os.walk(MAMOSLoader._MAMOS_DIR):
            for file in files:
                if not file.lower().endswith(".md"):
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, MAMOSLoader._MAMOS_DIR)

                # Normalize Windows "\\" → POSIX "/"
                rel_path = rel_path.replace("\\", "/")
                documents.append(rel_path)

        return sorted(documents)

    # -------------------------------------------------------------------------
    # 4) Load all documents into a {relative_path: content} dict
    # -------------------------------------------------------------------------
    @staticmethod
    def load_all_documents() -> Dict[str, str]:
        """
        Load all .md documents under MAMOS and return:

            {
                "MAMOS_README.md": "...",
                "PART_A_IDENTITY/A1_Brand_Philosophy.md": "...",
                ...
            }

        Useful for SYS agents like KNOWLEDGE-LIBRARIAN to get a full brain snapshot.
        """
        result: Dict[str, str] = {}
        docs = MAMOSLoader.list_documents()

        for rel_path in docs:
            full_path = os.path.join(MAMOSLoader._MAMOS_DIR, *rel_path.split("/"))
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    result[rel_path] = f.read()
            except Exception as e:  # noqa: BLE001
                result[rel_path] = (
                    f"[MAMOS ERROR] Could not load '{rel_path}': {e}"
                )

        return result
