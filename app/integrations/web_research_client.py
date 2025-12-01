from __future__ import annotations

import os
import re
from typing import List, Tuple, Literal, Optional, Dict, Any

import requests
from bs4 import BeautifulSoup  # HTML parsing for fallback search

# -----------------------------
# Config & Types
# -----------------------------

DEFAULT_HEADERS = {
    "User-Agent": "SamarkandSoulBot/1.0 (+https://samarkandsoul.com)"
}

# gələcəkdə ZENSERP, BRIGHTDATA və s. əlavə edə bilərik
SearchProvider = Literal["NONE", "SERPAPI", "SERPER", "BING_HTML", "DUCKDUCKGO_HTML"]

# default-u NONE saxlayırıq, özümüz BING_HTML fallback edirik
SEARCH_PROVIDER: SearchProvider = os.getenv("SEARCH_PROVIDER", "NONE").upper()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")  # əgər Serper.dev istifadə etsən

DEFAULT_TIMEOUT = int(os.getenv("WEB_REQUEST_TIMEOUT", "12"))


class WebResearchError(Exception):
    """Generic error for web research / search failures."""
    pass


# -----------------------------
# Low-level fetch helpers
# -----------------------------

def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch raw HTML/text from a URL."""
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        raise WebResearchError(f"Failed to fetch URL {url}: {e}") from e


def clean_text(html: str) -> str:
    """
    Very basic HTML -> text cleaner, agents üçün kifayət edir.
    Removes scripts/styles, strips tags, normalizes whitespace.
    """
    # remove scripts & styles
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    # remove all remaining tags
    text = re.sub(r"<[^>]+>", " ", text)
    # normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_and_clean(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Convenience helper: fetch URL and return cleaned text content.
    """
    html = fetch_url(url, timeout=timeout)
    return clean_text(html)


# -----------------------------
# Search entrypoint
# -----------------------------

def search_web(query: str, num_results: int = 5) -> List[Tuple[str, str]]:
    """
    Provider-agnostic web search.

    Returns list of (title, url).

    Strategy:
    - Əgər SERPAPI/SERPER və key varsa → onları işlət.
    - Yoxdursa → əvvəl BING HTML (API keysiz), sonra DuckDuckGo HTML fallback.
    """
    provider = SEARCH_PROVIDER

    # Explicit provider selections with keys
    if provider == "SERPAPI":
        if not SERPAPI_KEY:
            # fallback if misconfigured
            return _search_with_bing_html(query, num_results)
        return _search_with_serpapi(query, num_results)

    if provider == "SERPER":
        if not SERPER_KEY:
            # fallback if misconfigured
            return _search_with_bing_html(query, num_results)
        return _search_with_serper(query, num_results)

    if provider == "BING_HTML":
        return _search_with_bing_html(query, num_results)

    if provider == "DUCKDUCKGO_HTML":
        return _search_with_duckduckgo_html(query, num_results)

    # provider == "NONE" or unknown -> safe fallback chain
    try:
        return _search_with_bing_html(query, num_results)
    except WebResearchError:
        # əgər Bing HTML də bloklanıbsa, DuckDuckGo-nu da cəhd edək
        return _search_with_duckduckgo_html(query, num_results)


# -----------------------------
# Provider implementations
# -----------------------------

def _search_with_serpapi(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Legacy SerpAPI integration.
    Hazırda region limitlərinə görə disabled.
    """
    if not SERPAPI_KEY:
        raise WebResearchError("SERPAPI_API_KEY is not set.")

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
        resp = requests.post(url, json=payload, headers=headers, timeout=DEFAULT_TIMEOUT)
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


def _search_with_bing_html(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Free HTML-based search via Bing (no API key, no phone).

    Returns list of (title, url).
    """
    search_url = "https://www.bing.com/search"
    params = {"q": query, "setlang": "en"}

    try:
        resp = requests.get(
            search_url,
            params=params,
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
    except Exception as e:
        raise WebResearchError(f"Bing request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")

    results: List[Tuple[str, str]] = []

    # Klassik Bing layout: li.b_algo h2 a
    for li in soup.select("li.b_algo"):
        a = li.select_one("h2 a")
        if not a:
            continue
        title = a.get_text(strip=True)
        link = a.get("href")
        if not title or not link:
            continue

        results.append((title, link))
        if len(results) >= num_results:
            break

    if not results:
        raise WebResearchError("Bing HTML returned no results or layout changed.")

    return results


def _search_with_duckduckgo_html(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Fallback search provider using DuckDuckGo's HTML interface.
    No API key, no phone, sadəcə HTTP + HTML parsing.

    Returns list of (title, url).
    """
    search_url = "https://duckduckgo.com/html/"
    params = {
        "q": query,
        "kl": "us-en",  # location bias; can be adjusted
    }

    try:
        resp = requests.get(
            search_url,
            params=params,
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
    except Exception as e:
        raise WebResearchError(f"DuckDuckGo request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")

    results: List[Tuple[str, str]] = []

    # Köhnə layout: a.result__a
    for a in soup.select("a.result__a"):
        title = a.get_text(strip=True)
        link = a.get("href")
        if not link or not title:
            continue
        results.append((title, link))
        if len(results) >= num_results:
            break

    if not results:
        raise WebResearchError("DuckDuckGo HTML returned no results or layout changed.")

    return results


# -----------------------------
# High-level helpers for MSP / agents
# -----------------------------

def format_search_results(query: str, num_results: int = 5) -> str:
    """
    MSP üçün rahat format.

    Input:
        query – axtarış sözü
        num_results – neçə nəticə qaytarsın

    Output:
        Telegram/Markdown üçün səliqəli mətn.
    """
    if not query:
        return "WEB search error: query boş ola bilməz."

    try:
        results = search_web(query, num_results=num_results)
    except WebResearchError as e:
        return f"No results found for {query}.\n(Provider error: {e})"

    if not results:
        return f"No results found for {query}."

    lines: List[str] = [
        f"🔎 *Web Search results for:* `{query}`",
        "",
    ]

    for idx, (title, url) in enumerate(results, start=1):
        lines.append(f"{idx}. *{title}*\n   {url}")

    lines.append(
        "\nDaha dərin analiz üçün konkret linki belə açdır:\n"
        "`msp: web: fetch | https://example.com`"
    )

    return "\n".join(lines)
