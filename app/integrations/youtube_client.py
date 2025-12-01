# app/integrations/youtube_client.py

from __future__ import annotations

from typing import List, Dict


class YouTubeClientError(Exception):
    """Generic YouTube client error."""
    pass


def search_youtube_ideas(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Demo / dev-mode YouTube "search".

    Real YouTube API yoxdur, ona görə hazırda sadəcə
    struktur qaytarırıq. Gələcəkdə bura API inteqrasiyası əlavə edəcəyik.
    """
    if not query:
        raise YouTubeClientError("Query boş ola bilməz.")

    ideas: List[Dict[str, str]] = []
    for i in range(1, max_results + 1):
        ideas.append(
            {
                "title": f"[DEMO] {query} – idea #{i}",
                "url": "https://youtube.com",  # placeholder
                "note": "Real YouTube API inteqrasiyası gələcək mərhələdə qoşulacaq.",
            }
        )
    return ideas
