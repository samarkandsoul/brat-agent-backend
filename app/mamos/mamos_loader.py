# app/mamos/mamos_loader.py

import os

class MAMOSLoader:
    """
    Samarkand Soul – MAMOS Unified Brain Loader

    This class allows every agent to load the MAMOS document
    and understand the global mission, rules, structure and discipline.
    """

    @staticmethod
    def load_mamos() -> str:
        """
        Reads the MAMOS.md file and returns its content.
        Agents will call this method to get the main doctrine.
        """

        base_path = os.path.dirname(os.path.abspath(__file__))
        mamos_path = os.path.join(base_path, "MAMOS.md")

        try:
            with open(mamos_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"[MAMOS ERROR] Could not load MAMOS: {e}"
