from fastapi import FastAPI
from app.agents.ds.ds01_market_research import analyze_market, MarketResearchRequest

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK", "message": "BRAT backend running"}

@app.post("/market/analyze")
def market_analyze(req: MarketResearchRequest):
    result = analyze_market(req)
    return {"status": "success", "data": result}
