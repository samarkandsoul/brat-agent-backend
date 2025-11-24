# app/agents/core/msp.py

from typing import Tuple


class MSP:
    """
    MSP (Main Service Processor) - Samarkand Soul botunun əsas router-i.
    Buraya gələn "msp: ..." komandalarını oxuyub uyğun agenta yönləndirir.
    """

    def __init__(self) -> None:
        # Gələcəkdə bura config, token və s. əlavə edə bilərik
        pass

    # =========================
    #  Helper-lər
    # =========================
    @staticmethod
    def _strip_msp_prefix(raw_text: str) -> str:
        """
        'msp:' prefiksini kəsir və baş/son boşluqları təmizləyir.
        """
        text = (raw_text or "").strip()
        lowered = text.lower()
        if lowered.startswith("msp:"):
            text = text[4:].strip()
        return text

    @staticmethod
    def _split_once(body: str, sep: str = "|") -> Tuple[str, str]:
        """
        'a | b' formatını iki hissəyə bölən helper.
        Sağ tərəf boş ola bilər, amma tuple həmişə (left, right) qaytarır.
        """
        parts = [p.strip() for p in body.split(sep, 1)]
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    # =========================
    #  Main entrypoint
    # =========================
    def process(self, raw_text: str) -> str:
        """
        Telegramdan gələn bütün MSP komandaları üçün giriş nöqtəsi.
        Nümunələr:
          - 'msp: market: pet hair remover | US'
          - 'msp: offer: pet hair remover üçün ideal qiymət və bundle ideyaları | US market'
          - 'msp: drive: SamarkandSoulSystem / DS System / DS-01 - Market-Research-Master'
        """

        if not raw_text:
            return "MSP error: boş mesaj gəldi."

        text = self._strip_msp_prefix(raw_text)

        # ==========================================================
        # 1) DS-01 MARKET RESEARCH (FULL ENGINE)
        # ----------------------------------------------------------
        # Format:
        #   msp: market: Niche | Country
        # ==========================================================
        if text.lower().startswith("market:"):
            body = text[len("market:") :].strip()
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

            # Burada result artıq full engine cavabıdır (markdown ola bilər)
            return f"DS-01 Market Research nəticəsi:\n{result}"

        # ==========================================================
        # 2) DS-04 OFFER & PRICING STRATEGIST (DEMO)
        # ----------------------------------------------------------
