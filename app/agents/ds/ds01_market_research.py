# app/agents/ds/ds01_market_research.py

from pydantic import BaseModel

from app.llm.brat_gpt import simple_chat
from app.integrations.web_research_client import (
    search_web,
    fetch_and_clean,
    WebResearchError,
)


class MarketResearchRequest(BaseModel):
    """
    DS-01 üçün input modeli.
    FastAPI endpoint-i və MSP eyni modeli istifadə edir.
    """
    niche: str
    country: str = "US"


def _build_research_context(
    req: MarketResearchRequest,
    max_sources: int = 3,
    max_chars_per_source: int = 1200,
) -> str:
    """
    Niche + country üçün vebdən xammal məlumat toplayır:
    - search_web ilə ilk bir neçə nəticəni tapır
    - hər URL üçün fetch_and_clean ilə təmizlənmiş mətn çəkir
    - qısa snippet-lərdən kontekst string qurur

    Problem olsa (scraping, proxy, layout dəyişməsi və s.), boş string qaytarır ki,
    DS-01 yenə də GPT-only rejimdə işləyə bilsin.
    """
    # Sorğunu daha konkret edirik ki, faydalı nəticələr gəlsin
    query = (
        f"{req.niche} dropshipping market research {req.country} "
        f"ecommerce demand competitors reviews"
    )

    try:
        results = search_web(query, num_results=max_sources)
    except WebResearchError:
        return ""
    except Exception:
        # Hər ehtimala qarşı – istəmirik ki, DS-01 bütövlükdə çök­sün
        return ""

    if not results:
        return ""

    pieces: list[str] = []

    for idx, (title, url) in enumerate(results, start=1):
        try:
            text = fetch_and_clean(url)
        except WebResearchError:
            continue
        except Exception:
            continue

        if not text:
            continue

        snippet = text[:max_chars_per_source]

        piece = (
            f"Source {idx}: {title}\n"
            f"URL: {url}\n"
            f"Snippet:\n{snippet}"
        )
        pieces.append(piece)

    if not pieces:
        return ""

    return (
        "WEB RESEARCH CONTEXT (auto-generated; may contain noise):\n\n"
        + "\n\n---\n\n".join(pieces)
    )


def _build_prompts(
    req: MarketResearchRequest,
    research_context: str | None = None,
) -> tuple[str, str]:
    """
    DS-01 üçün system + user prompt qurur.
    Burada market research engine-in davranışı təsvir olunur.
    research_context varsa, onu user prompt-a əlavə edirik.
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

    if research_context:
        user_prompt += (
            "\n\nAşağıda vebdən avtomatik toplanmış xammal məlumat var. "
            "Bu mətni analitik süzgəcdən keçir: səhv, köhnə və ya uyğunsuz hissələri "
            "nəzərə alma, amma faydalı faktları istifadə et. MAMOS və brend "
            "prinsipləri hər şeydən öndədir.\n\n"
            "----- WEB RESEARCH RAW CONTEXT START -----\n"
            f"{research_context}\n"
            "----- WEB RESEARCH RAW CONTEXT END -----\n"
        )

    return system_prompt, user_prompt


def analyze_market(req: MarketResearchRequest) -> str:
    """
    DS-01-in əsas funksiyası.
    - Əvvəlcə internetdən qısa web research konteksti toplamağa çalışır.
    - Daha sonra GPT-yə MAMOS + web kontekst ilə market analizi etdizdirir.
    - Əgər web research alınmasa, GPT-only rejimdə davam edir.
    """
    # 1) Vebdən kontekst toplama (sakitcə – uğursuz olsa da agent ölmür)
    research_context = ""
    try:
        research_context = _build_research_context(req)
    except Exception:
        research_context = ""

    # 2) Prompta bu konteksti inject edirik (əgər varsa)
    system_prompt, user_prompt = _build_prompts(
        req,
        research_context=research_context or None,
    )

    # 3) GPT çağırışı (mövcud simple_chat mexanizmi ilə)
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
