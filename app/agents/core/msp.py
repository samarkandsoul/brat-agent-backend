# app/agents/core/msp.py

class MSP:
    """
    MSP (Main Service Processor) - Samarkand Soul botunun əsas router-i.
    Buraya gələn "msp: ..." komandalarını oxuyub uyğun agenta yönləndirir.
    """

    def __init__(self) -> None:
        # Gələcəkdə bura config, token və s. əlavə edə bilərik
        pass

    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP komandaları üçün giriş nöqtəsi.

        Nümunələr:
          - 'msp: market: pet hair remover | US'
          - 'msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
          - 'msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market'
        """

        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = raw_text.strip()
        lower = text.lower()

        # ==========================================================
        # 1) DRIVE KOMANDASI
        # ==========================================================
        if lower.startswith("drive:"):
            path = text[len("drive:"):].strip()

            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Nümunə: msp: drive: SamarkandSoulSystem / DS System / "
                    "DS-01 - Market-Research-Master"
                )

            # Import-u yoxlayırıq
            try:
                from app.agents.ds.ds02_drive_agent import DriveAgent
            except Exception as e:
                return f"MSP error: DriveAgent import xətası: {e}"

            # Agent obyekti
            try:
                agent = DriveAgent()
            except Exception as e:
                return f"MSP error: DriveAgent init xətası: {e}"

            # Qovluq path-i
            try:
                result = agent.create_folder_path(path)
                return result
            except Exception as e:
                return f"MSP error: DriveAgent create_folder_path xətası: {e}"

        # ==========================================================
        # 2) DS-01 MARKET RESEARCH (DEMO)
        # ==========================================================
        if lower.startswith("market:"):
            body = text[len("market:"):].strip()

            try:
                niche, country = [p.strip() for p in body.split("|", 1)]
            except ValueError:
                return (
                    "MSP error: Market komandasının formatı yanlışdır.\n"
                    "Düzgün format: msp: market: Niche | Country\n"
                    "Məsələn: msp: market: pet hair remover | US"
                )

            if not niche or not country:
                return (
                    "MSP error: Niche və Country boş ola bilməz.\n"
                    "Nümunə: msp: market: pet hair remover | US"
                )

            return (
                "DS-01 Market Research nəticəsi:\n"
                "DS-01 demo rejimindədir.\n"
                f"Niche: {niche}\n"
                f"Country: {country}\n\n"
                "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
                "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
            )

        # ==========================================================
        # 3) DS-04 OFFER & PRICING STRATEGIST (DEMO)
        # ==========================================================
        if lower.startswith("offer:"):
            # 1) import
            try:
                from app.agents.ds.ds04_offer_pricing import OfferPricingAgent
            except Exception as e:
                return f"MSP error: OfferPricingAgent import xətası: {e}"

            # 2) sorğunu təmizləyək
            query = text[len("offer:"):].strip()
            if not query:
                return (
                    "MSP error: Offer mətni boşdur.\n"
                    "Nümunə: msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market"
                )

            # 3) agenti işə salaq
            try:
                agent = OfferPricingAgent()
                agent_response = agent.process(query)
                return agent_response
            except Exception as e:
                return f"MSP error: OfferPricingAgent işləyə bilmədi: {e}"

        # ==========================================================
        # 4) TANINMAYAN KOMANDA
        # ==========================================================
        return (
            "MSP error: Bu MSP komandasını tanımadım.\n"
            "Mümkün nümunələr:\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master\n"
            "  • msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market"
            )
