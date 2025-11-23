# src/app/agents/core/msp.py

import re
from typing import Tuple

from app.agents.ds.ds02_drive_agent import DriveAgent


# ------------------------
# Core MSP logic
# ------------------------


def _parse_msp_text(text: str) -> str:
    """
    'msp:' prefixini təmizləyib qalan hissəni qaytarır.
    """
    if not text:
        return ""

    # Telegram mesajı: "msp: nəsə nəsə"
    lowered = text.strip()
    if lowered.lower().startswith("msp:"):
        return lowered[4:].strip()

    return lowered.strip()


def _handle_ds01_market(payload: str) -> str:
    """
    DS-01 demo cavabı.
    Gözlənilən format:
      'market: <Niche> | <Country>'
    """

    # nümunə: "market: pet hair remover | US"
    pattern = r"^market\s*:\s*(.+?)\s*\|\s*(.+)$"
    m = re.match(pattern, payload.strip(), flags=re.IGNORECASE)

    if not m:
        return (
            "DS-01 Market Research formatı yanlışdır.\n"
            "Düzgün format:\n"
            "msp: market: Niche | Country\n"
            "Məsələn:\n"
            "msp: market: pet hair remover | US"
        )

    niche, country = m.group(1).strip(), m.group(2).strip()

    return (
        "DS-01 Market Research nəticəsi:\n"
        "DS-01 demo rejimindədir.\n"
        f"Niche: {niche}\n"
        f"Country: {country}\n\n"
        "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
        "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
    )


def _handle_drive(payload: str) -> str:
    """
    Drive qovluq strukturu üçün handler.
    Gözlənilən format:
      'drive: <path>'
    Məsələn:
      'drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
    """
    path = payload.strip()
    if path.lower().startswith("drive:"):
        path = path[len("drive:") :].strip()

    if not path:
        return (
            "Drive komandasının formatı yanlışdır.\n"
            "Düzgün format:\n"
            "msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
        )

    try:
        drive_agent = DriveAgent()
        result = drive_agent.handle_drive_command(
            path_str=path,
            user_email="samarkand.soul.ss@gmail.com",
        )
        return result
    except Exception as e:
        # Hər halda cavab göndərək ki, bot 'susmasın'
        return f"Drive Agent xəta verdi: {e}"


def _core_handle_msp(text: str) -> str:
    """
    Bütün MSP mesajları üçün əsas router.
    """
    payload = _parse_msp_text(text)

    # boş mesaj
    if not payload:
        return "MSP skeleton received: (boş mesaj)."

    lower_payload = payload.lower()

    # DS-01 Market Research
    if lower_payload.startswith("market:"):
        return _handle_ds01_market(payload)

    # Drive komandasI
    if lower_payload.startswith("drive:"):
        return _handle_drive(payload)

    # Default skeleton cavabı
    return f"MSP skeleton received: {payload}"


# ------------------------
# Public entrypoints
# (router hansı adı çağırsa, hamısı eyni core funksiyanı istifadə edir)
# ------------------------


def handle_msp(text: str) -> str:
    return _core_handle_msp(text)


def handle_msp_message(text: str) -> str:
    return _core_handle_msp(text)


def process_msp_message(text: str) -> str:
    return _core_handle_msp(text)


class MSPAgent:
    """
    Əgər haradasa class-lı API istifadə olunursa, bu da işləsin deyə qoyuruq.
    """

    def handle(self, text: str) -> str:
        return _core_handle_msp(text)

    def handle_message(self, text: str) -> str:
        return _core_handle_msp(text)
