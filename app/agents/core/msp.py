# app/agents/core/msp.py

"""
MSP (Main Service Processor) – Samarkand Soul botunun əsas router-i.

Buraya gələn "msp: ..." tipli komandaları oxuyur və uyğun agenta yönləndirir.
Hazırda dəstəklənən əsas komandalar:

  - drive: PATH
  - market: Niche | Country
  - offer: Məhsul təsviri | Market

Telegram tərəfdə mesaj belə görünür:
  msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
  msp: market: pet hair remover | US
  msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market
"""


class MSP:
    def __init__(self) -> None:
        # Gələcəkdə bura config, token və s. əlavə edə bilərik
        pass

    # =========================
    #  PUBLIC ENTRY
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP komandaları üçün giriş nöqtəsi.
        Heç vaxt None qaytarmır – həmişə str.
        """
        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = raw_text.strip()
        if not text:
            return "MSP error: boş mesaj gəldi."

        # Əgər kimsə təsadüfən yenə "msp: ..." ilə göndəribsə, onu da kəsək
        lowered = text.lower()
        if lowered.startswith("msp:"):
            text = text[4:].strip()
            lowered = text.lower()

        # ---- DRIVE KOMANDASI ------------------------------------
        if lowered.startswith("drive:"):
            return self._handle_drive(text)

        # ---- MARKET (DS-01 DEMO) --------------------------------
        if lowered.startswith("market:"):
            return self._handle_market(text)

        # ---- OFFER / PRICING (DS-04 DEMO) -----------------------
        if lowered.startswith("offer:"):
            return self._handle_offer(text)

        # Burdan aşağısı – gələcək agentlər üçün placeholder ola bilər
        # məsələn: ds01:, ds04: və s. Sonra əlavə edəcəyik.

        # ---- TANINMAYAN KOMANDA --------------------------------
        return self._unknown_command(text)

    # =========================
    #  DRIVE HANDLER (DS-02)
    # =========================
    def _handle_drive(self, text: str) -> str:
        """
        drive: PATH
        Nümunə:
          drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        """
        # "drive:" hissəsini kəsək
        body = text[len("drive:"):].strip()
        if not body:
            return (
                "MSP error: drive path boşdur.\n"
                "Nümunə: msp: drive: SamarkandSoulSystem / DS System / "
                "DS-01 - Market-Research-Master"
            )

        # Import ayrı try/except-də ki, səhv olanda bütün servis yıxılmasın
        try:
            from app.agents.ds.ds02_drive_agent import DriveAgent
        except Exception as e:  # pragma: no cover
            return (
                "MSP error: DriveAgent import xətası.\n"
                f"Detallar: {e}\n\n"
                "Drive inteqrasiyasını sonra ayrıca düzəldərik, sistem işə davam edir. 🧩"
            )

        # Agent obyektini yaratmağa cəhd edək
        try:
            agent = DriveAgent()
        except Exception as e:  # pragma: no cover
            return (
                "MSP error: DriveAgent init xətası.\n"
                f"Detallar: {e}\n\n"
                "Ən çox ehtimal: GOOGLE_SERVICE_ACCOUNT_JSON və ya icazələr düzgün deyil."
            )

        # Qovluq path-i yaratmağa cəhd edək
        try:
            result = agent.create_folder_path(body)
            # DriveAgent özündə artıq səliqəli mesaj qaytarır
            return result
        except Exception as e:  # pragma: no cover
            return (
                "MSP error: DriveAgent create_folder_path xətası.\n"
                f"Path: {body}\n"
                f"Detallar: {e}"
            )

    # =========================
    #  MARKET HANDLER (DS-01 DEMO)
    # =========================
    def _handle_market(self, text: str) -> str:
        """
        market: Niche | Country
        Nümunə:
          market: pet hair remover | US
        """
        body = text[len("market:"):].strip()
        if not body:
            return (
                "MSP error: Market komandasının bədəni boşdur.\n"
                "Düzgün format: msp: market: Niche | Country\n"
                "Məsələn: msp: market: pet hair remover | US"
            )

        parts = [p.strip() for p in body.split("|", 1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return (
                "MSP error: Market komandasının formatı yanlışdır.\n"
                "Düzgün format: msp: market: Niche | Country\n"
                "Məsələn: msp: market: pet hair remover | US"
            )

        niche, country = parts[0], parts[1]

        # Hələlik DEMO cavab – DS-01 backend-i sonra real OpenAI ilə birləşdirəcəyik
        return (
            "DS-01 Market Research nəticəsi (DEMO):\n"
            f"Niche: {niche}\n"
            f"Country: {country}\n\n"
            "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
            "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
        )

    # =========================
    #  OFFER / PRICING HANDLER (DS-04 DEMO)
    # =========================
    def _handle_offer(self, text: str) -> str:
        """
        offer: Məhsul təsviri | Market
        Nümunə:
          offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market
        """
        body = text[len("offer:"):].strip()
        if not body:
            return (
                "MSP error: Offer komandasının bədəni boşdur.\n"
                "Düzgün format: msp: offer: Məhsul təsviri | Market\n"
                "Məsələn: msp: offer: pet hair remover üçün ideal qiymət və "
                "bundle ideyaları | US market"
            )

        parts = [p.strip() for p in body.split("|", 1)]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return (
                "MSP error: Offer komandasının formatı yanlışdır.\n"
                "Düzgün format: msp: offer: Məhsul təsviri | Market\n"
                "Məsələn: msp: offer: pet hair remover üçün ideal qiymət və "
                "bundle ideyaları | US market"
            )

        product_desc, market = parts[0], parts[1]

        # DEMO cavab – DS-04 agentini sonra real OpenAI ilə qüvvəyə minəcək formada yazacağıq
        return (
            "DS-04 Offer & Pricing Strategist (DEMO):\n"
            f"Məhsul: {product_desc}\n"
            f"Market: {market}\n\n"
            "Burada normalda ideal qiymət diapazonu, bundle təklifləri və "
            "upsell ideyaları generasiya olunacaq. Hazırda struktur testi gedir. 💡"
        )

    # =========================
    #  UNKNOWN COMMAND
    # =========================
    def _unknown_command(self, text: str) -> str:
        """
        Tanınmayan komandalar üçün fallback cavab.
        """
        return (
            "MSP error: Bu MSP komandasını tanımadım.\n"
            "Gələn mətn:\n"
            f"  `{text}`\n\n"
            "Hazırda aşağıdakı MSP komandalarını anlayıram:\n"
            "  • msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market\n\n"
            "Qalan DS, LIFE və SYS agentləri üçün router-i mərhələli şəkildə əlavə edəcəyik. 🔧"
        )
