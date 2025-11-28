# app/integrations/web_research_client.py

"""
Web Research Client

This module gives the agent system a basic "internet brain":
- fetch plain text from a given URL
- run a simple DuckDuckGo search and return top results

Later, DS-01 / DS-21 / other agents can import this module
and reuse its functions.
"""

from __future__ import annotations

import re
from typing import List, Tuple

import requests

# Common User-Agent for all outgoing HTTP requests
DEFAULT_HEADERS = {
    "User-Agent": "SamarkandSoulBot/1.0 (+https://samarkandsoul.com)",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_url(url: str, timeout: int = 12, max_chars: int = 8000) -> str:
    """
    Fetch a URL and return cleaned plain text.

    - Strips HTML tags, scripts, styles
    - Collapses whitespace
    - Truncates long pages to `max_chars`
    """
    url = (url or "").strip()
    if not url:
        return "WEB-ERROR: URL is empty."

    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    except Exception as e:  # pylint: disable=broad-except
        return f"WEB-ERROR: request failed: {e}"

    if resp.status_code != 200:
        return f"WEB-ERROR: status {resp.status_code} for {url}"

    text = resp.text

    # Remove scripts and styles
    clean = re.sub(
        r"<script.*?</script>",
        " ",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    clean = re.sub(
        r"<style.*?</style>",
        " ",
        clean,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Remove all HTML tags
    clean = re.sub(r"<[^>]+>", " ", clean)

    # Normalize whitespace
    clean = re.sub(r"\s+", " ", clean).strip()

    if len(clean) > max_chars:
        clean = clean[:max_chars] + "\n\n[TRUNCATED]"

    return clean


def duckduckgo_search(
    query: str,
    max_results: int = 5,
    timeout: int = 12,
) -> List[Tuple[str, str]]:
    """
    Run a simple DuckDuckGo HTML search.

    Returns a list of (title, url) tuples.
    If anything fails, returns an empty list.
    """
    q = (query or "").strip()
    if not q:
        return []

    try:
        resp = requests.get(
            "https://duckduckgo.com/html/",
            params={"q": q},
            headers=DEFAULT_HEADERS,
            timeout=timeout,
        )
    except Exception:
        return []

    if resp.status_code != 200:
        return []

    html = resp.text

    # Very simple parser: find <a> elements with class "result__a"
    pattern = re.compile(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )

    results: List[Tuple[str, str]] = []
    for match in pattern.finditer(html):
        url = match.group(1)
        title_html = match.group(2)
        # Strip any HTML tags from the title
        title = re.sub(r"<[^>]+>", " ", title_html)
        title = re.sub(r"\s+", " ", title).strip()
        if url and title:
            results.append((title, url))
        if len(results) >= max_results:
            break

    return results


def format_search_results(query: str, max_results: int = 5) -> str:
    """
    Helper for MSP / Telegram: returns search results as plain text.
    """
    query = (query or "").strip()
    if not query:
        return "WEB-ERROR: search query is empty."

    items = duckduckgo_search(query, max_results=max_results)
    if not items:
        return f"No search results or network error for query: {query!r}"

    lines = [
        f"Web search results for: {query!r}",
        "",
    ]

    for idx, (title, url) in enumerate(items, start=1):
        lines.append(f"{idx}. {title}\n   {url}")

    return "\n".join(lines)
