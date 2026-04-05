import requests
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")

TICKER_MAP = {
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL", "alphabet": "GOOGL",
    "amazon": "AMZN", "tesla": "TSLA", "nvidia": "NVDA", "meta": "META",
    "bitcoin": "BTC-USD", "crypto": "BTC-USD", "ethereum": "ETH-USD",
    "gold": "GLD", "silver": "SLV", "oil": "USO", "energy": "XLE",
    "semiconductors": "SOXX", "tech": "QQQ", "market": "SPY",
    "nifty": "^NSEI", "sensex": "^BSESN", "india": "INDA",
    "netflix": "NFLX", "uber": "UBER", "airbnb": "ABNB",
    "fed": "SPY", "inflation": "TIP", "bonds": "TLT"
}

DEMO_NEWS = [
    {
        "title": "NVIDIA Reports Record Revenue Driven by AI Chip Demand",
        "description": "NVIDIA data center revenue surged 400% year-over-year as hyperscalers race to build AI infrastructure.",
        "source": "Bloomberg",
        "url": "https://bloomberg.com"
    },
    {
        "title": "Federal Reserve Signals Pause in Rate Hikes Amid Cooling Inflation",
        "description": "Fed chair indicated rates may hold steady as CPI drops to 3.2%, giving markets relief.",
        "source": "Reuters",
        "url": "https://reuters.com"
    },
    {
        "title": "India IT Sector Sees Surge in AI-Related Contracts",
        "description": "TCS, Infosys and Wipro collectively won $4.2B in AI transformation deals in Q1.",
        "source": "Economic Times",
        "url": "https://economictimes.com"
    },
    {
        "title": "EV Adoption Accelerates as Battery Costs Hit Record Lows",
        "description": "Lithium-ion battery prices fell 14% this quarter, making EVs cost-competitive with ICE vehicles.",
        "source": "Financial Times",
        "url": "https://ft.com"
    },
    {
        "title": "Global Semiconductor Shortage Easing, Analysts Predict Supply Surplus",
        "description": "TSMC and Samsung expanding capacity as demand from automotive and consumer sectors normalises.",
        "source": "WSJ",
        "url": "https://wsj.com"
    }
]

DEMO_STOCK = {
    "ticker": "NVDA",
    "current_price": 875.40,
    "change_pct": 3.24,
    "week_52_high": 974.00,
    "week_52_low": 394.28,
    "chart_data": [520, 535, 548, 562, 590, 610, 598, 625, 648, 670,
                   655, 680, 695, 710, 698, 725, 748, 762, 775, 790,
                   780, 800, 815, 830, 820, 845, 858, 870, 865, 875]
}

DEMO_INSIGHTS = [
    {
        "sector": "Semiconductors & AI Infrastructure",
        "trend": "Bullish",
        "confidence": 89,
        "key_drivers": [
            "Explosive AI model training demand",
            "Hyperscaler capex up 40% YoY",
            "NVIDIA H100/H200 supply constraints easing"
        ],
        "impacted_companies": ["NVDA", "AMD", "TSM", "ASML", "INTC"],
        "time_horizon": "Short to Medium Term (3-9 months)",
        "risk_factors": [
            "US-China export restrictions",
            "Potential AI capex slowdown",
            "New entrants from AMD and custom silicon"
        ],
        "what_happens_next": "Continued outperformance likely as AI infrastructure buildout accelerates. Watch for NVDA earnings as the key catalyst.",
        "macro_context": "Fed pause supports growth stock valuations. Low rates benefit capital-intensive AI infrastructure spending.",
        "correlation": "AI chip demand is directly driving energy sector growth as data centers consume record levels of power."
    },
    {
        "sector": "Indian IT & Digital Transformation",
        "trend": "Bullish",
        "confidence": 76,
        "key_drivers": [
            "$4.2B in AI contracts won in Q1",
            "Rupee stability attracting FII inflows",
            "Global enterprises outsourcing AI implementation"
        ],
        "impacted_companies": ["TCS.NS", "INFY", "WIPRO.NS", "HCL.NS", "TECHM.NS"],
        "time_horizon": "Medium Term (6-12 months)",
        "risk_factors": [
            "US visa policy changes",
            "Client budget freezes in BFSI sector",
            "Currency volatility"
        ],
        "what_happens_next": "Indian IT positioned as primary beneficiary of global AI transformation wave. Margin expansion likely as AI tools reduce delivery costs.",
        "macro_context": "India GDP growth at 6.8% provides domestic demand cushion against global slowdown risks.",
        "correlation": "Indian IT growth is correlated with US tech spending cycles and dollar strength against the rupee."
    },
    {
        "sector": "Clean Energy & EV Ecosystem",
        "trend": "Neutral",
        "confidence": 62,
        "key_drivers": [
            "Battery cost parity with ICE vehicles reached",
            "Government EV subsidies in US and EU",
            "Charging infrastructure buildout accelerating"
        ],
        "impacted_companies": ["TSLA", "RIVN", "NIO", "ALB", "LTHM"],
        "time_horizon": "Medium to Long Term (9-18 months)",
        "risk_factors": [
            "Raw material price volatility",
            "Slower-than-expected consumer adoption",
            "Political risk to EV subsidies"
        ],
        "what_happens_next": "Near-term consolidation likely before next growth leg. Lithium miners and battery manufacturers outperform automakers.",
        "macro_context": "Higher-for-longer rates pressure EV manufacturer margins. Battery material plays more insulated.",
        "correlation": "EV adoption is linked to lithium and copper commodity cycles, creating opportunities in materials sector."
    }
]

FEAR_GREED_DEMO = {
    "value": 68,
    "label": "Greed",
    "timestamp": "2026-04-05"
}

MACRO_DEMO = {
    "fed_rate": "5.25-5.50%",
    "inflation_cpi": "3.2%",
    "gdp_growth": "2.1%",
    "unemployment": "3.8%"
}


def fetch_news(keyword, page_size=5):
    try:
        params = {
            "q": '"' + keyword + '" AND (market OR stock OR invest OR economy OR finance)',
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": page_size,
            "apiKey": NEWSAPI_KEY
        }
        r = requests.get("https://newsapi.org/v2/everything", params=params, timeout=8)
        data = r.json()
        if data.get("status") != "ok":
            return DEMO_NEWS
        articles = []
        for a in data.get("articles", []):
            if a["title"] == "[Removed]":
                continue
            articles.append({
                "title": a["title"],
                "description": a.get("description") or "No description available.",
                "source": a["source"]["name"],
                "url": a["url"]
            })
        return articles[:5] if articles else DEMO_NEWS
    except Exception:
        return DEMO_NEWS


def fetch_stock(keyword):
    try:
        ticker = TICKER_MAP.get(keyword.lower())
        if not ticker:
            return None
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1mo")
        current = info.get("currentPrice") or info.get("regularMarketPrice")
        prev = info.get("previousClose")
        if current and prev:
            change_pct = round(((current - prev) / prev) * 100, 2)
        else:
            change_pct = 0
        chart = hist["Close"].round(2).tolist() if not hist.empty else []
        return {
            "ticker": ticker,
            "current_price": current,
            "change_pct": change_pct,
            "week_52_high": info.get("fiftyTwoWeekHigh"),
            "week_52_low": info.get("fiftyTwoWeekLow"),
            "chart_data": chart[-30:] if len(chart) > 30 else chart
        }
    except Exception:
        return DEMO_STOCK


def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=5)
        data = r.json()
        entry = data["data"][0]
        return {
            "value": int(entry["value"]),
            "label": entry["value_classification"],
            "timestamp": entry["timestamp"]
        }
    except Exception:
        return FEAR_GREED_DEMO


def fetch_macro():
    try:
        return MACRO_DEMO
    except Exception:
        return MACRO_DEMO


def fetch_crypto(symbol="bitcoin"):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": symbol,
                "vs_currencies": "usd",
                "include_24hr_change": "true"
            },
            timeout=6
        )
        data = r.json().get(symbol, {})
        return {
            "price": data.get("usd"),
            "change_24h": round(data.get("usd_24h_change", 0), 2)
        }
    except Exception:
        return None