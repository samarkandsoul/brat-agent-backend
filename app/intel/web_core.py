from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

# Bütün real web axtarış loqikası burada cəmlənir
from app.integrations.web_research_client import (
    format_search_results,
    format_news_intel,
)


class IntelSearchRequest(BaseModel):
    """
    WEB-CORE-01 üçün əsas request modeli.

    - query: əsas sorğu mətni
    - tags: INTEL, NEWS, ECOM və s. kimi əlavə etikətlər
    """
    query: str
    tags: List[str] = []


class WebCoreAgent:
    """
    WEB-CORE-01 – Intel beyni.

    Öz-özünə internetə çıxmır; bütün web axtarışını
    `web_research_client` üzərindən edir.

    Xüsusi loqika:
      - Əgər tag-lar arasında NEWS varsa, ya da query-də 'news' sözü varsa →
        format_news_intel istifadə edir.
      - Əks halda → format_search_results (general web).
    """

    def handle_query(self, req: IntelSearchRequest) -> str:
        # Sadə qoruma
        if not req.query:
            return "WEB-CORE-01 error: sorğu (query) boş ola bilməz."

        # NEWS intent detection
        tags_upper = [t.upper() for t in (req.tags or [])]
        is_news_intent = ("NEWS" in tags_upper) or ("news" in req.query.lower())

        try:
            if is_news_intent:
                raw_answer = format_news_intel(req.query)
            else:
                raw_answer = format_search_results(req.query)
        except Exception as e:  # noqa: BLE001
            return (
                "WEB-CORE-01 hazırdır, amma real web axtarışında problem yarandı.\n"
                f"Error: {e}"
            )

        tag_line = ", ".join(req.tags) if req.tags else "none"

        return (
            "🧠 WEB-CORE-01 — Intel summary\n\n"
            f"• Sorğu: {req.query}\n"
            f"• Taglar: {tag_line}\n\n"
            f"{raw_answer}"
        )


# =========================
#  FastAPI router
# =========================
router = APIRouter(prefix="/intel", tags=["intel"])


@router.post("/search")
def intel_search(req: IntelSearchRequest):
    """
    HTTP endpoint (Render, Postman və s. üçün).
    Telegram MSP də eyni WebCoreAgent-i istifadə edir.
    """
    agent = WebCoreAgent()
    answer = agent.handle_query(req)
    return {"status": "ok", "answer": answer}
