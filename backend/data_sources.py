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

NEWS_CATEGORIES = {
    "AI & Technology": ["AI", "artificial intelligence", "machine learning", "chip", "semiconductor", "data center", "cloud", "software", "tech"],
    "Energy & Commodities": ["oil", "gas", "energy", "petroleum", "OPEC", "renewable", "solar", "wind", "gold", "silver", "commodity"],
    "Macro & Policy": ["Fed", "interest rate", "inflation", "GDP", "unemployment", "central bank", "monetary", "fiscal", "recession"],
    "Crypto & Blockchain": ["bitcoin", "crypto", "ethereum", "blockchain", "DeFi", "token", "web3", "NFT"],
    "Equity Markets": ["stock", "market", "NYSE", "Nasdaq", "S&P", "earnings", "revenue", "profit", "shares", "IPO"],
    "Geopolitics & Trade": ["war", "sanctions", "tariff", "trade", "China", "Iran", "Russia", "Ukraine", "export", "import"],
    "Indian Markets": ["India", "Nifty", "Sensex", "RBI", "rupee", "BSE", "NSE", "SEBI", "Modi", "Indian"]
}

IMPACT_DESCRIPTIONS = {
    "AI & Technology": "Technology stocks and semiconductor supply chains directly affected. Data center operators and AI infrastructure companies see demand shifts.",
    "Energy & Commodities": "Energy producers, refiners and commodity traders directly impacted. Downstream manufacturing and transport sectors feel secondary effects.",
    "Macro & Policy": "All asset classes affected. Rate changes alter borrowing costs, currency strength, and investor risk appetite across every sector.",
    "Crypto & Blockchain": "Digital asset prices and crypto-adjacent stocks (exchanges, miners) directly impacted. Retail investor sentiment shifts rapidly.",
    "Equity Markets": "Broad market sentiment affected. Index funds, institutional portfolios and retail investors all exposed to price movements.",
    "Geopolitics & Trade": "Supply chains, export revenues and currency markets disrupted. Defense, energy and manufacturing sectors most exposed.",
    "Indian Markets": "Domestic Indian equities, rupee strength and FII (foreign institutional investor) flows directly impacted."
}

DEMO_NEWS = [
    {
        "title": "NVIDIA Reports Record Revenue Driven by AI Chip Demand",
        "description": "NVIDIA data center revenue surged 400% year-over-year as hyperscalers race to build AI infrastructure, pushing quarterly earnings to an all-time high.",
        "source": "Bloomberg", "url": "https://bloomberg.com",
        "category": "AI & Technology",
        "impacted_industry": "Semiconductors & Data Centers",
        "industry_impact": "Direct positive — GPU demand from AI training workloads is driving NVIDIA margins to record levels, pulling AMD and TSMC alongside."
    },
    {
        "title": "Federal Reserve Signals Pause in Rate Hikes Amid Cooling Inflation",
        "description": "Fed chair indicated rates may hold steady as CPI drops to 3.2%, giving growth stocks relief and strengthening the case for a soft landing.",
        "source": "Reuters", "url": "https://reuters.com",
        "category": "Macro & Policy",
        "impacted_industry": "Banking & Financial Services",
        "industry_impact": "Systemic positive — rate pause reduces pressure on bank margins and makes growth-stage companies more attractive to investors."
    },
    {
        "title": "India IT Sector Wins $4.2B in AI Transformation Contracts in Q1",
        "description": "TCS, Infosys and Wipro collectively secured major enterprise AI deals as global companies outsource AI implementation to Indian IT firms.",
        "source": "Economic Times", "url": "https://economictimes.com",
        "category": "Indian Markets",
        "impacted_industry": "Indian IT & Software Services",
        "industry_impact": "Direct positive — large contract wins signal multi-year revenue visibility and margin expansion as AI tooling reduces delivery costs."
    },
    {
        "title": "EV Adoption Accelerates as Battery Costs Hit Record Lows",
        "description": "Lithium-ion battery prices fell 14% this quarter, making EVs cost-competitive with ICE vehicles for the first time in mass-market segments.",
        "source": "Financial Times", "url": "https://ft.com",
        "category": "Energy & Commodities",
        "impacted_industry": "Electric Vehicles & Battery Materials",
        "industry_impact": "Mixed — positive for EV manufacturers and lithium miners, negative for traditional automakers and oil demand long-term."
    },
    {
        "title": "Global Semiconductor Shortage Easing as TSMC Expands Capacity",
        "description": "TSMC and Samsung are ramping new fabs as automotive and consumer electronics demand normalises, signalling potential oversupply in legacy nodes.",
        "source": "WSJ", "url": "https://wsj.com",
        "category": "AI & Technology",
        "impacted_industry": "Semiconductors & Electronics Manufacturing",
        "industry_impact": "Mixed — advanced node chips remain tight due to AI demand while legacy node oversupply pressures margins for older chip designs."
    },
    {
        "title": "Bitcoin Surges Past $70,000 as Institutional ETF Inflows Accelerate",
        "description": "Spot Bitcoin ETF products saw record weekly inflows as pension funds and wealth managers increase digital asset allocations.",
        "source": "CoinDesk", "url": "https://coindesk.com",
        "category": "Crypto & Blockchain",
        "impacted_industry": "Cryptocurrency & Digital Assets",
        "industry_impact": "Direct positive — institutional adoption via ETFs provides sustained demand floor, reducing Bitcoin's historical volatility profile."
    },
    {
        "title": "US-China Trade Tensions Escalate With New Semiconductor Export Controls",
        "description": "Washington expanded chip export restrictions targeting advanced AI processors, forcing NVIDIA and AMD to redesign China-market products.",
        "source": "Reuters", "url": "https://reuters.com",
        "category": "Geopolitics & Trade",
        "impacted_industry": "Semiconductors & US-China Supply Chains",
        "industry_impact": "Negative for US chip exporters losing China revenue. Positive for domestic Chinese chip companies gaining protected market share."
    },
    {
        "title": "S&P 500 Hits Record High as Earnings Season Beats Expectations",
        "description": "Over 78% of S&P 500 companies reported earnings above analyst estimates, driving the index to an all-time high with technology leading gains.",
        "source": "CNBC", "url": "https://cnbc.com",
        "category": "Equity Markets",
        "impacted_industry": "Broad Equity Markets",
        "industry_impact": "Broad positive — strong earnings across sectors signal economic resilience, supporting risk-on sentiment and equity valuations."
    },
    {
        "title": "Gold Prices Hit All-Time High Amid Global Uncertainty",
        "description": "Gold crossed $2,400 per ounce as investors seek safe-haven assets amid geopolitical tensions and concerns about dollar debasement.",
        "source": "MarketWatch", "url": "https://marketwatch.com",
        "category": "Energy & Commodities",
        "impacted_industry": "Precious Metals & Safe-Haven Assets",
        "industry_impact": "Direct positive for gold miners and ETFs. Signals risk-off sentiment that typically pressures equity valuations."
    },
    {
        "title": "RBI Holds Rates Steady Supporting Indian Equity Rally",
        "description": "The Reserve Bank of India maintained its repo rate at 6.5%, boosting domestic market confidence and supporting the Nifty 50's upward momentum.",
        "source": "Economic Times", "url": "https://economictimes.com",
        "category": "Indian Markets",
        "impacted_industry": "Indian Banking & Equity Markets",
        "industry_impact": "Positive for Indian banks and rate-sensitive sectors. Stable rates support consumer lending growth and infrastructure spending."
    }
]

DEMO_STOCK = {
    "ticker": "NVDA", "current_price": 875.40, "change_pct": 3.24,
    "week_52_high": 974.00, "week_52_low": 394.28,
    "chart_data": [520,535,548,562,590,610,598,625,648,670,655,680,695,710,698,725,748,762,775,790,780,800,815,830,820,845,858,870,865,875]
}

DEMO_INSIGHTS = [
    {
        "sector": "Semiconductors & AI Infrastructure",
        "trend": "Bullish", "confidence": 89,
        "key_drivers": ["Explosive AI model training demand", "Hyperscaler capex up 40% YoY", "NVIDIA H100/H200 supply constraints easing"],
        "impacted_companies": ["NVDA", "AMD", "TSM", "ASML", "INTC"],
        "time_horizon": "Short to Medium Term (3-9 months)",
        "risk_factors": ["US-China export restrictions", "Potential AI capex slowdown", "New entrants from AMD and custom silicon"],
        "what_happens_next": "Continued outperformance likely as AI infrastructure buildout accelerates. Watch for NVDA earnings as the key catalyst.",
        "macro_context": "Fed pause supports growth stock valuations. Low rates benefit capital-intensive AI infrastructure spending.",
        "correlation": "AI chip demand is directly driving energy sector growth as data centers consume record levels of power."
    },
    {
        "sector": "Indian IT & Digital Transformation",
        "trend": "Bullish", "confidence": 76,
        "key_drivers": ["$4.2B in AI contracts won in Q1", "Rupee stability attracting FII inflows", "Global enterprises outsourcing AI implementation"],
        "impacted_companies": ["TCS.NS", "INFY", "WIPRO.NS", "HCL.NS", "TECHM.NS"],
        "time_horizon": "Medium Term (6-12 months)",
        "risk_factors": ["US visa policy changes", "Client budget freezes in BFSI sector", "Currency volatility"],
        "what_happens_next": "Indian IT positioned as primary beneficiary of global AI transformation wave. Margin expansion likely as AI tools reduce delivery costs.",
        "macro_context": "India GDP growth at 6.8% provides domestic demand cushion against global slowdown risks.",
        "correlation": "Indian IT growth is correlated with US tech spending cycles and dollar strength against the rupee."
    },
    {
        "sector": "Clean Energy & EV Ecosystem",
        "trend": "Neutral", "confidence": 62,
        "key_drivers": ["Battery cost parity with ICE vehicles reached", "Government EV subsidies in US and EU", "Charging infrastructure buildout accelerating"],
        "impacted_companies": ["TSLA", "RIVN", "NIO", "ALB", "LTHM"],
        "time_horizon": "Medium to Long Term (9-18 months)",
        "risk_factors": ["Raw material price volatility", "Slower-than-expected consumer adoption", "Political risk to EV subsidies"],
        "what_happens_next": "Near-term consolidation likely before next growth leg. Lithium miners and battery manufacturers outperform automakers.",
        "macro_context": "Higher-for-longer rates pressure EV manufacturer margins. Battery material plays more insulated.",
        "correlation": "EV adoption is linked to lithium and copper commodity cycles, creating opportunities in materials sector."
    }
]

FEAR_GREED_DEMO = {"value": 68, "label": "Greed", "timestamp": "2026-04-05"}
MACRO_DEMO = {"fed_rate": "5.25-5.50%", "inflation_cpi": "3.2%", "gdp_growth": "2.1%", "unemployment": "3.8%"}


def categorize_article(title, description):
    text = (title + " " + (description or "")).lower()
    for category, keywords in NEWS_CATEGORIES.items():
        if any(kw.lower() in text for kw in keywords):
            return category
    return "Equity Markets"


def get_industry_impact(category, title, description):
    base = IMPACT_DESCRIPTIONS.get(category, "Broad market impact across multiple sectors.")
    text = (title + " " + (description or "")).lower()
    if any(w in text for w in ["surge", "record", "high", "beat", "growth", "rally"]):
        sentiment = "Positive"
    elif any(w in text for w in ["fall", "drop", "crash", "loss", "decline", "warn", "risk"]):
        sentiment = "Negative"
    else:
        sentiment = "Mixed"
    return sentiment + " — " + base


def fetch_news(keyword, page_size=10):
    try:
        params = {
            "q": '"' + keyword + '" AND (market OR stock OR invest OR economy OR finance OR sector OR industry)',
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
            title = a["title"]
            desc = a.get("description") or "No summary available."
            if len(desc) > 220:
                desc = desc[:217] + "..."
            category = categorize_article(title, desc)
            industry_impact = get_industry_impact(category, title, desc)
            articles.append({
                "title": title,
                "description": desc,
                "source": a["source"]["name"],
                "url": a["url"],
                "published_at": a.get("publishedAt", "")[:10],
                "category": category,
                "impacted_industry": IMPACT_DESCRIPTIONS.get(category, "General Markets")[:60],
                "industry_impact": industry_impact
            })
        return articles[:10] if articles else DEMO_NEWS
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
        change_pct = round(((current - prev) / prev) * 100, 2) if current and prev else 0
        chart = hist["Close"].round(2).tolist() if not hist.empty else []
        return {
            "ticker": ticker, "current_price": current, "change_pct": change_pct,
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
        return {"value": int(entry["value"]), "label": entry["value_classification"], "timestamp": entry["timestamp"]}
    except Exception:
        return FEAR_GREED_DEMO


def fetch_macro():
    return MACRO_DEMO


def fetch_crypto(symbol="bitcoin"):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": symbol, "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=6
        )
        data = r.json().get(symbol, {})
        return {"price": data.get("usd"), "change_24h": round(data.get("usd_24h_change", 0), 2)}
    except Exception:
        return None