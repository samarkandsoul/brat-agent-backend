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
    - msp: ... komandalarını birbaşa MSP-ə yönləndirmək
    - "mamos" suallarını düzgün açmaq
    - sadə qeyri-müəyyən suallarda (hava, Shopify məhsulu və s.) əvvəlcə
      dəqiqləşdirici sual vermək
    - qalan bütün sualları premium GPT dialoqa yönləndirmək
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
                # Nə qədər hissəni atacağımızı tapırıq
                cut_len = len(p)
                return raw[cut_len:].strip()

        return raw

    @staticmethod
    def _is_msp_command(text: str) -> bool:
        """
        Mətni MSP kimi qəbul etmək olar?
        """
        if not text:
            return False

        t = text.strip().lower()

        # "msp: ..." və ya "msp ..." və ya tək "msp"
        if t.startswith("msp:") or t.startswith("msp "):
            return True

        # Birbaşa "mamos" və ya "msp mamos" kimi halları da MSP-ə buraxa bilərik
        if t.startswith("mamos"):
            return True

        return False

    @staticmethod
    def _needs_weather_clarification(text: str) -> bool:
        """
        Hava ilə bağlı sual olsa da şəhər qeyd olunmayıbsa, soruşaq.
        Çox sadə heuristic.
        """
        if not text:
            return False

        lower = text.lower()

        # Azərbaycan + İngilis:
        has_weather_word = (
            "hava" in lower
            or "weather" in lower
        )

        # şəhər adları – sadə check (bakı, bəri, daşkənd və s. genişlənə bilər)
        known_cities = [
            "baki",
            "baku",
            "tashkent",
            "daşkənd",
            "istanbul",
            "london",
            "new york",
        ]

        if not has_weather_word:
            return False

        if any(city in lower for city in known_cities):
            return False

        return True

    @staticmethod
    def _needs_shopify_product_clarification(text: str) -> bool:
        """
        Shopify məhsul sualı var, amma konkret məhsul adı yoxdur → dəqiqləşdirmə ver.
        """
        if not text:
            return False

        lower = text.lower()

        if "shopify" not in lower:
            return False

        # Satış, məhsul, page və s. keçirsə amma konkret ad / id yoxdursa
        has_product_context = any(
            kw in lower
            for kw in ["məhsul", "product", "page", "satış", "sales"]
        )

        if not has_product_context:
            return False

        # çox sadə heuristic – konkret məhsul adlarını və ya id-ləri tapmağa çalışmırıq
        return True

    # ------------------------------------------------------------------ #
    #  Main entrypoint
    # ------------------------------------------------------------------ #
    def process(self, raw_text: str) -> str:
        """
        Telegram-dan gələn hər mesaj üçün əsas giriş nöqtəsi.
        """
        if not raw_text:
            return "Zahid Brat, boş mesaj gəldi. Zəhmət olmasa sualını və ya komandanı yaz. 🙂"

        # 1) BRAT / ZAHID BRAT prefiksini təmizlə
        text = self._strip_brat_prefix(raw_text)
        if not text:
            return "Zahid Brat, mətn tapa bilmədim. Bir cümlə ilə də olsa yaz, mən davamını həll edim. 🙂"

        lowered = text.lower().strip()

        # 2) Əgər bu MSP/mamos tipli komandadırsa → birbaşa MSP-ə yönləndir
        if self._is_msp_command(text):
            try:
                # MSP özü "msp:" prefiksini tanıyır, ona görə
                # text-i olduğu kimi ötürə bilərik.
                response = self.msp.process(text)
                return f"MSP cavabı:\n{response}"
            except Exception as e:  # noqa: BLE001
                return (
                    "ESCALATION\n"
                    f"Reason: MSP processing error: {e}\n"
                    "Action: Human validation required.\n"
                )

        # 3) Hava ilə bağlı qeyri-müəyyən sual → şəhər soruş
        if self._needs_weather_clarification(text):
            return (
                "Zahid Brat, hava proqnozu üçün hansı şəhər lazımdır?\n"
                "Məsələn: *Bakı*, *Daşkənd* və ya başqa şəhər adı ilə yaz: \n"
                "`BRAT: Bakı üçün hava necədir?`"
            )

        # 4) Shopify məhsul sualı qeyri-müəyyəndirsə → məhsulu dəqiqləşdir
        if self._needs_shopify_product_clarification(text):
            return (
                "Zahid Brat, Shopify-də bir neçə məhsul ola bilər.\n"
                "Sənə konkret hansı məhsulun satışı maraqlıdır?\n\n"
                "Məsələn belə yaz:\n"
                "`BRAT: Shopify-də 'Samarkand Soul Demo Tablecloth' məhsulunun satışı necə gedir?`"
            )

        # 5) Əks halda – Brat GPT dialoqa göndər
        try:
            reply = brat_gpt_chat(
                user_prompt=text,
                agent_role="Telegram BRAT Dialog Brain",
            )
            return reply
        except Exception as e:  # noqa: BLE001
            return (
                "ESCALATION\n"
                f"Reason: Internal GPT error: {e}\n"
                "Action: Human validation required.\n"
                )
