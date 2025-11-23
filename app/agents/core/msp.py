from agents.ds.ds02_drive_agent import DriveAgent

# Drive Agent-i bir dəfə yaradırıq
drive_agent = DriveAgent()


def handle_msp(text: str) -> str:
    """
    Telegramdan gələn MSP mesajını emal edir və
    həmişə cavab string qaytarır.
    """
    raw = text.strip()

    # Mesaj msp: ilə başlamırsa
    if not raw.lower().startswith("msp:"):
        return "MSP cavabı: Bu MSP komandası deyil brat."

    payload = raw[4:].strip()  # 'drive: ...' və ya 'market: ...'
    if not payload:
        return "MSP cavabı: 'msp:' yazdın, amma komanda boş qaldı."

    # --- DRIVE KOMANDASI ---
    # nümunə: msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
    if payload.lower().startswith("drive:"):
        path = payload[6:].strip()
        if not path:
            return "MSP cavabı: drive üçün qovluq path-i yazmalıyıq."
        # Burdan sonra işi DriveAgent görür
        return drive_agent.process(path)

    # --- MARKET KOMANDASI (DS-01 DEMO) ---
    # nümunə: msp: market: pet hair remover | US
    if payload.lower().startswith("market:"):
        content = payload[len("market:"):].strip()
        if not content:
            return (
                "MSP cavabı: DS-01 üçün belə yazmalıyıq:\n"
                "msp: market: Niche | Country"
            )

        parts = [p.strip() for p in content.split("|")]
        niche = parts[0] if len(parts) > 0 else ""
        country = parts[1] if len(parts) > 1 else ""

        return (
            "DS-01 Market Research nəticəsi:\n"
            "DS-01 demo rejimindədir.\n"
            f"Niche: {niche}\n"
            f"Country: {country}\n\n"
            "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
            "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
        )

    # --- DEFAULT SKELETON ---
    return (
        "MSP cavabı:\n"
        f"MSP skeleton received: {payload}"
    )


# Bəzi yerlərdə başqa ad istifadə olunubsa, ikisi də işləsin deyə:
def process_msp(text: str) -> str:
    return handle_msp(text)
