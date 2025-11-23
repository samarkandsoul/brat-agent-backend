from fastapi import FastAPI
from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest

app = FastAPI()

@app.post("/market/analyze")
def analyze_market_endpoint(request: MarketResearchRequest):
    return analyze_market(request)

@app.get("/")
def root():
    return {"status": "OK", "message": "BRAT backend running"}
