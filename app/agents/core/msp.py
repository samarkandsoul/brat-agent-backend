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
        """

        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        # Baş-boşluqları təmizləyək
        text = raw_text.strip()

        # Əgər 'msp:' ilə başlayırsa, onu kəsək ki, iç router sadə işləsin
        lowered = text.lower()
        if lowered.startswith("msp:"):
            text = text[4:].strip()  # 'msp:' 4 simvol

        # ==========================================================
        # 1) DRIVE KOMANDASI (full debug-lu)
        # ----------------------------------------------------------
        # Nümunə:
        #   msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        # ==========================================================
        if text.lower().startswith("drive:"):
            path = text[len("drive:"):].strip()

            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Nümunə: msp: drive: SamarkandSoulSystem / DS System / "
                    "DS-01 - Market-Research-Master"
                )

            # 1) Import-u ayrıca yoxlayaq
            try:
                from app.agents.ds.ds02_drive_agent import DriveAgent
            except Exception as e:
                return f"MSP error: DriveAgent import xətası: {e}"

            # 2) Agent obyektinin yaradılmasını ayrıca yoxlayaq
            try:
                agent = DriveAgent()
            except Exception as e:
                return f"MSP error: DriveAgent init xətası: {e}"

            # 3) Qovluq path-i yaratmağı ayrıca yoxlayaq
            try:
                result = agent.create_folder_path(path)
                return result
            except Exception as e:
                return f"MSP error: DriveAgent create_folder_path xətası: {e}"

        # ==========================================================
        # 2) DS-01 MARKET RESEARCH DEMO
        # ----------------------------------------------------------
        # Nümunə:
        #   msp: market: pet hair remover | US
        # Format:
        #   market: Niche | Country
        # ==========================================================
        if text.lower().startswith("market:"):
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
        # 3) TANINMAYAN KOMANDA
        # ==========================================================
        return (
            "MSP error: Bu MSP komandasını tanımadım.\n"
            "Mümkün nümunələr:\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: drive: SamarkandSoulSystem / DS System / "
            "DS-01 - Market-Research-Master"
                )
