import anthropic
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))


def build_prompt(keyword, news_articles, stock_data, fear_greed, macro):
    news_text = "\n".join([
        "- " + a.get("title", "") + ": " + a.get("description", "")
        for a in news_articles
    ])

    stock_text = ""
    if stock_data:
        stock_text = (
            "Stock Data (" + str(stock_data.get("ticker", "N/A")) + "):\n"
            "- Current Price: $" + str(stock_data.get("current_price", "N/A")) + "\n"
            "- Change Today: " + str(stock_data.get("change_pct", "N/A")) + "%\n"
            "- 52W High: $" + str(stock_data.get("week_52_high", "N/A")) +
            " | 52W Low: $" + str(stock_data.get("week_52_low", "N/A"))
        )

    macro_text = (
        "Macro Environment:\n"
        "- Fed Rate: " + str(macro.get("fed_rate", "N/A")) + "\n"
        "- Inflation (CPI): " + str(macro.get("inflation_cpi", "N/A")) + "\n"
        "- GDP Growth: " + str(macro.get("gdp_growth", "N/A")) + "\n"
        "- Unemployment: " + str(macro.get("unemployment", "N/A"))
    )

    fg_text = (
        "Market Sentiment: Fear & Greed Index = " +
        str(fear_greed.get("value", "N/A")) + "/100 (" +
        str(fear_greed.get("label", "N/A")) + ")"
    )

    prompt = (
        'You are a senior financial analyst at a top-tier investment firm.\n'
        'Analyze the following data about "' + keyword + '" and produce a structured market intelligence report.\n\n'
        + news_text + "\n\n"
        + stock_text + "\n\n"
        + macro_text + "\n\n"
        + fg_text + "\n\n"
        'Respond ONLY with a valid JSON object, no extra text, no markdown:\n'
        '{\n'
        '  "sector": "sector name here",\n'
        '  "trend": "Bullish or Bearish or Neutral",\n'
        '  "confidence": 82,\n'
        '  "key_drivers": ["driver 1", "driver 2", "driver 3"],\n'
        '  "impacted_companies": ["TICK1", "TICK2", "TICK3"],\n'
        '  "time_horizon": "Short to Medium Term (3-9 months)",\n'
        '  "risk_factors": ["risk 1", "risk 2"],\n'
        '  "what_happens_next": "forward looking insight here",\n'
        '  "macro_context": "one sentence on macro environment",\n'
        '  "correlation": "one sentence linking to another sector"\n'
        '}'
    )

    return prompt


def analyze(keyword, news_articles, stock_data, fear_greed, macro):
    try:
        prompt = build_prompt(keyword, news_articles, stock_data, fear_greed, macro)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = message.content[0].text.strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw)
    except Exception:
        return None


def get_demo_insight(keyword):
    from data_sources import DEMO_INSIGHTS
    keyword_lower = keyword.lower()
    for insight in DEMO_INSIGHTS:
        sector_lower = insight["sector"].lower()
        if any(word in sector_lower for word in keyword_lower.split()):
            return insight
    return DEMO_INSIGHTS[0]