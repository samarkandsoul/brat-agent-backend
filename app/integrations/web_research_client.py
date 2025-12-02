from __future__ import annotations

import os
import re
from typing import List, Tuple, Literal, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup

# ============================================================
#  WEB RESEARCH CLIENT — multi-provider + NEWS preset
# ============================================================

DEFAULT_HEADERS = {
    "User-Agent": "SamarkandSoulBot/1.0 (+https://samarkandsoul.com)"
}

# Gələcək üçün API-lər də saxlanılır, amma default tam HTML chain-dir
SearchProvider = Literal[
    "AUTO",
    "SERPAPI",
    "SERPER",
    "DUCKDUCKGO_HTML",
    "BING_HTML",
    "BRAVE_HTML",
]

SEARCH_PROVIDER: SearchProvider = os.getenv("SEARCH_PROVIDER", "AUTO").upper()  # AUTO = chain

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

DEFAULT_TIMEOUT = int(os.getenv("WEB_REQUEST_TIMEOUT", "12"))


class WebResearchError(Exception):
    """Generic error for web research / search failures."""
    pass


# ============================================================
#  Low-level fetch helpers
# ============================================================

def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    Fetch raw HTML/text from a URL.
    MSP `msp: web: fetch | URL` üçün istifadə edir.
    """
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        raise WebResearchError(f"Failed to fetch URL {url}: {e}") from e


def clean_text(html: str) -> str:
    """
    Very basic HTML -> text cleaner.
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
    Agentlər üçün qısa yol.
    """
    html = fetch_url(url, timeout=timeout)
    return clean_text(html)


# ============================================================
#  Search entrypoint (multi-provider engine)
# ============================================================

def search_web(
    query: str,
    num_results: int = 5,
    intent: str = "general",
) -> List[Tuple[str, str]]:
    """
    Provider-agnostic web search.

    Returns list of (title, url).

    Strategy:
      - Əgər SEARCH_PROVIDER env ilə konkret provider seçilibsə → onu işə sal.
      - Əks halda (AUTO) → multi-provider chain:
          1) Bing HTML
          2) DuckDuckGo HTML
          3) Brave HTML
        və ilk uğurlu nəticə verən provider istifadə olunur.
    """
    provider = SEARCH_PROVIDER

    # Explicit provider selections with keys
    if provider == "SERPAPI":
        if not SERPAPI_KEY:
            # fallback if misconfigured
            return _search_chain(query, num_results, intent=intent)
        return _search_with_serpapi(query, num_results)

    if provider == "SERPER":
        if not SERPER_KEY:
            # fallback if misconfigured
            return _search_chain(query, num_results, intent=intent)
        return _search_with_serper(query, num_results)

    if provider == "DUCKDUCKGO_HTML":
        return _search_with_duckduckgo_html(query, num_results)

    if provider == "BING_HTML":
        return _search_with_bing_html(query, num_results)

    if provider == "BRAVE_HTML":
        return _search_with_brave_html(query, num_results)

    # provider == "AUTO" or unknown -> safe multi-provider chain
    return _search_chain(query, num_results, intent=intent)


def _search_chain(
    query: str,
    num_results: int = 5,
    intent: str = "general",
) -> List[Tuple[str, str]]:
    """
    Multi-provider chain:
      1) Bing HTML
      2) DuckDuckGo HTML
      3) Brave HTML

    İlk uğurlu nəticəni qaytarır, hamısı yanarsa WebResearchError atır.
    """
    providers = [
        ("Bing", _search_with_bing_html),
        ("DuckDuckGo", _search_with_duckduckgo_html),
        ("Brave", _search_with_brave_html),
    ]

    last_error: Optional[Exception] = None
    for name, fn in providers:
        try:
            results = fn(query, num_results)
            if results:
                return results
        except Exception as e:  # noqa: BLE001
            last_error = e
            continue

    raise WebResearchError(f"All providers failed or returned no usable results. Last error: {last_error}")


# ============================================================
#  Provider implementations
# ============================================================

def _search_with_serpapi(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Legacy SerpAPI integration.
    Hal-hazırda region məhdudiyyətlərinə görə disabled saxlayırıq.
    """
    if not SERPAPI_KEY:
        raise WebResearchError("SERPAPI_API_KEY is not set.")

    raise WebResearchError("SerpApi currently disabled due to region restrictions.")


def _search_with_serper(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Example integration with Serper.dev (Google Search JSON API).
    NOTE: field names may change, check Serper docs if something breaks.

    Qeyd: Səndə SMS / qeydiyyat problemi olduğuna görə, default istifadə etmirik,
    amma gələcək üçün saxlanılır.
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


def _search_with_duckduckgo_html(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Fallback search provider using DuckDuckGo's HTML interface.

    Returns list of (title, url).
    """
    search_url = "https://duckduckgo.com/html/"
    params = {
        "q": query,
        "kl": "us-en",
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

    # Bir neçə potensial selector – layout dəyişəndə də şans artsın
    for a in soup.select("a.result__a, a.result__url, h2 a"):
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


def _search_with_bing_html(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Bing HTML interfeysi ilə sadə axtarış.
    """
    search_url = "https://www.bing.com/search"
    params = {
        "q": query,
        "setlang": "en-us",
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
        raise WebResearchError(f"Bing request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")
    results: List[Tuple[str, str]] = []

    for a in soup.select("li.b_algo h2 a"):
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


def _search_with_brave_html(query: str, num_results: int) -> List[Tuple[str, str]]:
    """
    Brave Search HTML interfeysi.
    Layout dəyişə bilər, ona görə çox sadə selector istifadə edirik.
    """
    search_url = "https://search.brave.com/search"
    params = {
        "q": query,
        "source": "web",
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
        raise WebResearchError(f"Brave request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")
    results: List[Tuple[str, str]] = []

    # Brave nəticələri üçün tipik selector-lar
    for a in soup.select("a.result-header, div.snippet-title a, h2 a"):
        title = a.get_text(strip=True)
        link = a.get("href")
        if not title or not link:
            continue
        results.append((title, link))
        if len(results) >= num_results:
            break

    if not results:
        raise WebResearchError("Brave HTML returned no results or layout changed.")

    return results


# ============================================================
#  NEWS-specific helpers (RSS-based for real headlines)
# ============================================================

def _fetch_world_news_rss(num_results: int = 5) -> List[Tuple[str, str]]:
    """
    Dünya xəbərləri üçün stabil yol:
    Birbaşa BBC, Reuters, AP və s.-nin RSS feed-lərindən oxuyuruq.
    Burda heç bir search engine yoxdur, ona görə zibil nəticə gəlmir.
    """
    feeds = [
        # BBC World
        ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
        # Reuters World News
        ("Reuters World", "https://feeds.reuters.com/Reuters/worldNews"),
        # AP – Top News (burda da world xəbərləri çox olur)
        ("AP Top", "https://rss.apnews.com/apf-topnews"),
    ]

    items: List[Tuple[str, str]] = []

    for name, url in feeds:
        try:
            xml_text = fetch_url(url)
        except WebResearchError:
            continue

        # RSS üçün XML parser daha təhlükəsizdir
        soup = BeautifulSoup(xml_text, "xml")

        for item in soup.find_all("item"):
            title_tag = item.find("title")
            link_tag = item.find("link")

            title = title_tag.get_text(strip=True) if title_tag else ""
            link = link_tag.get_text(strip=True) if link_tag else ""

            if not title or not link:
                continue

            items.append((title, link))
            if len(items) >= num_results:
                break

        if len(items) >= num_results:
            break

    return items


# ============================================================
#  High-level helpers for MSP / agents
# ============================================================

def format_search_results(
    query: str,
    num_results: int = 5,
    intent: str = "general",
) -> str:
    """
    MSP üçün rahat format.

    Input:
        query – axtarış sözü
        num_results – neçə nəticə qaytarsın
        intent – "general" / "news" və s.

    Output:
        Telegram/Markdown üçün səliqəli mətn.
    """
    primary_query = (query or "").strip()
    if not primary_query:
        return "WEB search: sorğu boş ola bilməz."

    # 1-ci cəhd – olduğu kimi
    try:
        results = search_web(primary_query, num_results=num_results, intent=intent)
    except WebResearchError:
        results = []

    # 2-ci cəhd – bir az “latest” əlavə edib yenidən
    if not results:
        alt_query = f"{primary_query} latest"
        try:
            results = search_web(alt_query, num_results=num_results, intent=intent)
        except WebResearchError:
            results = []

    if not results:
        return f"No results found for {primary_query}."

    lines: List[str] = [
        f"🔎 Web Search results for: `{primary_query}`",
        "",
    ]

    for idx, (title, url) in enumerate(results, start=1):
        lines.append(f"{idx}. *{title}*\n   {url}")

    lines.append(
        "\nDaha dərin analiz üçün konkret linki belə açdır:\n"
        "`msp: web: fetch | https://example.com`"
    )

    return "\n".join(lines)


def format_news_intel(query: str, num_results: int = 5) -> str:
    """
    Xüsusi NEWS / INTEL formatı.

    - Əgər sorğu ümumi "world news", "today world news" tipindədirsə →
      birbaşa BBC / Reuters / AP RSS-dən oxuyuruq (zero-zibil, real xəbərlər).
    - Daha spesifik sorğular üçün yenə search engine chain istifadə olunur.
    """
    base = (query or "").strip()
    base_lower = base.lower() if base else ""

    # --- 1) WORLD NEWS CASE — RSS İLƏ ---
    if (
        not base_lower
        or "world news" in base_lower
        or base_lower in ("world", "news", "today world news", "today news")
    ):
        headlines = _fetch_world_news_rss(num_results=num_results)

        if not headlines:
            return "No results found for world news."

        lines: List[str] = [
            "🌍 *Global News Intel — World Headlines*",
            "",
        ]

        for idx, (title, url) in enumerate(headlines, start=1):
            lines.append(f"{idx}. *{title}*\n   {url}")

        lines.append(
            "\nDaha dərin analiz üçün konkret linki belə açdır:\n"
            "`msp: web: fetch | https://example.com`"
        )

        return "\n".join(lines)

    # --- 2) SPESİFİK NEWS SORĞULARI ÜÇÜN KEÇMİŞ SEARCH-BAZALI YOL ---
    base_clean = base or "world news"

    enriched_query = (
        f"latest {base_clean} headlines "
        "site:bbc.com OR site:reuters.com OR site:apnews.com "
        "OR site:ft.com OR site:bloomberg.com"
    )

    try:
        results = search_web(enriched_query, num_results=num_results, intent="news")
    except WebResearchError:
        results = []

    if not results:
        fallback_query = f"latest {base_clean} today"
        try:
            results = search_web(fallback_query, num_results=num_results, intent="news")
        except WebResearchError:
            results = []

    if not results:
        return f"No results found for {base_clean}."

    lines: List[str] = [
        f"🌍 *Global News Intel for:* `{base_clean}`",
        "",
    ]

    for idx, (title, url) in enumerate(results, start=1):
        lines.append(f"{idx}. *{title}*\n   {url}")

    lines.append(
        "\nDaha dərin analiz üçün konkret linki belə açdır:\n"
        "`msp: web: fetch | https://example.com`"
    )

    return "\n".join(lines)
