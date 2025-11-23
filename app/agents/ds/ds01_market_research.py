from pydantic import BaseModel

class MarketResearchRequest(BaseModel):
    niche: str
    country: str

def analyze_market(niche: str, country: str):
    return {
        "niche": niche,
        "country": country,
        "keywords": [
            f"best {niche} products in {country}",
            f"{niche} market trends {country}",
            f"{country} {niche} competitors"
        ],
        "summary": f"Market research for {niche} in {country} completed."
    }
