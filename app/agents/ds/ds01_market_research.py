from pydantic import BaseModel
import os
import requests
import json

# OPENAI API açarını Render environment-dən oxuyuruq
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MarketResearchRequest(BaseModel):
    niche: str
    country: str = "US"


def analyze_market(data: MarketResearchRequest):
    """
    DS-01: Full market research analysis using OpenAI.
    """

    if not OPENAI_API_KEY:
        return {
            "error": "OPENAI_API_KEY is missing. Set it in Render environment variables."
        }

    prompt = f"""
    You are DS-01 (Market-Research-Master).
    Analyze the following dropshipping niche and return a JSON object.

    Niche: {data.niche}
    Country: {data.country}

    Return STRICTLY valid JSON with this structure:

    {{
      "niche": "<niche>",
      "country": "<country>",
      "demand_score": <0-100>,
      "competition_score": <0-100>,
      "trending_potential": "<short text>",
      "top_competitor_products": [
        "<product 1>",
        "<product 2>",
        "<product 3>",
        "<product 4>",
        "<product 5>"
      ],
      "winning_angles": [
        "<angle 1>",
        "<angle 2>",
        "<angle 3>"
      ],
      "final_recommendation": "<1-sentence recommendation>"
    }}

    Do NOT add any extra text outside the JSON.
    """

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4.1",
            "messages": [
                {
                    "role": "system",
                    "content": "You are DS-01, a precise market analysis AI agent.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        },
        timeout=60,
    )

    if response.status_code != 200:
        return {
            "error": "OpenAI request failed",
            "status_code": response.status_code,
            "details": response.text,
        }

    content = response.json()["choices"][0]["message"]["content"]

    # Cavabı JSON-a çevirməyə cəhd edirik
    try:
        data = json.loads(content)
        return data
    except Exception:
        # JSON deyilsə, xam cavabı qaytarırıq
        return {"raw_response": content}
