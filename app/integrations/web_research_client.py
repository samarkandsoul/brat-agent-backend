# app/integrations/web_research_client.py

from __future__ import annotations
import os
import re
import requests
from typing import List, Tuple, Literal, Optional, Dict, Any

DEFAULT_HEADERS = {
    "User-Agent": "SamarkandSoulBot/1.0 (+https://samarkandsoul.com)"
}

SearchProvider = Literal["NONE", "SERPAPI", "SERPER"]  # gələcəkdə ZENSERP, BRIGHTDATA və s. əlavə edə bilərik

SEARCH_PROVIDER: SearchProvider = os.getenv("SEARCH_PROVIDER", "NONE").upper()  # "NONE" default
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")  # əgər Serper.dev istifadə etsən

class WebResearchError(Exception):
    pass


def fetch_url(url: str, timeout: int = 12) -> str:
    """Fetch raw HTML/text from a URL."""
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        raise WebResearchError(f"Failed to fetch URL {url}: {e}") from e


def clean_text(html: str) -> str:
    """Very basic HTML -> text cleaner, agents üçün kifayət edir."""
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def search_web(query: str, num_results: int = 5) -> List[Tuple[str, str]]:
    """
    Provider-agnostic web search.
    Returns list of (title, url).
    """
    provider = SEARCH_PROVIDER
    if provider == "SERPAPI":
        return _search_with_serpapi(query, num_results)
    elif provider == "SERPER":
        return _search_with_serper(query, num_results)
    elif provider == "NONE":
        raise WebResearchError(
            "SEARCH_PROVIDER is NONE. Configure a search provider or disable search for this agent."
        )
    else:
        raise WebResearchError(f"Unknown SEARCH_PROVIDER: {provider}")


def _search_with_serpapi(query: str, num_results: int) -> List[Tuple[str, str]]:
    if not SERPAPI_KEY:
        raise WebResearchError("SERPAPI_API_KEY is not set.")
    # Burada səndə olan köhnə SerpApi kodun qalsın – amma artıq məcburi deyil
    # Sadə placeholder:
    raise WebResearchError("SerpApi currently disabled due to region restrictions.")


def _search_with_serper(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Example integration with Serper.dev (Google Search JSON API).
    NOTE: field names may change, check Serper docs if something breaks.
    """
    if not SERPER_KEY:
        raise WebResearchError("SERPER_API_KEY is not set.")

    url = "https://google.serper.dev/search"
    payload: Dict[str, Any] = {"q": query, "num": num_results}
    headers = {
        "X-API-KEY": SERPER_KEY,
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=12)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        raise WebResearchError(f"Serper request failed: {e}") from e

    results: List[Tuple[str, str]] = []
    for item in data.get("organic", [])[:num_results]:
        title = item.get("title") or ""
        link = item.get("link") or ""
        if title and link:
            results.append((title, link))

    if not results:
        raise WebResearchError("Serper returned no organic results.")

    return results
