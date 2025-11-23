# app/agents/core/msp.py

class MSP:
    def __init__(self):
        # Gələcəkdə bura konfiq, token və s. əlavə edə bilərik
        pass

    def process(self, text: str) -> str:
        """
        MSP əsas router-di.
        Burda "msp: ..." komandalarını oxuyuruq və uyğun agenta yönləndiririk.
        """
        # Təhlükəsizlik üçün boşluqları təmizləyək
        text = text.strip()

        # 1) DRIVE KOMANDASI
        # nümunə:  msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        if text.startswith("drive:"):
            # İçi boş olsa belə, burda heç error atmasın deyə try/except əlavə edirik
            from app.agents.ds.ds02_drive_agent import DriveAgent  # <-- YOL DÜZDÜR

            path = text[len("drive:"):].strip()
            if not path:
                return "MSP error: drive path boşdur. Nümunə: `msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master`"

            agent = DriveAgent()
            try:
                result = agent.create_folder_path(path)
                return result
            except Exception as e:
                return f"MSP error (DriveAgent): {e}"

        # 2) DS-01 MARKET RESEARCH DEMO
        # nümunə:  msp: market: pet hair remover | US
        if text.startswith("market:"):
            body = text[len("market:"):].strip()

            # "Niche | Country" formatını parçalayaq
            try:
                niche, country = [p.strip() for p in body.split("|", 1)]
            except ValueError:
                return (
                    "MSP error: Market komandasının formatı yanlışdır.\n"
                    "Düzgün format: `msp: market: Niche | Country`\n"
                    "Məsələn: `msp: market: pet hair remover | US`"
                )

            # Hələlik DEMO cavab (OpenAI real balans gələndən sonra buranı dəyişərik)
            return (
                "DS-01 Market Research nəticəsi:\n"
                "DS-01 demo rejimindədir.\n"
                f"Niche: {niche}\n"
                f"Country: {country}\n\n"
                "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
                "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
            )

        # Tanımadığı komanda
        return "MSP error: Bu MSP komandasını tanımadım. Nümunə: `msp: market: ...` və ya `msp: drive: ...`"
