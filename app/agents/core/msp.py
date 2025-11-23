from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest
from app.agents.ds.ds02_drive_agent import DriveAgent


class MSP:
    """
    MSP – Master Strategy Processor.

    Qəbul etdiyi nümunə komandalar:
      "market: pet hair remover | US"
      "shopify temasi hazirla"
      "drive: samarkand soul qovlugu yarat"
    """

    def __init__(self) -> None:
        # Gələcəkdə burada başqa agentlər də saxlayacağıq
        self.drive_agent = DriveAgent()

    def process(self, raw_command: str) -> str:
        """
        Telegram-dan gələn MSP komandalarını emal edir.
        Sadə string qaytarır.
        """
        text = (raw_command or "").strip()
        if not text:
            return "MSP: Boş komanda alındı."

        lower = text.lower()

        # =========================
        #  DS-01: MARKET RESEARCH
        # =========================
        # "market: Niche | Country" və ya "market Niche | Country"
        if lower.startswith("market"):
            niche = ""
            country = "US"

            if ":" in text:
                after = text.split(":", 1)[1].strip()
            else:
                after = text.split(" ", 1)[1].strip() if " " in text else ""

            if after:
                parts = [p.strip() for p in after.split("|")]
                if len(parts) >= 1:
                    niche = parts[0]
                if len(parts) >= 2 and parts[1]:
                    country = parts[1]

            if not niche:
                return (
                    "MSP: `market` komandası üçün format belə olmalıdır:\n"
                    "market: Niche | Country\n"
                    "Məsələn: market: pet hair remover | US"
                )

            try:
                req = MarketResearchRequest(niche=niche, country=country)
                result = analyze_market(req)

                if isinstance(result, dict) and "error" in result:
                    return f"DS-01 error: {result}"

                return f"DS-01 Market Research nəticəsi:\n{result}"
            except Exception as e:
                return f"MSP: DS-01 çağırılarkən xəta baş verdi: {e!r}"

        # =========================
        #  SHOPIFY SKELETON
        # =========================
        if lower.startswith("shopify"):
            return (
                "Shopify komandası qəbul edildi. "
                "Tezliklə inteqrasiyaya əlavə olunacaq."
            )

        # =========================
        #  DS-02: DRIVE AGENT SKELETON
        # =========================
        if lower.startswith("drive"):
            # "drive: ..." və ya "drive ..." formasında ola bilər
            if ":" in text:
                payload = text.split(":", 1)[1].strip()
            else:
                payload = text.split(" ", 1)[1].strip() if " " in text else ""

            if not payload:
                return (
                    "Drive Agent üçün komanda boşdur. Nümunə:\n"
                    "drive: Samarkand Soul üçün yeni qovluq yarat"
                )

            try:
                return self.drive_agent.process(payload)
            except Exception as e:
                return f"Drive Agent xətaya düşdü: {e!r}"

        # =========================
        #  DEFAULT – ECHO
        # =========================
        return f"MSP skeleton received: {text}"
