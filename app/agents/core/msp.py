from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest
from app.agents.ds.ds02_drive_agent import DriveAgent
from app.agents.ds.ds03_shopify_agent import ShopifyAgent


class MSP:
    """
    MSP – Master Strategy Processor.
    Bütün agentləri yönləndirən əsas beyin moduludur.
    """

    def __init__(self) -> None:
        # Agent obyektləri
        self.drive_agent = DriveAgent()
        self.shopify_agent = ShopifyAgent()

    def process(self, raw_command: str) -> str:
        """
        Telegram-dan gələn MSP komandalarını emal edir.
        """
        text = (raw_command or "").strip()
        if not text:
            return "MSP: Boş komanda alındı."

        lower = text.lower()

        # =========================
        # DS-01: MARKET RESEARCH
        # =========================
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
        # DS-02: DRIVE AGENT
        # =========================
        if lower.startswith("drive"):
            if ":" in raw_command:
                payload = raw_command.split(":", 1)[1].strip()
            else:
                payload = raw_command.split(" ", 1)[1].strip() if " " in raw_command else ""

            if not payload:
                return (
                    "Drive Agent üçün komanda boşdur.\n"
                    "Nümunə: drive: Samarkand Soul üçün yeni qovluq yarat"
                )

            try:
                return self.drive_agent.process(payload)
            except Exception as e:
                return f"Drive Agent xətaya düşdü: {e!r}"

        # =========================
        # DS-03: SHOPIFY AGENT
        # =========================
        if lower.startswith("shopify"):
            if ":" in raw_command:
                payload = raw_command.split(":", 1)[1].strip()
            else:
                payload = raw_command.split(" ", 1)[1].strip() if " " in raw_command else ""

            if not payload:
                return (
                    "Shopify Agent üçün komanda boşdur.\n"
                    "Nümunə: shopify: kolleksiya yarat"
                )

            try:
                return self.shopify_agent.process(payload)
            except Exception as e:
                return f"Shopify Agent xətaya düşdü: {e!r}"

        # =========================
        # DEFAULT – TANINMAYAN KOMANDA
        # =========================
        return f"MSP skeleton received: {text}"
