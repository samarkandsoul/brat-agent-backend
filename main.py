from fastapi import FastAPI
from pydantic import BaseModel

# Import agents
from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest

app = FastAPI(
    title="BRAT Backend",
    version="1.0.0",
    description="Core backend for BRAT multi-agent system"
)

@app.get("/")
def root():
    return {"status": "OK", "message": "BRAT backend running"}

@app.post("/market/analyze")
def market_analyze(req: MarketResearchRequest):
    try:
        result = analyze_market(req.niche, req.country)
        return {"status": "success", "data": result}
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
