# app/agents/ds/ds01_market_research.py

from pydantic import BaseModel

from app.llm.brat_gpt import simple_chat


class MarketResearchRequest(BaseModel):
    """
    DS-01 üçün input modeli.
    FastAPI endpoint-i və MSP eyni modeli istifadə edir.
    """
    niche: str
    country: str = "US"


def _build_prompts(req: MarketResearchRequest) -> tuple[str, str]:
    """
    DS-01 üçün system + user prompt qurur.
    Burada market research engine-in davranışı təsvir olunur.
    """
    system_prompt = (
        "Sən senior e-commerce market research analitiksən. "
        "Dropshipping, Shopify, TikTok & Meta reklamları, UGC creative-lər və "
        "conversion optimizasiyası üzrə ixtisaslaşmısan. "
        "Sənin vəzifən Zahid Brat üçün konkret niche və ölkə üzrə qısa, "
        "amma dərin analiz hazırlamaqdır.\n\n"
        "Cavabın strukturlu Markdown formatında olsun və bu bölmələri mütləq əhatə et:\n"
        "1) Market Snapshot\n"
        "2) Buyer Profile & Pain Points\n"
        "3) Demand, Trend & Seasonality\n"
        "4) Competition & Differentiation Opportunities\n"
        "5) Ad Angles & Creative Ideas (hook nümunələri ilə)\n"
        "6) Pricing & Offer Hints (qısa)\n"
        "7) Risklər & Red Flags\n"
        "8) Final Verdict — 1–10 arası 'Winning Potential Score' və qısa nəticə.\n\n"
        "Cavab maksimum ~400 söz ətrafında olsun. Konkret ol, boş motivasiya yazma."
    )

    user_prompt = (
        f"Niche: {req.niche}\n"
        f"Country / Market: {req.country}\n\n"
        "Zahid Brat dropshipping mağazasında bu niche üzrə məhsul test etmək istəyir. "
        "Yuxarıdakı struktura uyğun peşəkar, lakin praktik report hazırla."
    )

    return system_prompt, user_prompt


def analyze_market(req: MarketResearchRequest) -> str:
    """
    DS-01-in əsas funksiyası.
    - Əgər OPENAI_API_KEY varsa → real GPT analizi.
    - Əks halda → DEMO cavab (engine skeleton).
    """
    system_prompt, user_prompt = _build_prompts(req)
    answer = simple_chat(system_prompt, user_prompt, model="gpt-4o-mini")

    # Əgər simple_chat error / demo mətni qaytarıbsa, onu olduğu kimi göndəririk.
    # Normal GPT cavabı gəlirsə, sadəcə forwarding edirik.
    if answer.startswith("DS-01 info: OPENAI_API_KEY"):
        # DEMO fallback – balans/və ya API hazır deyil
        return (
            "DS-01 Market Research nəticəsi (DEMO):\n"
            f"Niche: {req.niche}\n"
            f"Country: {req.country}\n\n"
            "Real GPT bazalı market analizi üçün OpenAI açarı aktiv olanda DS-01 "
            "tam gücü ilə işləyəcək. Hal-hazırda yalnız struktur test olunur. 🧠"
        )

    if answer.startswith("DS-01 OpenAI xətası:"):
        # OpenAI error-u aydın şəkildə göstər
        return (
            f"DS-01 xətası:\n{answer}\n\n"
            "Bu, OpenAI sorğusu ilə bağlı texniki problemdir. Balansı, modeli və "
            "OPENAI_API_KEY-i yoxlamaq lazımdır."
        )

    # Normal, uğurlu cavab
    return answer
