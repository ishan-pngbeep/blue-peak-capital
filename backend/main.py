from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from data_sources import (
    fetch_news, fetch_stock, fetch_fear_greed,
    fetch_macro, fetch_crypto, DEMO_INSIGHTS,
    DEMO_NEWS, DEMO_STOCK, FEAR_GREED_DEMO, MACRO_DEMO
)
from analyzer import analyze, get_demo_insight

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "live"}


@app.get("/api/insights/demo")
def demo_insights():
    fear_greed = fetch_fear_greed()
    macro = fetch_macro()
    return {
        "insights": DEMO_INSIGHTS,
        "fear_greed": fear_greed,
        "macro": macro,
        "mode": "demo"
    }


@app.get("/api/search")
def search(keyword: str, mode: str = "live"):
    fear_greed = fetch_fear_greed()
    macro = fetch_macro()
    stock = fetch_stock(keyword)

    if mode == "demo":
        insight = get_demo_insight(keyword)
        news = DEMO_NEWS
        stock = stock or DEMO_STOCK
        return {
            "keyword": keyword,
            "insight": insight,
            "news": news,
            "stock": stock,
            "fear_greed": fear_greed,
            "macro": macro,
            "mode": "demo"
        }

    news = fetch_news(keyword)
    insight = analyze(keyword, news, stock, fear_greed, macro)

    if not insight:
        insight = get_demo_insight(keyword)
        mode = "demo_fallback"

    return {
        "keyword": keyword,
        "insight": insight,
        "news": news,
        "stock": stock or DEMO_STOCK,
        "fear_greed": fear_greed,
        "macro": macro,
        "mode": mode
    }


@app.get("/api/market-overview")
def market_overview():
    try:
        fear_greed = fetch_fear_greed()
        macro = fetch_macro()
        btc = fetch_crypto("bitcoin")
        eth = fetch_crypto("ethereum")
        return {
            "fear_greed": fear_greed,
            "macro": macro,
            "crypto": {"bitcoin": btc, "ethereum": eth},
            "mode": "live"
        }
    except Exception:
        return {
            "fear_greed": FEAR_GREED_DEMO,
            "macro": MACRO_DEMO,
            "crypto": {},
            "mode": "demo"
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)