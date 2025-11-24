# app/agents/core/msp.py

from typing import Tuple, List, Dict, Any, Optional

from app.agents.tiktok_growth import TikTokGrowthAgent


class MSP:
    """
    MSP (Main Service Processor) - Samarkand Soul botunun əsas router-i.
    'msp: ...' tipli komandaları oxuyub uyğun agenta yönləndirir.
    """

    def __init__(self) -> None:
        # DS, LIFE və SYS agent label xəritələri (DEMO cavab üçün)
        self.ds_labels = {
            "ds02": "DRIVE-AGENT",
            "ds03": "SHOPIFY-AGENT",
            "ds04": "OFFER & PRICING-STRATEGIST",
            "ds05": "PRODUCT-PAGE-COPYWRITER",
            "ds06": "CREATIVE-SCRIPTWRITER",
            "ds07": "AD ANGLES & HOOKS-MASTER",
            "ds08": "IMAGE & VISUAL-BRIEF-CREATOR",
            "ds09": "STORE-STRUCTURE-PLANNER",
            "ds10": "CHECKOUT & FUNNEL-OPTIMIZER",
            "ds11": "EMAIL & SMS-FLOWS-PLANNER",
            "ds12": "KPI & ANALYTICS-ANALYST",
            "ds13": "META-ADS-STRATEGIST",
            "ds14": "TIKTOK-ADS-STRATEGIST",
            "ds15": "INFLUENCER & UGC STRATEGIST",
            "ds16": "CUSTOMER-SUPPORT-PLAYBOOK-WRITER",
            "ds17": "POLICY & RISK-GUARD",
            "ds18": "SUPPLIER & LOGISTICS-PLANNER",
            "ds19": "SCALE & EXIT-STRATEGIST",
            "ds20": "EXPERIMENTS & A/B TESTING LAB",
        }

        self.life_labels = {
            "life01": "HEALTH & HABIT-COACH",
            "life02": "NUTRITION & MEAL PLANNER",
            "life03": "FITNESS & TRAINING COACH",
            "life04": "CALENDAR & TIME ARCHITECT",
            "life05": "INFO & NEWS CURATOR",
        }

        self.sys_labels = {
            "sys01": "KNOWLEDGE-LIBRARIAN",
            "sys02": "SECURITY & PRIVACY-GUARDIAN",
            "sys03": "PROCESS & SOP BUILDER",
            "sys04": "SYSTEM HEALTH & REFACTOR PLANNER",
            "sys05": "FUTURE-ROADMAP & INNOVATION-PLANNER",
        }

        # TikTok Growth Agent (TGA) – TikTok kontent fabriki
        self.tga = TikTokGrowthAgent()

    # =========================
    #  Helper-lər
    # =========================
    @staticmethod
    def _strip_msp_prefix(raw_text: str) -> str:
        """
        'msp:' prefiksini kəsir və baş/son boşluqları təmizləyir.
        """
        text = (raw_text or "").strip()
        if text.lower().startswith("msp:"):
            return text[4:].strip()
        return text

    @staticmethod
    def _split_once(body: str, sep: str = "|") -> Tuple[str, str]:
        """
        'a | b' formatını iki hissəyə bölən helper.
        """
        parts = [p.strip() for p in body.split(sep, 1)]
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    # =========================
    #  TGA – TikTok Growth Agent helper-ləri
    # =========================
    def build_tga_preview_payloads(self) -> List[Dict[str, Any]]:
        """
        TikTok Growth Agent üçün Telegram-a uyğun preview payload-larını qaytarır.

        MSP-dən kənardakı bot layer bunu belə istifadə edə bilər:
            payloads = msp.build_tga_preview_payloads()
            for p in payloads:
                bot.send_message(chat_id, **p)
        """
        return self.tga.build_telegram_preview_payloads()

    def process_callback(self, callback_data: str) -> Optional[str]:
        """
        Telegram callback_data üçün router.

        Hal-hazırda yalnız TGA üçün callback-lər:
          - tga_approve:<draft_id>
          - tga_reject:<draft_id>

        Return:
          - str -> istifadəçiyə göndəriləcək cavab mətni
          - None -> bu callback MSP tərəfindən tanınmadı, başqa router baxa bilər
        """
        if not callback_data:
            return None

        if callback_data.startswith("tga_approve:"):
            draft_id = callback_data.split(":", 1)[1]
            self.tga.handle_telegram_approval(draft_id, approved=True)
            return "✅ Video təsdiqləndi. Posting üçün növbəyə əlavə olundu."

        if callback_data.startswith("tga_reject:"):
            draft_id = callback_data.split(":", 1)[1]
            self.tga.handle_telegram_approval(draft_id, approved=False)
            return "❌ Video rədd edildi. Yeni variant generasiya olunacaq."

        # Başqa callback tipləri üçün None qaytarırıq
        return None

    # =========================
    #  Main entrypoint (text mesajlar)
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP *mətn* komandaları üçün giriş nöqtəsi.

        Nümunələr:
          - msp: market: pet hair remover | US
          - msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market
          - msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
          - msp: ds05: product page yaz
          - msp: life01: sağlamlıq planı ver
          - msp: sys01: bilik bazasını izah et
          - msp: tga: start   (TikTok Growth Agent-i işə salmaq üçün)
        """
        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = self._strip_msp_prefix(raw_text)
        if not text:
            return "MSP error: boş MSP komandası."

        lowered = text.lower()

        # ==========================================================
        # 1) DS-01 MARKET RESEARCH (real modul)
        # ----------------------------------------------------------
        # Format:
        #   msp: market: Niche | Country
        #   msp: ds01: Niche | Country
        # ==========================================================
        if lowered.startswith("market:") or lowered.startswith("ds01:"):
            if lowered.startswith("market:"):
                body = text[len("market:"):].strip()
            else:
                body = text[len("ds01:"):].strip()

            if not body:
                return (
                    "MSP error: Market komandasının gövdəsi boşdur.\n"
                    "Düzgün format: msp: market: Niche | Country\n"
                    "Məsələn: msp: market: pet hair remover | US"
                )

            niche, country = self._split_once(body, "|")
            if not country:
                country = "US"

            if not niche:
                return (
                    "MSP error: Niche boş ola bilməz.\n"
                    "Nümunə: msp: market: pet hair remover | US"
                )

            try:
                from app.agents.ds.ds01_market_research import (
                    analyze_market,
                    MarketResearchRequest,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-01 modulunu import edə bilmədim: {e}"

            try:
                req = MarketResearchRequest(niche=niche, country=country)
                result = analyze_market(req)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-01 işləmə xətası: {e}"

            return f"DS-01 Market Research nəticəsi:\n{result}"

        # ==========================================================
        # 2) DS-04 OFFER & PRICING (stub, həm 'offer:', həm də 'ds04:')
        # ==========================================================
        if lowered.startswith("offer:") or lowered.startswith("ds04:"):
            if lowered.startswith("offer:"):
                body = text[len("offer:"):].strip()
            else:
                body = text[len("ds04:"):].strip()

            if not body:
                return (
                    "MSP error: Offer komandasının gövdəsi boşdur.\n"
                    "Format: msp: offer: Məhsul üçün qiymət və bundle ideyaları | Market"
                )

            product, market = self._split_once(body, "|")
            product = product or "Naməlum məhsul"
            market = market or "Naməlum market"

            return (
                "DS-04 Offer & Pricing Strategist (DEMO):\n"
                f"Məhsul: {product}\n"
                f"Market: {market}\n\n"
                "Burada normalda ideal qiymət diapazonu, bundle təklifləri və upsell ideyaları generasiya "
                "olunacaq. Hazırda struktur testi gedir. 💡"
            )

        # ==========================================================
        # 3) DRIVE DEMO
        # ----------------------------------------------------------
        # msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
        # ==========================================================
        if lowered.startswith("drive:"):
            path = text[len("drive:"):].strip()
            if not path:
                return (
                    "MSP error: drive path boşdur.\n"
                    "Nümunə: msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master"
                )

            return (
                "Drive DEMO cavabı:\n"
                "Bu path üçün qovluq strukturu yaradılmalı idi:\n"
                f"{path}\n"
                "Google Drive real inteqrasiyasını ayrıca test edib qoşacağıq. 🎛️"
            )

        # ==========================================================
        # 4) GENERIC DS / LIFE / SYS KOMANDALARI
        # ----------------------------------------------------------
        # Formatlar:
        #   msp: ds05: ...
        #   msp: life01: ...
        #   msp: sys01: ...
        # Bu mərhələdə hamısı STUB / DEMO cavab qaytarır.
        # ==========================================================
        if ":" in text:
            prefix, _, body = text.partition(":")
            key = prefix.strip().lower()
            query = body.strip() or "(boş sorğu)"

            # ----- DS agentləri -----
            if key in self.ds_labels:
                label = self.ds_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "Bu agent hazırda struktur testi üçün stub cavab qaytarır. "
                    "Gələcəkdə burada real LLM + inteqrasiyalar işləyəcək. 🧠"
                )

            # ----- LIFE agentləri -----
            if key in self.life_labels:
                label = self.life_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "Bu LIFE agenti hazırda demo rejimindədir. Gələcəkdə şəxsi planlar və tövsiyələr "
                    "buradan generasiya olunacaq."
                )

            # ----- SYS agentləri -----
            if key in self.sys_labels:
                label = self.sys_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "Bu SYS agenti hazırda struktur testindədir. Sistem bilikləri və idarəetmə "
                    "planları buradan idarə olunacaq."
                )

        # ==========================================================
        # 4.5) TGA – TikTok Growth Agent tekst trigger-i
        # ----------------------------------------------------------
        # Sadə idarəetmə üçün:
        #   msp: tga: start
        #   msp: tiktok: start
        # TGA-nın günlük cycle-ını işə salır və preview-ları hazır edir.
        # ==========================================================
        if lowered.startswith("tga:") or lowered.startswith("tiktok:"):
            # Məzmunu hələ istifadə etməsək də gələcəkdə action-lara görə ayıra bilərik
            # Məs: "tga: preview", "tga: rerun" və s.
            self.tga.run_daily_cycle()
            return (
                "TGA — TikTok Growth Agent işə salındı.\n"
                "Bu gün üçün video draftları planlaşdırıldı və stub preview-lar hazırlandı.\n"
                "Telegram bot layer: MSP.build_tga_preview_payloads() çağıraraq həmin preview-ları "
                "Zahid Brat-a göndərə bilər. 📹"
            )

        # ==========================================================
        # 5) TANINMAYAN KOMANDA
        # ==========================================================
        return (
            "MSP error: Bu MSP komandasını tanımadım.\n"
            "Mümkün nümunələr:\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market\n"
            "  • msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master\n"
            "  • msp: ds05: product page copy yaz pet hair remover üçün\n"
            "  • msp: life01: sağlamlıq və vərdiş planı ver\n"
            "  • msp: sys01: sistem bilik bazası haqqında izah et\n"
            "  • msp: tga: start  (TikTok Growth Agent günlük cycle)\n"
            )
