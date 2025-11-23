# src/app/agents/core/msp.py

from typing import Any, Optional

# VACİB: DriveAgent modulunun YOLU
# Səndə ds agentləri ayrıca "ds" qovluğundadırsa, bu import doğrudur:
from app.agents.ds.ds02_drive_agent import DriveAgent


class MSP:
    """
    MSP – Samarkand Soul üçün mərkəzi komanda emalçısı.
    Telegram bot sadəcə msp.process(text) çağırır, o da cavab string qaytarır.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Mövcud koddakı hər cür konstruktor çağırışını pozmamaq üçün *args/**kwargs qəbul edirik.
        # DriveAgent istəsən, backend-dən belə ötürə bilərsən:
        # msp = MSP(drive_agent=my_drive_agent)
        self.drive_agent: Optional[DriveAgent] = kwargs.get("drive_agent")

    # Telegram-da çağırılan əsas funksiya
    def process(self, text: str) -> str:
        text = (text or "").strip()

        # Boş mesaj
        if not text:
            return "MSP error: boş komanda göndərdin."

        lower = text.lower()

        # DS-01 – Market Research
        if lower.startswith("market:"):
            return self._handle_market_command(text)

        # Drive – Google Drive qovluq strukturu
        if lower.startswith("drive:"):
            return self._handle_drive_command(text)

        # Digər hallar
        return (
            "MSP cavabı:\n"
            "Bu komandani hələ başa düşmürəm.\n\n"
            "Mövcud format nümunələri:\n"
            "• market: Niche | Country\n"
            "• drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
        )

    # -----------------------------
    # DS-01 – Market Research (demo)
    # -----------------------------
    def _handle_market_command(self, text: str) -> str:
        try:
            payload = text[len("market:") :].strip()
            niche, country = [part.strip() for part in payload.split("|", 1)]
        except ValueError:
            return (
                "MSP error: Market komandası üçün format belə olmalıdır:\n"
                "market: Niche | Country\n"
                "Məsələn:\n"
                "market: pet hair remover | US"
            )

        return (
            "DS-01 Market Research nəticəsi:\n"
            "DS-01 demo rejimindədir.\n"
            f"Niche: {niche}\n"
            f"Country: {country}\n\n"
            "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
            "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
        )

    # -----------------------------
    # Drive Agent – qovluq strukturu
    # -----------------------------
    def _handle_drive_command(self, text: str) -> str:
        # DriveAgent MSP-yə ötürülməyibsə
        if self.drive_agent is None:
            return (
                "Drive Agent hələ tam qoşulmayıb.\n"
                "Backend-də DriveAgent obyektini yaradıb MSP(drive_agent=...) "
                "şəklində ötürmək lazımdır."
            )

        path = text[len("drive:") :].strip()
        if not path:
            return (
                "MSP error: Drive komandası üçün format belə olmalıdır:\n"
                "drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
            )

        try:
            # Burada mövcud DriveAgent API-sinə uyğun funksiya çağırırıq.
            # Səndə bu metodun adı fərqlidirsə, sadəcə burda dəyişəcəksən.
            result = self.drive_agent.create_folder_structure(path)
        except Exception as e:
            return f"MSP error: Drive Agent icra zamanı xəta verdi: {e}"

        # Nəticə dict və ya sadə link string ola bilər – ikisini də dəstəkləyək
        if isinstance(result, dict):
            link = result.get("link") or result.get("url") or ""
        else:
            link = str(result)

        msg = [
            "Drive Agent: Qovluq strukturu hazırdır.",
            f"Path: {path}",
        ]
        if link:
            msg.append(f"Link: {link}")

        return "\n".join(msg)


__all__ = ["MSP"]
