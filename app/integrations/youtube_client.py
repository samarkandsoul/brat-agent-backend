# app/integrations/youtube_client.py

from typing import List
from app.llm.brat_gpt import brat_gpt_chat
from app.integrations.web_research_client import (
    format_search_results,
    fetch_url,
)


def search_youtube_via_web(query: str, max_results: int = 3) -> str:
    """
    YouTube API-siz YouTube axtarış beyni.

    addım:
      1) web: search → normal axtarış (format_search_results)
      2) brat_gpt_chat ilə nəticələrdən yalnız YouTube linkləri süzmək
    """
    if not query:
        return "WEB/YT error: boş query ilə YouTube axtarışı edə bilmirəm."

    # 1) web search nəticələrini alırıq (burda sən artıq web_research_client yazmısan)
    raw_results = format_search_results(f"YouTube video: {query}")

    # 2) GPT-yə deyirik: bu mətndən ən çox 3 youtube link çıxart
    prompt = (
        "You are a YouTube search assistant inside the Samarkand Soul system.\n"
        "Below is a raw web search result text. Extract up to "
        f"{max_results} relevant YouTube video links about the topic.\n"
        "Return them as a clean markdown list:\n"
        "- Title (short, 1 line)\n"
        "- URL\n\n"
        "If there are no valid YouTube links, say that clearly.\n\n"
        "RAW RESULTS:\n"
        f"{raw_results}"
    )

    reply = brat_gpt_chat(
        user_prompt=prompt,
        agent_role="WEB/YOUTUBE-SEARCH-AGENT",
    )
    return reply


def summarize_youtube_via_web(url: str, target_minutes: int = 10) -> str:
    """
    YouTube video xülasəçisi.

    addım:
      1) videonun səhifəsini fetch_url ilə çək
      2) HTML + səhifə məzmununu GPT-yə ver
      3) 'sanki videoya baxmış kimi' 10 dəqiqəlik xülasə hazırla
    """
    if not url:
        return "WEB/YT error: URL boşdur."

    raw_page = fetch_url(url)

    prompt = (
        "You are a senior video analysis assistant for Zahid Brat.\n"
        "You are given the HTML/page content of a YouTube video URL.\n"
        "Your job: simulate that you watched the FULL video and create a summary "
        f"that condenses it into about {target_minutes} minutes of core content.\n\n"
        "RULES:\n"
        "- First, give a 5–7 bullet 'Core Insights' section.\n"
        "- Then a short 'Structure of the video' (beginning → middle → end).\n"
        "- Then 'Actionable points for Zahid Brat' with 3–7 practical items.\n"
        "- No fluff, calm premium tone.\n\n"
        "PAGE CONTENT:\n"
        f"{raw_page}"
    )

    reply = brat_gpt_chat(
        user_prompt=prompt,
        agent_role="WEB/YOUTUBE-SUMMARY-AGENT",
    )
    return reply
