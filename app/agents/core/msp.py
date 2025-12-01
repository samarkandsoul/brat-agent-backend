from typing import Tuple, List, Dict, Any, Optional

# MAMOS: loader path fixed (force redeploy marker)

# TikTok Growth brain
from app.agents.tiktok_growth.TGA_Main_Brain_manager import TikTokGrowthAgent

# DS-02 Drive Agent
from app.agents.ds.ds02_drive_agent import DriveAgent

# MAMOS – unified doctrine loader
from app.mamos.MAMOS.mamos_loader import MAMOSLoader

# Brat GPT – unified LLM interface (MAMOS-aware)
from app.llm.brat_gpt import brat_gpt_chat


class MSP:
    """
    MSP (Main Service Processor) – central router for the Samarkand Soul bot.

    All `msp: ...` style commands from Telegram pass through here and are
    routed to the correct agent / integration.
    """

    def __init__(self) -> None:
        # DS (Dropshipping System) agent labels (for demo handlers)
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
            "ds23": "TIKTOK-VIDEO-AUTO-AGENT",
        }

        # LIFE agents – protect commander (health, time, focus)
        self.life_labels = {
            "life01": "HEALTH & HABIT-COACH",
            "life02": "NUTRITION & MEAL PLANNER",
            "life03": "FITNESS & TRAINING COACH",
            "life04": "CALENDAR & TIME ARCHITECT",
            "life05": "INFO & NEWS CURATOR",
        }

        # SYS agents – keep the system clean and evolving
        self.sys_labels = {
            "sys01": "KNOWLEDGE-LIBRARIAN",
            "sys02": "SECURITY & PRIVACY-GUARDIAN",
            "sys03": "PROCESS & SOP BUILDER",
            "sys04": "SYSTEM HEALTH & REFACTOR PLANNER",
            "sys05": "FUTURE-ROADMAP & INNOVATION-PLANNER",
        }

        # DS-02 Drive Agent – Google Drive folder blueprints
        self.drive = DriveAgent()

        # TikTok Growth Agent (TGA) – content factory
        self.tga = TikTokGrowthAgent()

    # =========================
    #  MAMOS – Unified Brain
    # =========================
    def load_mamos(self) -> str:
        """
        Load the global Samarkand Soul doctrine (MAMOS).
        """
        return MAMOSLoader.load_mamos()

    # =========================
    #  Helper functions
    # =========================
    @staticmethod
    def _strip_msp_prefix(raw_text: str) -> str:
        """
        Remove 'msp:' prefix and trim whitespace.
        """
        text = (raw_text or "").strip()
        if text.lower().startswith("msp:"):
            return text[4:].strip()
        return text

    @staticmethod
    def _split_once(body: str, sep: str = "|") -> Tuple[str, str]:
        """
        Simple helper to split "a | b" into two pieces.
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
        Build Telegram preview payloads for TGA drafts.
        """
        return self.tga.build_telegram_preview_payloads()

    def process_callback(self, callback_data: str) -> Optional[str]:
        """
        Telegram callback_data router (currently only for TGA).
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
        Main entrypoint for ALL text coming from Telegram.
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

            # Əgər loader error qaytardısa, preview əvəzinə xətanı göstər
            if isinstance(doc, str) and doc.startswith("[MAMOS ERROR]"):
                return "📜 MAMOS — Samarkand Soul Doctrine (error):\n\n" + doc

            preview = doc[:3500]
            return "📜 MAMOS — Samarkand Soul Doctrine (preview):\n\n" + preview

        # ==========================================================
        # 0.5) DAILY REPORT AGENT (sales + life + system)
        # ==========================================================
        if lowered.startswith("daily"):
            # Lokal import – circular riskini öldürmək üçün
            from app.reports.daily_report_service import (
                generate_daily_report_text,
                send_daily_report_via_telegram,
            )

            # Accept both:
            #   msp: daily: report
            #   msp: daily report
            after = text[len("daily"):].strip()
            if after.startswith(":"):
                after = after[1:].strip()
            sub = after.lower()

            # default: "report" -> return formatted text
            if sub in ("", "report", "text"):
                try:
                    rep_text = generate_daily_report_text()
                    return rep_text
                except Exception as e:  # noqa: BLE001
                    return f"MSP error: daily report generation failed: {e}"

            # "send" -> push to Telegram via backend service
            if sub == "send":
                try:
                    ok = send_daily_report_via_telegram()
                    if ok:
                        return "✅ Daily report sent to Telegram (DEFAULT_CHAT_ID)."
                    return (
                        "❌ Daily report FAILED to send.\n"
                        "Check DEFAULT_CHAT_ID env var and Telegram bot config."
                    )
                except Exception as e:  # noqa: BLE001
                    return f"MSP error: daily report send failed: {e}"

            return (
                "Daily agent commands:\n"
                "  • msp: daily: report   → show formatted daily report here\n"
                "  • msp: daily: send     → send daily report to Telegram chat"
            )

        # ==========================================================
        # 0.6) MORNING PLAN AGENT (commander focus plan)
        # ==========================================================
        if lowered.startswith("morning"):
            # Lokal import – circular-dan qaçmaq üçün
            from app.reports.morning_plan_service import (
                generate_morning_plan_text,
                send_morning_plan_via_telegram,
            )

            # Accept:
            #   msp: morning: plan
            #   msp: morning plan
            #   msp: morning: send
            after = text[len("morning"):].strip()
            if after.startswith(":"):
                after = after[1:].strip()
            sub = after.lower()

            if sub in ("", "plan", "text", "preview"):
                try:
                    plan_text = generate_morning_plan_text()
                    return plan_text
                except Exception as e:  # noqa: BLE001
                    return f"MSP error: morning plan generation failed: {e}"

            if sub == "send":
                try:
                    ok = send_morning_plan_via_telegram()
                    if ok:
                        return "✅ Morning plan sent to Telegram (DEFAULT_CHAT_ID)."
                    return (
                        "❌ Morning plan FAILED to send.\n"
                        "Check DEFAULT_CHAT_ID env var and Telegram bot config."
                    )
                except Exception as e:  # noqa: BLE001
                    return f"MSP error: morning plan send failed: {e}"

            return (
                "Morning agent commands:\n"
                "  • msp: morning: plan   → show morning focus plan here\n"
                "  • msp: morning: send   → send morning plan to Telegram chat"
            )

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
            except Exception as e:  # pylint: disable-broad-except
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
            # Examples:
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
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: DS-02 DriveAgent failure: {e}"

        # ==========================================================
        # 3.5) SHOPIFY AGENT (DS03) — real API integration
        # ==========================================================
        if lowered.startswith("shopify:"):
            raw_body = text[len("shopify:"):].strip()
            lowered_body = raw_body.lower()

            try:
                from app.integrations.shopify_client import (
                    test_shopify_connection,
                    create_demo_product,
                    setup_coming_soon_product,
                    ShopifyDemoProductSpec,
                    create_product_from_prompt,
                    create_collection,
                    setup_basic_store_structure,
                    autods_search_stub,
                    overwrite_page_html,
                )
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: Shopify integration import failed: {e}"

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
                    image_url=None,
                )
                return create_demo_product(spec)

            # --- coming soon product ---
            if lowered_body.startswith("comingsoon"):
                return setup_coming_soon_product()

            # --- add product via text prompt ---
            if lowered_body.startswith("add"):
                # Format:
                #   msp: shopify: add | Title | Price | OptionalImageURL
                after = raw_body[3:].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                return create_product_from_prompt(after)

            # --- create collection ---
            if lowered_body.startswith("collection"):
                #   msp: shopify: collection | Samarkand Soul Premium Tablecloths
                after = raw_body[len("collection"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                return create_collection(after or "Samarkand Soul Collection")

            # --- basic store structure (core pages) ---
            if lowered_body.startswith("structure_basic"):
                return setup_basic_store_structure()

            # --- update single page via GPT (legal / about / shipping etc.) ---
            if lowered_body.startswith("update_page"):
                # Format:
                #   msp: shopify: update_page | privacy-policy | <Brief text>
                after = raw_body[len("update_page"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()

                if not after:
                    return (
                        "MSP error: update_page body is empty.\n"
                        "Format:\n"
                        "  msp: shopify: update_page | privacy-policy | Brief for GPT\n"
                        "Example:\n"
                        "  msp: shopify: update_page | terms-of-service | Full legal ToS for Samarkand Soul..."
                    )

                parts = [p.strip() for p in after.split("|", 1)]
                if len(parts) < 2 or not parts[0] or not parts[1]:
                    return (
                        "MSP error: update_page requires: handle | brief.\n"
                        "Example:\n"
                        "  msp: shopify: update_page | terms-of-service | Full legal ToS for Samarkand Soul..."
                    )

                handle = parts[0].lower()
                brief = parts[1]

                # HTML is generated via GPT, then pushed to Shopify
                try:
                    gpt_prompt = (
                        "You are the official content & legal page writer for the Samarkand Soul Shopify store.\n"
                        f"Page handle: {handle}\n"
                        "Write clean HTML content using <h2>, <h3>, <p>, <ul>, <li> tags.\n"
                        "Do NOT include <html>, <head> or <body> tags – only inner HTML.\n"
                        "The brand: Samarkand Soul – premium, calm luxury, handmade-style home textiles.\n"
                        f"Brief from commander:\n{brief}\n\n"
                        "Return ONLY the HTML, nothing else."
                    )
                    html = brat_gpt_chat(
                        user_prompt=gpt_prompt,
                        agent_role="Samarkand Soul Shopify Page Writer",
                    )
                except Exception as e:  # pylint: disable-broad-except
                    return f"MSP error: GPT bridge failed inside update_page: {e}"

                return overwrite_page_html(handle, html)

            # --- AutoDS stub (future real integration) ---
            if lowered_body.startswith("autods"):
                #   msp: shopify: autods | tablecloth niche
                after = raw_body[len("autods"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                niche = after or "general niche"
                return autods_search_stub(niche)

            # Default help for shopify agent
            return (
                "Shopify agent commands:\n"
                "  • msp: shopify: test\n"
                "  • msp: shopify: demo\n"
                "  • msp: shopify: comingsoon\n"
                "  • msp: shopify: add | Title | Price | OptionalImageURL\n"
                "  • msp: shopify: collection | Collection Name\n"
                "  • msp: shopify: structure_basic\n"
                "  • msp: shopify: update_page | handle | brief\n"
                "  • msp: shopify: autods | niche\n"
            )

        # ==========================================================
        # 3.55) WEB RESEARCH AGENT — Internet access
        # ==========================================================
        if lowered.startswith("web:"):
            raw_body = text[len("web:"):].strip()
            lowered_body = raw_body.lower()

            try:
                from app.integrations.web_research_client import (
                    fetch_url,
                    format_search_results,
                )
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: web_research_client import failed: {e}"

            # --- web: search | query ---
            if lowered_body.startswith("search"):
                after = raw_body[len("search"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                query = after or ""
                if not query:
                    return (
                        "WEB error: Missing query.\n"
                        "Format: msp: web: search | keyword"
                    )
                return format_search_results(query)

            # --- web: fetch | URL ---
            if lowered_body.startswith("fetch"):
                after = raw_body[len("fetch"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()
                url = after or ""
                if not url:
                    return (
                        "WEB error: Missing URL.\n"
                        "Format: msp: web: fetch | https://example.com"
                    )
                return fetch_url(url)

            # Default help for web agent
            return (
                "Web Research commands:\n"
                "  • msp: web: search | keyword\n"
                "  • msp: web: fetch | https://example.com\n"
            )

        # ==========================================================
        # 3.56) GMAIL AGENT — read & send email
        # ==========================================================
        if lowered.startswith("gmail:"):
            raw_body = text[len("gmail:"):].strip()
            lowered_body = raw_body.lower()

            try:
                from app.integrations.google_client import (
                    list_recent_emails,
                    send_email,
                    GoogleClientError,
                )
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: google_client import failed: {e}"

            # --- gmail: unread | 5  / gmail: recent | 10 ---
            if lowered_body.startswith("unread") or lowered_body.startswith("recent"):
                count = 5
                parts = raw_body.split("|", 1)
                if len(parts) == 2:
                    try:
                        count = int(parts[1].strip())
                    except ValueError:
                        pass

                query = "is:unread" if lowered_body.startswith("unread") else ""
                try:
                    emails = list_recent_emails(max_results=count, query=query)
                except GoogleClientError as e:
                    return f"GMAIL error: {e}"

                if not emails:
                    return "📥 Gmail: uyğun məktub tapılmadı."

                lines: List[str] = ["📥 *Gmail — son məktublar:*"]
                for idx, msg in enumerate(emails, start=1):
                    from_f = msg.get("from", "")
                    subject = msg.get("subject", "")
                    date = msg.get("date", "")
                    snippet = msg.get("snippet", "")
                    lines.append(
                        f"{idx}. *{subject}*\n"
                        f"   From: `{from_f}`\n"
                        f"   Date: `{date}`\n"
                        f"   Snippet: {snippet}"
                    )
                return "\n".join(lines)

            # --- gmail: send | to@example.com | Subject | Body text ---
            if lowered_body.startswith("send"):
                after = raw_body[len("send"):].strip()
                if after.startswith("|"):
                    after = after[1:].strip()

                parts = [p.strip() for p in after.split("|")]
                if len(parts) < 3:
                    return (
                        "GMAIL send formatı:\n"
                        "  msp: gmail: send | to@example.com | Subject | Body text"
                    )

                to_email = parts[0]
                subject = parts[1]
                body_text = parts[2]

                try:
                    msg_id = send_email(
                        to_email=to_email,
                        subject=subject,
                        body_text=body_text,
                    )
                except GoogleClientError as e:
                    return f"GMAIL send error: {e}"

                return f"📧 Gmail: məktub göndərildi. ID: `{msg_id}`"

            # --- help ---
            return (
                "Gmail agent komandaları:\n"
                "  • msp: gmail: unread | 5\n"
                "  • msp: gmail: recent | 10\n"
                "  • msp: gmail: send | to@example.com | Subject | Body text\n"
            )

        # ==========================================================
        # 3.57) CALENDAR AGENT — upcoming events
        # ==========================================================
        if lowered.startswith("calendar:") or lowered.startswith("cal:"):
            if lowered.startswith("calendar:"):
                raw_body = text[len("calendar:"):].strip()
            else:
                raw_body = text[len("cal:"):].strip()

            lowered_body = raw_body.lower()

            try:
                from app.integrations.google_client import (
                    list_upcoming_events,
                    GoogleClientError,
                )
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: google_client import failed: {e}"

            if lowered_body.startswith("upcoming") or lowered_body.startswith("today"):
                count = 5
                parts = raw_body.split("|", 1)
                if len(parts) == 2:
                    try:
                        count = int(parts[1].strip())
                    except ValueError:
                        pass

                try:
                    events = list_upcoming_events(max_results=count)
                except GoogleClientError as e:
                    return f"CALENDAR error: {e}"

                if not events:
                    return "📅 Calendar: yaxın vaxtda event yoxdur."

                lines: List[str] = ["📅 *Google Calendar — upcoming events:*"]
                for ev in events:
                    summary = ev.get("summary", "(no title)")
                    start = (
                        ev.get("start", {}).get("dateTime")
                        or ev.get("start", {}).get("date")
                        or ""
                    )
                    end = (
                        ev.get("end", {}).get("dateTime")
                        or ev.get("end", {}).get("date")
                        or ""
                    )
                    location = ev.get("location", "") or "-"

                    lines.append(
                        f"- *{summary}*\n"
                        f"   When: `{start}` → `{end}`\n"
                        f"   Location: {location}"
                    )

                return "\n".join(lines)

            # --- help ---
            return (
                "Calendar agent komandaları:\n"
                "  • msp: calendar: upcoming | 5\n"
                "  • msp: cal: today | 10\n"
            )

        # ==========================================================
        # 3.58) INTEL / WEB-CORE-01 — central web search brain
        # ==========================================================
        if lowered.startswith("intel:") or lowered.startswith("news:"):
            if lowered.startswith("intel:"):
                body = text[len("intel:"):].strip()
            else:
                body = text[len("news:"):].strip()

            if not body:
                return (
                    "Intel agent commands:\n"
                    "  • msp: intel: today world news\n"
                    "  • msp: news: ecommerce trends for tablecloth niche\n"
                )

            try:
                from app.intel.web_core import WebCoreAgent, IntelSearchRequest
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: WEB-CORE-01 import failed: {e}"

            agent = WebCoreAgent()
            req = IntelSearchRequest(
                query=body,
                intent_tags=["INTEL", "NEWS"],
            )

            try:
                result = agent.route(req)
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: WEB-CORE-01 routing failed: {e}"

            lines: List[str] = []
            lines.append("🛰 *WEB-CORE-01 — Intel summary*")
            lines.append("")
            lines.append(result.summary)
            lines.append("")

            if result.bullets:
                for b in result.bullets:
                    lines.append(f"- {b}")
                lines.append("")

            if result.action_items:
                lines.append("Next steps:")
                for a in result.action_items:
                    lines.append(f"  • {a}")
                lines.append("")

            if result.sources:
                lines.append("Sources:")
                for s in result.sources[:3]:
                    title = s.title or s.url
                    provider = f" [{s.provider}]" if s.provider else ""
                    lines.append(f"  • {title}{provider}")

            return "\n".join(lines)

        # ==========================================================
        # 3.8) DS-21 PRODUCT AUTO CREATOR
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
            except Exception as e:  # pylint: disable-broad-except
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
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: DS-21 processing error: {e}"

        # ==========================================================
        # 3.9) DS-22 IMAGE AUTO AGENT
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
            except Exception as e:  # pylint: disable-broad-except
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
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: DS-22 processing error: {e}"

        # ==========================================================
        # 3.6) DS-05 PRODUCT PAGE COPYWRITER
        # ==========================================================
        if lowered.startswith("ds05:"):
            body = text[len("ds05:"):].strip()
            if not body:
                return (
                    "MSP error: ds05 body is empty.\n"
                    "Format:\n"
                    "  msp: ds05: Product name | Niche | Target customer | Main benefit | Extra notes\n"
                )

            try:
                from app.agents.ds.ds05_product_page_copywriter import (
                    generate_product_page_copy_from_text,
                )
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: could not import DS-05 module: {e}"

            try:
                return generate_product_page_copy_from_text(body)
            except Exception as e:  # pylint: disable-broad-except
                return f"MSP error: DS-05 processing error: {e}"

        # ==========================================================
        # 3.7) GPT / MAMOS-aware General Chat
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
            except Exception as e:  # pylint: disable-broad-except
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
                    f"Input: {query}\n"
                    "This agent is currently running in structure-test mode. "
                    "Later it will use real LLM + integrations. 🧠"
                )

            # ----- LIFE agents -----
            if key in self.life_labels:
                label = self.life_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n"
                    "This LIFE agent is in demo mode. In the future it will generate "
                    "personal plans and recommendations."
                )

            # ----- SYS agents -----
            if key in self.sys_labels:
                label = self.sys_labels[key]
                return (
                    f"{key.upper()} — {label} (DEMO):\n"
                    f"Input: {query}\n"
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
            "  • msp: shopify: test / demo / comingsoon / add / collection / structure_basic / update_page / autods\n"
            "  • msp: web: search | keyword\n"
            "  • msp: web: fetch | https://example.com\n"
            "  • msp: gmail: unread | 5\n"
            "  • msp: calendar: upcoming | 5\n"
            "  • msp: intel: today world news\n"
            "  • msp: news: ecommerce trends for tablecloth niche\n"
            "  • msp: gpt: Explain the Samarkand Soul brand in 3 sentences\n"
            "  • msp: tga: start  (TikTok Growth Agent daily cycle)\n"
            )
