# app/agents/core/msp.py

class MSP:
    def __init__(self):
        pass

    def process(self, text: str) -> str:
        text = text.strip()

        # DRIVE (DEMO)
        if text.startswith("drive:"):
            path = text[len("drive:"):].strip()

            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Düzgün format nümunə:\n"
                    "msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
                )

            return (
                "Drive DEMO cavabı:\n"
                f"Bu path üçün qovluq strukturu yaradılmalı idi:\n{path}\n\n"
                "DriveAgent real inteqrasiyasını ayrıca test edib qoşacağıq. 🚧"
            )

        # MARKET RESEARCH (DEMO)
        if text.startswith("market:"):
            body = text[len("market:"):].strip()

            try:
                niche, country = [p.strip() for p in body.split("|", 1)]
            except ValueError:
                return (
                    "MSP error: Market komandasının formatı yanlışdır.\n"
                    "Düzgün format: `msp: market: Niche | Country`\n"
                    "Məsələn: `msp: market: pet hair remover | US`"
                )

            return (
                "DS-01 Market Research nəticəsi:\n"
                "DS-01 demo rejimindədir.\n"
                f"Niche: {niche}\n"
                f"Country: {country}\n\n"
                "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
            )

        return (
            "MSP error: Bu MSP komandasını tanımadım.\n"
            "Nümunə: `msp: market: ...` və ya `msp: drive: ...`"
                )
