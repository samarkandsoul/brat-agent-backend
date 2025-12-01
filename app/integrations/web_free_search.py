import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SamarkandSoulBot/1.0)",
}

# -------------------------------
# GOOGLE NEWS RSS (KEYSIZ)
# -------------------------------
def google_news_rss(query: str, limit: int = 5):
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        items = soup.find_all("item")[:limit]
        results = []
        for it in items:
            title = it.title.text
            link = it.link.text
            results.append((title, link))
        return results
    except:
        return []


# -------------------------------
# DUCKDUCKGO Lite HTML
# -------------------------------
def ddg_lite_search(query: str, limit: int = 5):
    try:
        url = "https://lite.duckduckgo.com/lite/"
        resp = requests.post(url, data={"q": query}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for a in soup.select("a.result-link")[:limit]:
            title = a.get_text(strip=True)
            link = a["href"]
            results.append((title, link))
        return results
    except:
        return []


# -------------------------------
# BRAVE SEARCH (api-siz fallback)
# -------------------------------
def brave_html(query: str, limit: int = 5):
    try:
        url = f"https://search.brave.com/search?q={query}"
        resp = requests.get(url, timeout=10, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for d in soup.select(".snippet__title")[:limit]:
            title = d.get_text(strip=True)
            link = d.find("a")["href"]
            results.append((title, link))
        return results
    except:
        return []


# -------------------------------
# MASTER: MIXED SEARCH ENGINE
# -------------------------------
def free_web_search(query: str, limit: int = 5):
    providers = [
        google_news_rss,
        ddg_lite_search,
        brave_html,
    ]

    final = []
    for provider in providers:
        res = provider(query, limit)
        if res:
            final.extend(res)
        if len(final) >= limit:
            break

    if not final:
        return []

    return final[:limit]


# -------------------------------
# FORMAT for agent
# -------------------------------
def free_format_results(query: str, limit: int = 5):
    res = free_web_search(query, limit)
    if not res:
        return f"No results found for `{query}`."

    lines = [f"🔎 *Results for* `{query}`", ""]
    for idx, (title, link) in enumerate(res, start=1):
        lines.append(f"{idx}. *{title}*\n   {link}")

    return "\n".join(lines)
