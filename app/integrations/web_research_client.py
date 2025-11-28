"""
Web Research Client (SERPAPI EDITION)

This module gives the agent system a reliable internet search brain
using SerpAPI (Google Search API).

Functions:
- fetch_url(url): returns cleaned text from a webpage
- search_web(query): uses SerpAPI Google Search (stable, non-blocked)
"""

from __future__ import annotations

import os
import re
import requests
from typing import List, Tuple

# Common User-Agent for all outgoing HTTP requests
DEFAULT_HEADERS = {
    "User-Agent": "SamarkandSoulBot/1.0 (+https://samarkandsoul.com)",
    "Accept-Language": "en-US,en;q=0.9",
}

# SERPAPI KEY (you must set it in Render environment)
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# -------------------------------
# FETCH URL (works correctly)
# -------------------------------
def fetch_url(url: str, timeout: int = 12, max_chars: int = 9000) -> str:
    url = (url or "").strip()
    if not url:
        return "WEB-ERROR: URL is empty."

    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    except Exception as e:
        return f"WEB-ERROR: request failed: {e}"

    if resp.status_code != 200:
        return f"WEB-ERROR: status {resp.status_code} for {url}"

    text = resp.text

    # Remove scripts, styles, and HTML tags
    clean = re.sub(r"<script.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<style.*?</style>", " ", clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    if len(clean) > max_chars:
        clean = clean[:max_chars] + "\n\n[TRUNCATED]"

    return clean


# -------------------------------
# GOOGLE SEARCH (SERPAPI)
# -------------------------------
def search_web(query: str, max_results: int = 5) -> List[Tuple[str, str]]:
    """
    Uses SerpAPI for guaranteed search results.
    Returns list of (title, url).
    """
    if not query:
        return []

    if not SERPAPI_KEY:
        return []

    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY,
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
    except Exception:
        return []

    results = []
    organic = data.get("organic_results", [])
    for item in organic[:max_results]:
        title = item.get("title", "")
        link = item.get("link", "")
        if title and link:
            results.append((title, link))

    return results


# -------------------------------
# FORMATTED RESULT STRING
# -------------------------------
def format_search_results(query: str, max_results: int = 5) -> str:
    items = search_web(query, max_results=max_results)
    if not items:
        return f"No results or SERPAPI key missing.\nQuery: {query!r}"

    lines = [f"🔍 Search results for: {query}\n"]
    for i, (title, link) in enumerate(items, start=1):
        lines.append(f"{i}) {title}\n{link}\n")

    return "\n".join(lines)
