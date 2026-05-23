import os
from dotenv import load_dotenv
from google import genai
import yfinance as yf

load_dotenv()

def generate_analyst_report(ticker):
    try:
        stock = yf.Ticker(ticker)
        info  = stock.info

        name          = info.get("longName", ticker)
        sector        = info.get("sector", "N/A")
        current_price = info.get("currentPrice", "N/A")
        pe            = info.get("trailingPE", "N/A")
        pb            = info.get("priceToBook", "N/A")
        roe           = info.get("returnOnEquity", "N/A")
        profit_margin = info.get("profitMargins", "N/A")
        debt_equity   = info.get("debtToEquity", "N/A")
        week52_high   = info.get("fiftyTwoWeekHigh", "N/A")
        week52_low    = info.get("fiftyTwoWeekLow", "N/A")
        market_cap    = info.get("marketCap", "N/A")

        prompt = f"""
You are a senior equity research analyst at a top investment bank.
Write a concise professional stock research report for {name} ({ticker}).

Financial data:
- Sector: {sector}
- Current Price: {current_price}
- Market Cap: {market_cap}
- P/E Ratio: {pe}
- Price/Book: {pb}
- Return on Equity: {roe}
- Profit Margin: {profit_margin}
- Debt/Equity: {debt_equity}
- 52-Week High: {week52_high}
- 52-Week Low: {week52_low}

Write a 150-word analyst report covering:
1. Business overview (1 sentence)
2. Valuation assessment based on the ratios
3. Financial health and profitability
4. Key risks
5. Final verdict: Buy, Hold, or Sell with a brief reason

Write like a real analyst report. Be specific, use the numbers.
        """

        api_key = os.getenv("GEMINI_API_KEY")
        client  = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model    = "gemini-2.5-flash",
            contents = prompt
        )
        report = response.text

        print(f"\n===== AI Analyst Report: {ticker} =====")
        print(report)

        os.makedirs("data/processed", exist_ok=True)
        with open(f"data/processed/{ticker}_report.txt", "w", encoding="utf-8") as f:
            f.write(report)

        return report

    except Exception as e:
        print(f"AI Report Error: {e}")
        return None


if __name__ == "__main__":
    generate_analyst_report("RELIANCE.NS")