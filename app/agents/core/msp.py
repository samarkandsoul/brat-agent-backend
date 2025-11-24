# app/agents/core/msp.py

class MSP:
    """
    Minimal debug MSP.
    Gələn mətnin özünü geri qaytarır ki, zənciri test edək.
    """

    def __init__(self) -> None:
        pass

    def process(self, raw_text: str) -> str:
        if not raw_text:
            return "MSP DEBUG: boş mesaj gəldi."

        text = raw_text.strip()
        return f"MSP DEBUG cavab: '{text}'"
