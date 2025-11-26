# app/agents/core/msp.py

from typing import Tuple, List, Dict, Any, Optional

# TikTok Growth brain
from app.agents.tiktok_growth.TGA_Main_Brain_manager import TikTokGrowthAgent

# DS-02 Drive Agent
from app.agents.ds.ds02_drive_agent import DriveAgent

# MAMOS – unified doctrine loader
from app.mamos.mamos_loader import MAMOSLoader

# Brat GPT – unified LLM interface (MAMOS-aware)
from app.llm.brat_gpt import brat_gpt_chat


class MSP:
    """
    MSP (Main Service Processor) – central router for the Samarkand Soul bot.

    It receives all `msp: ...` style commands from Telegram
    and dispatches them to the correct agent, integration or tool.

    Examples:
      msp: mamos
      msp: market: pet hair remover | US
      msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
      msp: shopify: test
      msp: ds05: Samarkand Soul Ikat Tablecloth | premium home textile | ...
      msp: product: Samarkand Soul Ikat Tablecloth | warm beige ikat | 39.90 | women 28–45 EU/US
      msp: image: Samarkand Soul Ikat Tablecloth | hero image for product page | warm beige, minimalist, family dinner
      msp: gpt: Explain the Samarkand Soul brand in 3 sentences.
    """

    def __init__(self) -> None:
        # DS (Dropshipping System) agent labels (for generic demo handlers)
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
            "ds21": "PRODUCT-AUTO-CREATOR",
            "ds22": "IMAGE-AUTO-AGENT",
        }

        # LIFE agents – protect the commander (health, time, clarity)
        self.life_labels = {
            "life01": "HEALTH & HABIT-COACH",
            "life02": "NUTRITION & MEAL PLANNER",
            "life03": "FITNESS & TRAINING COACH",
            "life04": "CALENDAR & TIME ARCHITECT",
            "life05": "INFO & NEWS CURATOR",
        }

        # SYS agents – keep the ecosystem clean and evolving
        self.sys_labels = {
            "sys01": "KNOWLEDGE-LIBRARIAN",
            "sys02": "SECURITY & PRIVACY-GUARDIAN",
            "sys03": "PROCESS & SOP BUILDER",
            "sys04": "SYSTEM HEALTH & REFACTOR PLANNER",
            "sys05": "FUTURE-ROADMAP & INNOVATION-PLANNER",
        }

        # DS-02 Drive Agent – folder blueprints
        self.drive = DriveAgent()

        # TikTok Growth Agent (TGA) – content factory
        self.tga = TikTokGrowthAgent()

    # =========================
    #  MAMOS – Unified Brain
    # =========================
    def load_mamos(self) -> str:
        """
        Load the global MAMOS doctrine.

        All agents should conceptually use this to understand
        the Samarkand Soul mission, rules and discipline.
        """
        return MAMOSLoader.load_mamos()

    # =========================
    #  Helper functions
    # =========================
    @staticmethod
    def _strip_msp_prefix(raw_text: str) -> str:
        """
        Remove the 'msp:' prefix and trim whitespace.
        """
        text = (raw_text or "").strip()
        if text.lower().startswith("msp:"):
            return text[4:].strip()
        return text

    @staticmethod
    def _split_once(body: str, sep: str = "|") -> Tuple[str, str]:
        """
        Split "a | b" format into two parts.
        """
        parts = [p.strip() for p in body.split(sep, 1)]
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    # =========================
    #  TGA – TikTok Growth Agent helpers
    # =========================
    def build_tga_preview_payloads(self) -> List[Dict[str, Any]]:
        """
        Build Telegram-ready preview payloads for the TikTok Growth Agent.

        The external bot layer can use it like:

            payloads = msp.build_tga_preview_payloads()
            for p in payloads:
                bot.send_message(chat_id, **p)
        """
        return self.tga.build_telegram_preview_payloads()

    def process_callback(self, callback_data: str) -> Optional[str]:
        """
        Router for Telegram callback_data.

        Currently supports only TGA callbacks:
          - tga_approve:<draft_id>
          - tga_reject:<draft_id>
        """
        if not callback_data:
            return None

        if callback_data.startswith("tga_approve:"):
            draft_id = callback_data.split(":", 1)[1]
            self.tga.handle_telegram_approval(draft_id, approved=True)
            return "✅ Video approved. Added to posting queue."

        if callback_data.startswith("tga_reject:"):
            draft_id = callback_data.split(":", 1)[1]
            self.tga.handle_telegram_approval(draft_id, approved=False)
            return "❌ Video rejected. A new variant will be generated."

        return None  # other callback types

    # =========================
    #  Main entrypoint (text messages)
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Main entrypoint for ALL MSP *text* commands coming from Telegram.
        """
        if not raw_text:
            return "MSP error: empty message."

        text = self._strip_msp_prefix(raw_text)
        if not text:
            return "MSP error: empty MSP command."

        lowered = text.lower()

        # ==========================================================
        # 0) MAMOS – show global doctrine
        # ==========================================================
        if lowered.startswith("mamos"):
            doc = self.load_mamos()
            # Telegram has limits – show only a preview; full text lives in repo
            preview = doc[:3500]
            return "📜 MAMOS — Samarkand Soul Doctrine (preview):\n\n" + preview

        # ==========================================================
        # 1) DS-01 MARKET RESEARCH (real module)
        # ==========================================================
        if lowered.startswith("market:") or lowered.startswith("ds01:"):
            if lowered.startswith("market:"):
                body = text[len("market:"):].strip()
            else:
                body = text[len("ds01:"):].strip()

            if not body:
                return (
                    "MSP error: Market command body is empty.\n"
                    "Correct format: msp: market: Niche | Country\n"
                    "Example: msp: market: pet hair remover | US"
                )

            niche, country = self._split_once(body, "|")
            if not country:
                country = "US"

            if not niche:
                return (
                    "MSP error: Niche cannot be empty.\n"
                    "Example: msp: market: pet hair remover | US"
                )

            try:
                from app.agents.ds.ds01_market_research import (
                    analyze_market,
                    MarketResearchRequest,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: could not import DS-01 module: {e}"

            try:
                req = MarketResearchRequest(niche=niche, country=country)
                result = analyze_market(req)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-01 processing error: {e}"

            return f"DS-01 Market Research result:\n{result}"

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
                    "MSP error: Offer command body is empty.\n"
                    "Format: msp: offer: Product description | Market"
                )

            product, market = self._split_once(body, "|")
            product = product or "Unknown product"
            market = market or "Unknown market"

            return (
                "DS-04 Offer & Pricing Strategist (DEMO):\n"
                f"Product: {product}\n"
                f"Market: {market}\n\n"
                "Here, in the full version, the agent would generate ideal price ranges, "
                "bundle ideas and upsell concepts. Currently this is a structure test. 💡"
            )

        # ==========================================================
        # 3) DS-02 DRIVE AGENT (real logical layer)
        # ==========================================================
        if lowered.startswith("drive"):
            # Supported formats:
            #   msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master
            #   msp: drive SamarkandSoulSystem / DS-02 - Drive-Agent-Lab
            body = text
            if lowered.startswith("drive:"):
                body = text[len("drive:"):].strip()
            elif lowered.startswith("drive"):
                body = text[len("drive"):].strip()

            path = (body or "").strip()
            if not path:
                return (
                    "MSP error: drive path is empty.\n"
                    "Examples:\n"
                    "  msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master\n"
                    "  msp: drive SamarkandSoulSystem / DS-02 - Drive-Agent-Lab"
                )

            try:
                return self.drive.create_folder_path(path)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-02 DriveAgent failure: {e}"

        # ==========================================================
        # 3.5) SHOPIFY AGENT (DS03) — real API integration
        # ----------------------------------------------------------
        # Examples:
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

            # --- test connection ---
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
                    image_url=None,  # optional demo image URL
                )
                return create_demo_product(spec)

            # --- coming soon page ---
            if lowered_body.startswith("comingsoon"):
                return setup_coming_soon_page()

            # --- add product via text prompt ---
            if lowered_body.startswith("add"):
                # Expected format:
                #   add | Title | Price | OptionalImageURL
                after = raw_body[3:].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                return create_product_from_prompt(after)

            # --- create collection ---
            if lowered_body.startswith("collection"):
                # Format:
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
        # 3.8) DS-21 PRODUCT AUTO CREATOR
        # ----------------------------------------------------------
        # Examples:
        #   msp: product: Samarkand Soul Ikat Tablecloth | warm beige ikat, minimalist | 39.90 | women 28–45 in EU & US
        #   msp: ds21: Blue Ikat Tablecloth | deep blue pattern | 44.90 | gift-ready premium packaging
        # ==========================================================
        if lowered.startswith("product:") or lowered.startswith("ds21:"):
            if lowered.startswith("product:"):
                body = text[len("product:"):].strip()
            else:
                body = text[len("ds21:"):].strip()

            if not body:
                return (
                    "MSP error: Product command body is empty.\n"
                    "Example:\n"
                    "  msp: product: Samarkand Soul Ikat Tablecloth | warm beige ikat, minimalist | 39.90 | women 28–45 in EU & US"
                )

            parts = [p.strip() for p in body.split("|")]
            title_seed = parts[0] if len(parts) > 0 else ""
            style_brief = parts[1] if len(parts) > 1 else ""
            price_hint = parts[2] if len(parts) > 2 else ""
            extra_info = " | ".join(parts[3:]) if len(parts) > 3 else ""

            if not title_seed:
                return (
                    "MSP error: Product title seed cannot be empty.\n"
                    "Example:\n"
                    "  msp: product: Samarkand Soul Ikat Tablecloth | warm beige ikat, minimalist | 39.90 | women 28–45 in EU & US"
                )

            try:
                from app.agents.ds.ds21_product_auto_creator import (
                    ProductAutoCreator,
                    ProductIdea,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-21 module import failed: {e}"

            creator = ProductAutoCreator()
            idea = ProductIdea(
                title_seed=title_seed,
                style_brief=style_brief,
                price_hint=price_hint,
                extra_info=extra_info,
            )

            try:
                return creator.create_full_product(idea)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-21 processing error: {e}"

        # ==========================================================
        # 3.9) DS-22 IMAGE AUTO AGENT
        # ----------------------------------------------------------
        # Generates AI image prompts, shot list, filenames, alt-text
        # Examples:
        #   msp: image: Samarkand Soul Ikat Tablecloth | hero image for product page | warm beige, minimalist, family dinner
        #   msp: ds22: Blue Ikat Tablecloth | lifestyle shots for TikTok | cozy evening, candles, premium home textile
        # ==========================================================
        if lowered.startswith("image:") or lowered.startswith("ds22:"):
            if lowered.startswith("image:"):
                body = text[len("image:"):].strip()
            else:
                body = text[len("ds22:"):].strip()

            if not body:
                return (
                    "MSP error: Image command body is empty.\n"
                    "Example:\n"
                    "  msp: image: Samarkand Soul Ikat Tablecloth | hero image for product page | warm beige, minimalist, family dinner"
                )

            parts = [p.strip() for p in body.split("|")]
            product_name = parts[0] if len(parts) > 0 else ""
            use_case = parts[1] if len(parts) > 1 else ""
            style_notes = parts[2] if len(parts) > 2 else ""
            extra_info = " | ".join(parts[3:]) if len(parts) > 3 else ""

            if not product_name:
                return (
                    "MSP error: Product name for image agent cannot be empty.\n"
                    "Example:\n"
                    "  msp: image: Samarkand Soul Ikat Tablecloth | hero image for product page | warm beige, minimalist, family dinner"
                )

            try:
                from app.agents.ds.ds22_image_auto_agent import (
                    ImageAutoAgent,
                    ImageIdea,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-22 module import failed: {e}"

            agent = ImageAutoAgent()
            idea = ImageIdea(
                product_name=product_name,
                use_case=use_case,
                style_notes=style_notes,
                extra_info=extra_info,
            )

            try:
                return agent.generate_image_plan(idea)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-22 processing error: {e}"

        # ==========================================================
        # 3.6) DS-05 PRODUCT PAGE COPYWRITER (real LLM via AgentBrain)
        # ----------------------------------------------------------
        # Example:
        #   msp: ds05: Samarkand Soul Ikat Tablecloth | premium home textile | \
        #         modern minimalist women in Europe | gift-ready, table as ritual | \
        #         mention Samarkand spirit and premium packaging
        # ==========================================================
        if lowered.startswith("ds05:"):
            body = text[len("ds05:"):].strip()
            if not body:
                return (
                    "MSP error: ds05 body is empty.\n"
                    "Format:\n"
                    "  msp: ds05: Product name | Niche | Target customer | Main benefit | Extra notes\n"
                    "Example:\n"
                    "  msp: ds05: Samarkand Soul Ikat Tablecloth | premium home textile | "
                    "modern minimalist women in Europe | gift-ready, table as a ritual"
                )

            try:
                from app.agents.ds.ds05_product_page_copywriter import (
                    generate_product_page_copy_from_text,
                )
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: could not import DS-05 module: {e}"

            try:
                return generate_product_page_copy_from_text(body)
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: DS-05 processing error: {e}"

        # ==========================================================
        # 3.7) GPT / MAMOS-aware General Chat
        # ----------------------------------------------------------
        # Examples:
        #   msp: gpt: What is the Samarkand Soul brand?
        #   msp: chat: Explain our mission in 3 sentences.
        # ==========================================================
        if lowered.startswith("gpt:") or lowered.startswith("chat:"):
            if lowered.startswith("gpt:"):
                body = text[len("gpt:"):].strip()
            else:
                body = text[len("chat:"):].strip()

            if not body:
                return (
                    "MSP error: GPT command body is empty.\n"
                    "Example: msp: gpt: Explain the Samarkand Soul brand in 3 sentences."
                )

            try:
                reply = brat_gpt_chat(
                    user_prompt=body,
                    agent_role="Samarkand Soul General Agent",
                )
                return f"MSP / GPT reply:\n{reply}"
            except Exception as e:  # pylint: disable=broad-except
                return f"MSP error: GPT bridge failed: {e}"

        # ==========================================================
        # 4) GENERIC DS / LIFE / SYS COMMANDS (demo stubs)
        # ==========================================================
        if ":" in text:
            prefix, _, body = text.partition(":")
            key = prefix.strip().lower()
            query = body.strip() or "(empty query)"

            # ----- DS agents -----
            if key in self.ds_labels:
                label = self.ds_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "This agent is currently running in structure-test mode. "
                    "Later it will use real LLM + integrations. 🧠"
                )

            # ----- LIFE agents -----
            if key in self.life_labels:
                label = self.life_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "This LIFE agent is in demo mode. In the future it will generate "
                    "personal plans and recommendations."
                )

            # ----- SYS agents -----
            if key in self.sys_labels:
                label = self.sys_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n\n"
                    "This SYS agent is in structure-test mode. System knowledge and "
                    "governance plans will live here."
                )

        # ==========================================================
        # 4.5) TGA – TikTok Growth Agent text trigger
        # ==========================================================
        if lowered.startswith("tga:") or lowered.startswith("tiktok:"):
            self.tga.run_daily_cycle()
            summary = self.tga.get_text_preview_summary()
            return summary

        # ==========================================================
        # 5) UNKNOWN COMMAND
        # ==========================================================
        return (
            "MSP error: I did not recognize this MSP command.\n"
            "Possible examples:\n"
            "  • msp: mamos\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: offer: ideal pricing and bundle ideas for pet hair remover | US market\n"
            "  • msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master\n"
            "  • msp: drive SamarkandSoulSystem / DS-02 - Drive-Agent-Lab\n"
            "  • msp: ds05: Samarkand Soul Ikat Tablecloth | premium home textile | target customer ...\n"
            "  • msp: product: Samarkand Soul Ikat Tablecloth | warm beige ikat | 39.90 | women 28–45 EU/US\n"
            "  • msp: image: Samarkand Soul Ikat Tablecloth | hero image for product page | warm beige, minimalist, family dinner\n"
            "  • msp: life01: give me a health & habit plan\n"
            "  • msp: sys01: explain the system knowledge base\n"
            "  • msp: shopify: test / demo / comingsoon / add / collection\n"
            "  • msp: gpt: Explain the Samarkand Soul brand in 3 sentences\n"
            "  • msp: tga: start  (TikTok Growth Agent daily cycle)\n"
            )
