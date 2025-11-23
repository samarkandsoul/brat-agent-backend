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

        # 1) DRIVE KOMANDASI – HƏLƏLİK DEMO MOD
        # nümunə:  msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        if text.startswith("drive:"):
            path = text[len("drive:"):].strip()

            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Düzgün format nümunə:\n"
                    "msp: drive: SamarkandSoulSystem / DS System / "
                    "DS-01 - Market-Research-Master"
                )

            # HƏLƏLİK GOOGLE DRIVE-Ə TOXUNMURUQ – SADƏCƏ DEMO CAVAB
            return (
                "Drive DEMO cavabı:\n"
                f"Bu path üçün qovluq strukturu yaradılmalı idi:\n{path}\n\n"
                "DriveAgent real inteqrasiyasını ayrıca test edib qoşacağıq. 🚧"
            )

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
                "Real market analizi OpenAI balansı aktiv olandan sonra qoş
