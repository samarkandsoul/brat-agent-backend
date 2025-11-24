# app/agents/core/msp.py

from typing import Tuple, List, Dict, Any, Optional

from app.agents.tiktok_growth.TGA_Main_Brain_manager import TikTokGrowthAgent


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

        return None  # Başqa callback tipləri üçün

    # =========================
    #  Main entrypoint (text mesajlar)
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP *mətn* komandaları üçün giriş nöqtəsi.
        """
        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = self._strip_msp_prefix(raw_text)
        if not text:
            return "MSP error: boş MSP komandası."

        lowered = text.lower()

        # ==========================================================
        # 1) DS-01 MARKET RESEARCH (real modul)
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
        # 2) DS-04 OFFER & PRICING (stub)
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
        # 3.5) SHOPIFY AGENT (DS03) — real API integration
        # ----------------------------------------------------------
        # Nümunələr:
        #   msp: shopify: test
        #   msp: shopify: demo
        #   msp: shopify: comingsoon
        #   msp: shopify: add | Title | Price | OptionalImageURL
        #   msp: shopify: collection | Premium Tablecloths
        # ==========================================================
        if lowered.startswith("shopify:"):
            raw_body = text[len("shopify:"):].strip()
            lowered_body = raw_body.lower()

            try:
                from app.agents.ds.ds03_shopify_agent import (
                    test_shopify_connection,
                    create_demo_product,
                    setup_coming_soon_page,
                    ShopifyDemoProductSpec,
                    create_product_from_prompt,
                    create_collection,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS03 Shopify agent import failed: {e}"

            # --- test ---
            if lowered_body.startswith("test"):
                return test_shopify_connection()

            # --- demo product ---
            if lowered_body.startswith("demo"):
                spec = ShopifyDemoProductSpec(
                    title="Samarkand Soul Demo Tablecloth",
                    description="""
                        <p>This is a demo product created by the Samarkand Soul DS03 Shopify Agent.</p>
                        <p>Premium home textile, inspired by the soul of Samarkand.</p>
                    """,
                    price="39.90",
                    tags=["samarkand soul", "demo", "tablecloth"],
                    image_url=None,  # istəsən bura şəkil URL-i qoya bilərik
                )
                return create_demo_product(spec)

            # --- coming soon page ---
            if lowered_body.startswith("comingsoon"):
                return setup_coming_soon_page()

            # --- add product via text prompt ---
            if lowered_body.startswith("add"):
                # gözlənən format:
                #   add | Title | Price | OptionalImageURL
                after = raw_body[3:].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                return create_product_from_prompt(after)

            # --- create collection ---
            if lowered_body.startswith("collection"):
                # format:
                #   collection | Premium Tablecloths
                after = raw_body[len("collection"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                return create_collection(after)

            return (
                "Shopify agent commands:\n"
                "  • msp: shopify: test\n"
                "  • msp: shopify: demo\n"
                "  • msp: shopify: comingsoon\n"
                "  • msp: shopify: add | Title | Price | OptionalImageURL\n"
                "  • msp: shopify: collection | Collection Name\n"
            )

        # ==========================================================
        # 4) GENERIC DS / LIFE / SYS KOMANDALARI
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
        # ==========================================================
        if lowered.startswith("tga:") or lowered.startswith("tiktok:"):
            self.tga.run_daily_cycle()
            summary = self.tga.get_text_preview_summary()
            return summary

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
            "  • msp: shopify: test / demo / comingsoon / add / collection\n"
            "  • msp: tga: start  (TikTok Growth Agent günlük cycle)\n"
            )
