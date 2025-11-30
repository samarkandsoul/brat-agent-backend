# app/agents/core/telegram_brat_brain.py

from __future__ import annotations

from typing import Optional

from app.agents.core.msp import MSP
from app.llm.brat_gpt import brat_gpt_chat


class TelegramBratBrain:
    """
    Telegram BRAT Brain – unified dialog router for Zahid Brat.

    Məqsəd:
    - "BRAT:" / "ZAHID BRAT:" prefixlərini anlamaq
    - msp: ... və mamos komandalarını birbaşa MSP-ə yönləndirmək
    - Samarkand Soul sistem suallarında texniki, səmimi cavab vermək
    - Qalan bütün suallarda premium Brat GPT dialoq davranışı vermək
    - Normal suallara görə "ESCALATION" yazmamaq, əvəzində izah və ya sual vermək
    """

    def __init__(self) -> None:
        self.msp = MSP()

    # ------------------------------------------------------------------ #
    #  Helperlar
    # ------------------------------------------------------------------ #
    @staticmethod
    def _strip_brat_prefix(text: str) -> str:
        """
        'BRAT:' və 'ZAHID BRAT:' kimi prefiksləri təmizləyir.

        Nümunə:
            "BRAT: msp: mamos"   → "msp: mamos"
            "Zahid Brat: hava necədir?" → "hava necədir?"
        """
        if not text:
            return ""

        raw = text.strip()
        lowers = raw.lower()

        prefixes = [
            "brat:",
            "brat :",
            "zahid brat:",
            "zahid brat :",
            "brat",
            "zahid brat",
        ]

        for p in prefixes:
            if lowers.startswith(p):
                cut_len = len(p)
                return raw[cut_len:].strip()

        return raw

    @staticmethod
    def _is_msp_command(text: str) -> bool:
        """
        Mətni MSP/mamos kimi qəbul etmək olarmı?
        """
        if not text:
            return False

        t = text.strip().lower()

        # "msp: ..." və ya "msp ..." və ya tək "msp"
        if t.startswith("msp:") or t.startswith("msp "):
            return True

        # Birbaşa "mamos" yazılıbsa, onu da MSP-ə ötürürük
        if t.startswith("mamos"):
            return True

        return False

    @staticmethod
    def _looks_like_weather_question(text: str) -> bool:
        if not text:
            return False
        lower = text.lower()
        return "hava" in lower or "weather" in lower

    @staticmethod
    def _looks_like_shopify_sales_question(text: str) -> bool:
        if not text:
            return False
        lower = text.lower()
        if "shopify" not in lower:
            return False
        return any(
            kw in lower
            for kw in ["satış", "sales", "satis", "conversion", "məhsul səhifəsi", "product page"]
        )

    # ------------------------------------------------------------------ #
    #  Internal helpers for special domains
    # ------------------------------------------------------------------ #
    def _answer_weather(self, text: str) -> str:
        """
        Hava haqda sual üçün dürüst, sistemə uyğun cavab.
        """
        return (
            "Zahid Brat, bizim hazırkı Samarkand Soul agent backend-ində "
            "hava proqnozu üçün ayrıca servis qoşulmayıb – yəni real API-dən "
            "hava məlumatı çəkə bilmirik.\n\n"
            "Bu nə deməkdir?\n"
            "- Telegram BRAT beyni hazırda Shopify, MAMOS, DS/LIFE/SYS agentləri və s. ilə "
            "işləmək üçün qurulub.\n"
            "- Hava proqnozu üçün ayrıca *Weather-Agent* və xarici API qoşmaq lazımdır.\n\n"
            "Yəni indi ən praktik variant: telefonundakı hava tətbiqinə və ya brauzerdə hava saytına baxırsan. "
            "Biz isə gələcəkdə istəsən DS/SYS xəritəsinə Weather-Agent əlavə edib bu hissəni də tam avtomatlaşdırarıq. 🌦"
        )

    def _answer_shopify_sales(self, text: str) -> str:
        """
        Shopify satış sualı – real metrikləri hələ oxumuruq, ona görə
        vəziyyəti səmimi izah edir və növbəti addımı göstərir.
        """
        return (
            "Zahid Brat, Shopify məhsul səhifəsində SATIŞ necə gedir sualı artıq "
            "DS-12 / Analytics və real Shopify API oxuma səviyyəsinə girir.\n\n"
            "Hazır vəziyyət:\n"
            "- DS03 Shopify Agent məhsul yaratmaq, struktur qurmaq, səhifə kontentini yeniləmək üçündür.\n"
            "- Shopify satış metrikləri (order sayı, conversion rate, add-to-cart və s.) üçün ayrıca "
            "analytics layer hələ qoşulmayıb.\n\n"
            "Növbəti mərhələ üçün plan belə olmalıdır:\n"
            "1️⃣ DS-12 KPI & Analytics Agent üçün rəsmi MAMOS doktrina (C2_12_KPI_Analytics.md) aktivləşdirilir.\n"
            "2️⃣ Shopify Admin API-dən raport/metrics oxuyan ayrıca modul yazılır (məs., `/shopify/analytics/...`).\n"
            "3️⃣ MSP-ə belə komanda əlavə edilir:\n"
            "    `msp: analytics: shopify | product=Samarkand Soul Demo Tablecloth`\n"
            "4️⃣ Telegram BRAT bu komandanı DS-12 agentə yönləndirib real rəqəmlə cavab verir.\n\n"
            "Yəni qısa cavab: hazırda sistem sənin Shopify-də *satışları oxumaq* gücündə deyil, "
            "amma memarlıq artıq agent səviyyəsində hazırdır – növbəti texniki addım metrikləri oxuyan kodu yazmaqdır. 📊"
        )

    # ------------------------------------------------------------------ #
    #  Main entrypoint
    # ------------------------------------------------------------------ #
    def process(self, raw_text: str) -> str:
        """
        Telegram-dan gələn hər mesaj üçün əsas giriş nöqtəsi.
        """
        if not raw_text:
            return (
                "Zahid Brat, boş mesaj gəldi. "
                "Zəhmət olmasa sualını və ya komandanı yaz. 🙂"
            )

        # 1) BRAT / ZAHID BRAT prefiksini təmizlə
        text = self._strip_brat_prefix(raw_text)
        if not text:
            return (
                "Zahid Brat, mətn tapa bilmədim. "
                "Bir cümlə ilə də olsa yaz, mən davamını həll edim. 🙂"
            )

        lowered = text.lower().strip()

        # 2) Əgər bu MSP/MAMOS tipli komandadırsa → birbaşa MSP-ə yönləndir
        if self._is_msp_command(text):
            try:
                response = self.msp.process(text)
                # Kiçik imza ki, həqiqətən bu beyin MSP cavabını qaytarır
                return f"🧠 BRAT · MSP cavabı:\n{response}"
            except Exception as e:  # noqa: BLE001
                return (
                    "ESCALATION\n"
                    f"Reason: MSP processing error: {e}\n"
                    "Action: Human validation required.\n"
                )

        # 3) Hava sualı → öz xüsusi cavabımız
        if self._looks_like_weather_question(text):
            return self._answer_weather(text)

        # 4) Shopify satış sualı → öz xüsusi cavabımız
        if self._looks_like_shopify_sales_question(text):
            return self._answer_shopify_sales(text)

        # 5) Qalan bütün suallar → premium Brat GPT dialoqa göndər
        dialog_prompt = (
            "You are GPT BRAT, the personal AI co-founder and Telegram assistant of "
            "Zahid Brat for the Samarkand Soul brand.\n\n"
            "Context:\n"
            "- Brand tone: premium calm luxury, honest, minimal, non-clickbait.\n"
            "- You operate inside a Telegram bot as 'BRAT'.\n"
            "- There is a separate MSP command router that handles `msp:` and system agents.\n\n"
            "Critical rules for THIS TELEGRAM DIALOG ROLE:\n"
            "1. Do NOT answer with 'ESCALATION' for normal user questions.\n"
            "2. If the question is unclear or missing key info, ask ONE short clarifying question instead of refusing.\n"
            "3. Be concrete, practical and system-aware: you know about Samarkand Soul, MAMOS, DS/LIFE/SYS agents, Render, GitHub, Shopify, etc.\n"
            "4. Always answer in the same language as the user (here: Azerbaijani is primary, with English tech terms allowed).\n"
            "5. Keep answers focused; no unnecessary long intros.\n\n"
            f"User message:\n{text}\n"
        )

        try:
            reply = brat_gpt_chat(
                user_prompt=dialog_prompt,
                agent_role="Telegram BRAT Dialog Brain",
            )
            # Kiçik imza ilə – bunu görürüksə, demək BRAT beyni işləyir
            return f"🧠 BRAT · {reply}"
        except Exception as e:  # noqa: BLE001
            return (
                "ESCALATION\n"
                f"Reason: Internal GPT error: {e}\n"
                "Action: Human validation required.\n"
        )
