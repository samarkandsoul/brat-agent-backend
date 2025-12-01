from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter

# ===========================
# 1. Pydantic data modelləri
# ===========================


class IntelSource(BaseModel):
    url: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    provider: Optional[str] = None  # "openai_browser", "google_api" və s.


class IntelSearchRequest(BaseModel):
    query: str = Field(..., description="Bratın sorğusu")
    intent_tags: List[str] = Field(
        default_factory=list,
        description=(
            "MSP Router-dən gələn intent tag-lar, məsələn: "
            "INTEL, NEWS, WEB, PRODUCT_SPY"
        ),
    )
    # gələcəkdə: language, country, time_range və s. əlavə edə bilərik


class IntelSearchResponse(BaseModel):
    summary: str
    bullets: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    sources: List[IntelSource] = Field(default_factory=list)
    used_channel: Optional[Literal["openai_browser", "search_api", "mock"]] = None
    raw_data: Optional[dict] = None


# ===========================
# 2. WEB-CORE-01 Agent class
# ===========================


class WebCoreAgent:
    """
    WEB-CORE-01 — Central WebSearch Brain

    HYBRID məntiq:
      - sadə, ümumi suallar üçün: OpenAI browser / ReAct (gələcəkdə)
      - xüsusi intel (rəqiblər, məhsullar və s.) üçün: search API (gələcəkdə)

    İndi skeleton: hələ real API çağırmır, sadəcə struktur hazırdır.
    """

    def route(self, req: IntelSearchRequest) -> IntelSearchResponse:
        """
        Hal-hazırda sync method – MSP-dən və FastAPI endpoint-dən rahat çağırılsın.
        Gələcəkdə real web inteqrasiyası bu funksiya içində işə salınacaq.
        """
        tags = [t.upper() for t in req.intent_tags]

        summary = (
            "WEB-CORE-01 hazırdır, amma hələ demo rejimdədir. "
            "Sorğunu qəbul etdi və sənə strukturlaşdırılmış cavab qaytardı."
        )

        bullets = [
            f"Sorğun: {req.query}",
            f"Intent tag-lar: {', '.join(tags) if tags else 'heç biri verilməyib'}",
            "Gələcək mərhələdə bu cavab real web nəticələrindən generasiya olunacaq.",
        ]

        action_items = [
            "MSP Router-də INTEL/NEWS/WEB tipli sorğuları WEB-CORE-01-ə yönləndir.",
            "Sonra OpenAI browser və ya search API inteqrasiyasını bu class-ın içində aktiv et.",
        ]

        sources = [
            IntelSource(
                url="https://samarkandsoul-intel.local/mock",
                title="Mock intel source (dev mode)",
                snippet="Bu, yalnız development mərhələsi üçün istifadə olunan test mənbədir.",
                provider="mock",
            )
        ]

        return IntelSearchResponse(
            summary=summary,
            bullets=bullets,
            action_items=action_items,
            sources=sources,
            used_channel="mock",
            raw_data={"note": "Real web inteqrasiyası hələ qoşulmayıb."},
        )

    # Gələcəkdə burda real funksiyalar olacaq
    async def _call_openai_browser(self, req: IntelSearchRequest) -> IntelSearchResponse:
        """
        TODO: OpenAI ReAct + Browser tool inteqrasiyası bura gələcək.
        """
        raise NotImplementedError

    async def _call_search_api(self, req: IntelSearchRequest) -> IntelSearchResponse:
        """
        TODO: Google / SerpAPI və s. web search API çağırışları bura gələcək.
        """
        raise NotImplementedError


# ===========================
# 3. FastAPI router
# ===========================

router = APIRouter(prefix="/intel", tags=["intel"])


@router.post("/search", response_model=IntelSearchResponse)
def intel_search_endpoint(payload: IntelSearchRequest) -> IntelSearchResponse:
    """
    Ümumi INTEL / WEB search endpoint-i.
    MSP Router buraya sorğunu və intent tag-ları ötürür.
    """
    agent = WebCoreAgent()
    result = agent.route(payload)
    return result


# ===========================
# 4. Helper (istəsən istifadə edərsən)
# ===========================


def get_web_core_agent() -> WebCoreAgent:
    """
    Dependency injection üçün helper.
    Gələcəkdə burada cache / shared state saxlaya bilərsən.
    """
    return WebCoreAgent()
