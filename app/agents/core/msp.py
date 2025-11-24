from typing import Tuple
import importlib


class MSP:
    """
    MSP (Main Service Processor)
    'msp: ...' tipli komandaları uyğun agenta yönləndirən router.
    """

    def __init__(self) -> None:
        # DS, LIFE və SYS agent xəritələri
        self.ds_agents = {
            "ds02": ("app.agents.ds.ds02_drive_agent", "DS02DriveAgent"),
            "ds03": ("app.agents.ds.ds03_shopify_agent", "DS03ShopifyAgent"),
            "ds04": ("app.agents.ds.ds04_offer_pricing", "DS04OfferPricingAgent"),
            "ds05": ("app.agents.ds.ds05_product_page_copywriter", "DS05ProductPageCopywriter"),
            "ds06": ("app.agents.ds.ds06_creative_scriptwriter", "DS06CreativeScriptwriterAgent"),
            "ds07": ("app.agents.ds.ds07_ad_angles_hooks_master", "DS07AdAnglesHooksMasterAgent"),
            "ds08": ("app.agents.ds.ds08_image_visual_brief_creator", "DS08ImageVisualBriefCreatorAgent"),
            "ds09": ("app.agents.ds.ds09_store_structure_planner", "DS09StoreStructurePlannerAgent"),
            "ds10": ("app.agents.ds.ds10_checkout_funnel_optimizer", "DS10CheckoutFunnelOptimizerAgent"),
            "ds11": ("app.agents.ds.ds11_email_sms_flows_planner", "DS11EmailSMSFlowsPlannerAgent"),
            "ds12": ("app.agents.ds.ds12_kpi_analytics_analyst", "DS12KPIAnalyticsAnalystAgent"),
            "ds13": ("app.agents.ds.ds13_meta_ads_strategist", "DS13MetaAdsStrategistAgent"),
            "ds14": ("app.agents.ds.ds14_tiktok_ads_strategist", "DS14TiktokAdsStrategistAgent"),
            "ds15": ("app.agents.ds.ds15_influencer_ugc_strategist", "DS15InfluencerUGCStrategistAgent"),
            "ds16": ("app.agents.ds.ds16_customer_support_playbook_writer", "DS16CustomerSupportPlaybookWriterAgent"),
            "ds17": ("app.agents.ds.ds17_policy_risk_guard", "DS17PolicyRiskGuardAgent"),
            "ds18": ("app.agents.ds.ds18_supplier_logistics_planner", "DS18SupplierLogisticsPlannerAgent"),
            "ds19": ("app.agents.ds.ds19_scale_exit_strategist", "DS19ScaleExitStrategistAgent"),
            "ds20": ("app.agents.ds.ds20_experiments_ab_testing_lab", "DS20ExperimentsABTestingLabAgent"),
        }

        self.life_agents = {
            "life01": ("app.agents.life.life01_health_habit_coach", "LIFE01HealthHabitCoachAgent"),
            "life02": ("app.agents.life.life02_nutrition_meal_planner", "LIFE02NutritionMealPlannerAgent"),
            "life03": ("app.agents.life.life03_fitness_training_coach", "LIFE03FitnessTrainingCoachAgent"),
            "life04": ("app.agents.life.life04_calendar_time_architect", "LIFE04CalendarTimeArchitectAgent"),
            "life05": ("app.agents.life.life05_info_news_curator", "LIFE05InfoNewsCuratorAgent"),
        }

        self.sys_agents = {
            "sys01": ("app.agents.sys.sys01_knowledge_librarian", "SYS01KnowledgeLibrarianAgent"),
            "sys02": ("app.agents.sys.sys02_security_privacy_guardian", "SYS02SecurityPrivacyGuardianAgent"),
            "sys03": ("app.agents.sys.sys03_process_sop_builder", "SYS03ProcessSOPBuilderAgent"),
            "sys04": ("app.agents.sys.sys04_system_health_refactor_planner", "SYS04SystemHealthRefactorPlannerAgent"),
            "sys05": ("app.agents.sys.sys05_future_roadmap_innovation_planner", "SYS05FutureRoadmapInnovationPlannerAgent"),
        }

    # =========================
    #  Helper-lər
    # =========================
    @staticmethod
    def _strip_msp_prefix(raw_text: str) -> str:
        text = (raw_text or "").strip()
        if text.lower().startswith("msp:"):
            return text[4:].strip()
        return text

    @staticmethod
    def _split_once(body: str, sep: str = "|") -> Tuple[str, str]:
        parts = [p.strip() for p in body.split(sep, 1)]
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    def _call_agent(self, module_path: str, class_name: str, query: str, label: str) -> str:
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            agent = cls()
            return agent.run(query)
        except Exception as e:
            return f"MSP error ({label}): {e}"

    # =========================
    #  Main entrypoint
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP komandaları üçün giriş.
        Nümunələr:
          - msp: market: pet hair remover | US
          - msp: ds05: product page yaz
          - msp: life01: sağlamlıq planı ver
          - msp: sys01: bilik bazasını izah et
        """
        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = self._strip_msp_prefix(raw_text)
        if not text:
            return "MSP error: boş MSP komandası."

        lowered = text.lower()

        # ----------------------------------------------------------
        #  DS-01 — MARKET (xüsusi format)
        # ----------------------------------------------------------
        if lowered.startswith("market:") or lowered.startswith("ds01:"):
            if lowered.startswith("market:"):
                body = text[len("market:"):].strip()
            else:
                body = text[len("ds01:"):].strip()

            if not body:
                return (
                    "MSP error: Market komandasının gövdəsi boşdur.\n"
                    "Format: msp: market: Niche | Country"
                )

            niche, country = self._split_once(body, "|")
            if not country:
                country = "US"

            if not niche:
                return "MSP error: Niche boş ola bilməz."

            try:
                from app.agents.ds.ds01_market_research import (
                    analyze_market,
                    MarketResearchRequest,
                )
            except Exception as e:
                return f"MSP error: DS-01 modul import xətası: {e}"

            try:
                req = MarketResearchRequest(niche=niche, country=country)
                result = analyze_market(req)
                return f"DS-01 Market Research nəticəsi:\n{result}"
            except Exception as e:
                return f"MSP error: DS-01 işləmə xətası: {e}"

        # ----------------------------------------------------------
        #  DRIVE DEMO
        # ----------------------------------------------------------
        if lowered.startswith("drive:"):
            path = text[len("drive:"):].strip()
            if not path:
                return "MSP error: drive path boşdur."

            return (
                "Drive DEMO cavabı:\n"
                f"- Path: {path}\n\n"
                "Burada normalda Google Drive qovluq strukturu yaradılacaq."
            )

        # ----------------------------------------------------------
        #  GENERIC DS / LIFE / SYS komanda forması
        #  Formatlar:
        #    msp: ds05: ...
        #    msp: life01: ...
        #    msp: sys01: ...
        # ----------------------------------------------------------
        if ":" in text:
            prefix, _, body = text.partition(":")
            key = prefix.strip().lower()
            query = body.strip()

            # DS
            if key in self.ds_agents:
                module_path, class_name = self.ds_agents[key]
                return self._call_agent(module_path, class_name, query, key)

            # LIFE
            if key in self.life_agents:
                module_path, class_name = self.life_agents[key]
                return self._call_agent(module_path, class_name, query, key)

            # SYS
            if key in self.sys_agents:
                module_path, class_name = self.sys_agents[key]
                return self._call_agent(module_path, class_name, query, key)

        # ----------------------------------------------------------
        #  UNKNOWN
        # ----------------------------------------------------------
        return (
            "MSP error: bu MSP komandasını tanımadım.\n"
            "Nümunələr:\n"
            "  • msp: market: pet hair remover | US\n"
            "  • msp: ds05: product page copy yaz pet hair remover üçün\n"
            "  • msp: life01: sağlamlıq və vərdiş planı ver\n"
            "  • msp: sys01: sistem bilik bazası haqqında izah et\n"
            )
