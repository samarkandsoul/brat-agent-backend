from pydantic import BaseModel
import requests
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MarketResearchRequest(BaseModel):
    niche: str
    country: str = "US"


def analyze_market(data: MarketResearchRequest):
    """
    DS-01: Full market research analysis using OpenAI.
    """

    if not OPENAI_API_KEY:
        return {"error": "OPENAI_API_KEY is not set in environment variables"}

    prompt = f"""
    You are DS-01 (Market-Research-Master).
    Analyze the following niche for dropshipping:

    Niche: {data.niche}
    Country: {data.country}

    Provide:
    - Demand score (0-100)
    - Competition score (0-100)
    - Trending potential
    - Top 5 competitor products
    - 3 winning angles
    - Final 1-sentence recommendation
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
                    "content": "You are DS-01; a market analysis AI agent.",
                },
                {"role": "user", "content": prompt},
            ],
        },
    )

    if response.status_code != 200:
        return {"error": "OpenAI request failed", "details": response.text}

    content = response.json()["choices"][0]["message"]["content"]
    return {"result": content}
