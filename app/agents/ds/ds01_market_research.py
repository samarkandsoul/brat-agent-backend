from pydantic import BaseModel


class MarketResearchRequest(BaseModel):
    niche: str
    country: str = "US"


def analyze_market(req: MarketResearchRequest) -> str:
    """
    DS-01 DEMO VERSIYA.
    Hələ OpenAI kvotası qoşulmadığı üçün burda real API çağırışı YOXDUR.
    Sadəcə daxil olan məlumatı təsdiqləyir.
    """
    return (
        "DS-01 demo rejimindədir.\n"
        f"Niche: {req.niche}\n"
        f"Country: {req.country}\n\n"
        "Real market analizi OpenAI balansı aktiv olandan sonra qoşulacaq. "
        "Hal-hazırda yalnız komanda strukturunu test edirik. 🧠"
    )
