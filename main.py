from fastapi import FastAPI
from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Brat backend running"}

@app.post("/ds/market-research")
def run_market_research(request: MarketResearchRequest):
    return analyze_market(request)
