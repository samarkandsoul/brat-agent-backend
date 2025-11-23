import re
from dataclasses import dataclass
from typing import Optional, Tuple

# ✅ DİQQƏT:
# DriveAgent artıq ayrıca fayldadır (ds02_drive_agent.py).
# Biz onu birbaşa buradan çağırırıq.
# Fayl yolu: app/agents/ds02_drive_agent.py
from app.agents.ds02_drive_agent import DriveAgent


# ==============================
#  MSP AGENT — CORE LOGIC
# ==============================

@dataclass
class MSPCommandResult:
    success: bool
    message: str


class MSPAgent:
    """
    MSP — 'Multi-System Processor'
    Burada:
      • DS-01 Market Research komandasını emal edir
      • DriveAgent vasitəsilə Google Drive qovluqları yaradır
    """

    # ---------- PUBLIC MAIN ENTRY ----------

    def handle(self, text: str) -> str:
        """
        Telegramdan gələn `msp: ....` hissəsi buraya düşür.
        """
        cleaned = text.strip()

        # boşdursa
        if not cleaned:
            return "MSP cavabı:\nBoş komanda göndərildi."

        # əvvəl drive komandasını yoxlayaq
        if cleaned.lower().startswith("drive:"):
            return self._handle_drive_command(cleaned)

        # sonra DS-01 market research
        if cleaned.lower().startswith("market:"):
            return self._handle_ds01_market(cleaned)

        # əks halda tanınmayan komanda
        return (
            "MSP cavabı:\n"
            "Bu komandanı hələ anlamıram.\n\n"
            "Mümkün komandalar:\n"
            "• DS-01 Market Research:  market: Niche | Country\n"
            "• Drive Agent:            drive: PATH/to/folder"
        )

    # ---------- DS-01 MARKET RESEARCH ----------

    def _parse_market_command(self, cmd: str) -> Optional[Tuple[str, str]]:
        """
        Gözlənən format:
            market: Niche | Country
        Məsələn:
            market: pet hair remover | US
        """
        # "market:" sözünü sil
        body = cmd[len("market:") :].strip()
        if "|" not in body:
            return None

        parts = [p.strip() for p in body.split("|", maxsplit=1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None

        niche, country = parts
        return niche, country

    def _handle_ds01_market(self, cmd: str) -> str:
        parsed = self._parse_market_command(cmd)
        if not parsed:
            return (
                "MSP cavabı:\n"
                "DS-01 Market Research komandası yanlışdır.\n"
                "Düzgün format:\n"
                "  msp: market: Niche | Country\n"
                "Məsələn:\n"
                "  msp: market: pet hair remover | US"
            )

        niche, country = parsed

        # Hal-hazırda bunu DEMO kimi saxlayırıq – real analitika OpenAI balansı aktiv olanda qoşulacaq.
        return (
            "MSP cavabı:\n"
            "DS-01 Market Research nəticəsi:\n"
            "DS-01 demo rejimindədir.\n"
            f"Niche: {niche}\n"
            f"Country: {country}\n\n"
            "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
            "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
        )

    # ---------- DRIVE AGENT ----------

    def _parse_drive_path(self, cmd: str) -> Optional[str]:
        """
        Gözlənən format:
            drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        Yəni 'drive:' sözündən sonra gələn hər şeyi PATH kimi qəbul edirik.
        """
        body = cmd[len("drive:") :].strip()
        if not body:
            return None
        # lazımsız boşluqları bir az təmizləyək
        body = re.sub(r"\s*/\s*", " / ", body)
        return body

    def _handle_drive_command(self, cmd: str) -> str:
        path = self._parse_drive_path(cmd)
        if not path:
            return (
                "MSP cavabı:\n"
                "Drive Agent komandası yanlışdır.\n"
                "Düzgün format:\n"
                "  msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
            )

        # DriveAgent-i çağırırıq
        try:
            drive_agent = DriveAgent()
            result: MSPCommandResult = drive_agent.create_folder_structure(path)  # type: ignore
        except Exception as e:
            # DriveAgent daxilində hər hansı xəta olarsa, onu user-friendly göstəririk
            return (
                "MSP cavabı:\n"
                "Drive Agent xətası baş verdi.\n"
                f"Texniki məlumat: {e}"
            )

        status = "uğurlu" if result.success else "uğursuz"
        return f"MSP cavabı:\nDrive Agent nəticəsi ({status}):\n{result.message}"


# ==============================
#  WRAPPER — KÖHNƏ KOD ÜÇÜN
# ==============================

class MSP:
    """
    Köhnə sistemlə tam uyğunluq üçün wrapper.

    Köhnə backend hələ də belə çağırır:
        msp = MSP()
        msp.process(text)

    Yeni sistemdə isə MSPAgent.handle(text) istifadə olunur.
    Bu wrapper bütün köhnə adları (process, run, execute, __call__) MSPAgent-ə yönləndirir.
    """

    def __init__(self):
        self.agent = MSPAgent()

    # Köhnə əsas metod
    def process(self, text: str) -> str:
        return self.agent.handle(text)

    # Ehtiyat köhnə adlar
    def run(self, text: str) -> str:
        return self.agent.handle(text)

    def execute(self, text: str) -> str:
        return self.agent.handle(text)

    # Yeni adlar
    def handle(self, text: str) -> str:
        return self.agent.handle(text)

    def handle_message(self, text: str) -> str:
        return self.agent.handle(text)

    # msp("text") kimi çağırmaq üçün
    def __call__(self, text: str) -> str:
        return self.agent.handle(text)
