# app/mamos/mamos_loader.py

import os
from typing import Dict, List


class MAMOSLoader:
    """
    Samarkand Soul – MAMOS Unified Brain Loader

    Bu klass agentlərə MAMOS beynini oxumaq üçün vahid giriş nöqtəsidir.
    - MAMOS_README.md  → əsas konstitusiya
    - MAMOS/ altındakı bütün .md fayllar → alt doktrinalar (agentlər, sistem, s.ü.)
    """

    # Fayl yolları üçün baza konfiqurasiya
    _BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    _MAMOS_DIR = os.path.join(_BASE_PATH, "MAMOS")
    _MAMOS_README = os.path.join(_MAMOS_DIR, "MAMOS_README.md")

    # -------------------------------------------------------------------------
    # 1) Köhnə metod – geri uyğunluq (main doktrina)
    # -------------------------------------------------------------------------
    @staticmethod
    def load_mamos() -> str:
        """
        Legacy giriş nöqtəsi.

        Əsas MAMOS konstitusiyasını (MAMOS_README.md) oxuyur və string kimi qaytarır.
        Bütün agentlər üçün “single source of truth” bu fayldır.
        """
        try:
            with open(MAMOSLoader._MAMOS_README, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[MAMOS ERROR] Could not load MAMOS_README.md: {e}"

    # -------------------------------------------------------------------------
    # 2) Konkrekt sənəd yükləmək üçün metod
    # -------------------------------------------------------------------------
    @staticmethod
    def load_document(relative_path: str) -> str:
        """
        Verilən nisbət yolu əsasında MAMOS içindəki konkret .md sənədini oxuyur.

        Misallar:
            load_document('PART_A_IDENTITY/A1_Brand_Philosophy.md')
            load_document('PART_C_AGENTS_BIBLE/C2_03_ShopifyAgent.md')

        :param relative_path: MAMOS qovluğuna nisbətən yol (POSIX style / ilə)
        :return: Fayl məzmunu və ya xəta mesajı
        """
        doc_path = os.path.join(MAMOSLoader._MAMOS_DIR, *relative_path.split("/"))

        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[MAMOS ERROR] Could not load document '{relative_path}': {e}"

    # -------------------------------------------------------------------------
    # 3) Bütün MAMOS .md fayllarının siyahısı
    # -------------------------------------------------------------------------
    @staticmethod
    def list_documents() -> List[str]:
        """
        MAMOS qovluğundakı bütün .md sənədlərin nisbət yollarını qaytarır.

        Nümunə çıxış:
            [
                'MAMOS_README.md',
                'PART_A_IDENTITY/A1_Brand_Philosophy.md',
                'PART_C_AGENTS_BIBLE/C2_01_MarketResearch.md',
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

                # Windows \\ → POSIX /
                rel_path = rel_path.replace("\\", "/")
                documents.append(rel_path)

        return sorted(documents)

    # -------------------------------------------------------------------------
    # 4) Bütün sənədləri dictionary kimi yükləmək
    # -------------------------------------------------------------------------
    @staticmethod
    def load_all_documents() -> Dict[str, str]:
        """
        Bütün MAMOS .md fayllarını {relative_path: content} formatında qaytarır.

        Bu, daha sonra “Knowledge Librarian” və ya başqa SYS agentlərə
        tam beyin snapshot-u vermək üçün istifadə oluna bilər.
        """
        result: Dict[str, str] = {}
        docs = MAMOSLoader.list_documents()

        for rel_path in docs:
            full_path = os.path.join(MAMOSLoader._MAMOS_DIR, *rel_path.split("/"))
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    result[rel_path] = f.read()
            except Exception as e:
                result[rel_path] = f"[MAMOS ERROR] Could not load '{rel_path}': {e}"

        return result
