import yfinance as yf
import pandas as pd

def calculate_ratios(ticker):
    """
    Ratio analysis compares a stock against its own history
    and against peer companies in the same sector.
    P/E, EV/EBITDA, ROE are the most used ratios in equity research.
    """
    try:
        stock = yf.Ticker(ticker)
        info  = stock.info

        # --- valuation ratios ---
        pe_ratio       = info.get("trailingPE", "N/A")
        forward_pe     = info.get("forwardPE", "N/A")
        pb_ratio       = info.get("priceToBook", "N/A")
        ev_to_ebitda   = info.get("enterpriseToEbitda", "N/A")
        ps_ratio       = info.get("priceToSalesTrailing12Months", "N/A")

        # --- profitability ratios ---
        roe            = info.get("returnOnEquity", "N/A")
        roa            = info.get("returnOnAssets", "N/A")
        profit_margin  = info.get("profitMargins", "N/A")
        operating_margin = info.get("operatingMargins", "N/A")

        # --- financial health ---
        debt_to_equity = info.get("debtToEquity", "N/A")
        current_ratio  = info.get("currentRatio", "N/A")

        print(f"\n===== Ratio Analysis: {ticker} =====")
        print(f"\n-- Valuation --")
        print(f"P/E Ratio (TTM)   : {pe_ratio}")
        print(f"Forward P/E       : {forward_pe}")
        print(f"Price/Book        : {pb_ratio}")
        print(f"EV/EBITDA         : {ev_to_ebitda}")
        print(f"Price/Sales       : {ps_ratio}")

        print(f"\n-- Profitability --")
        print(f"Return on Equity  : {str(round(roe*100, 2))+'%' if isinstance(roe, float) else roe}")
        print(f"Return on Assets  : {str(round(roa*100, 2))+'%' if isinstance(roa, float) else roa}")
        print(f"Profit Margin     : {str(round(profit_margin*100, 2))+'%' if isinstance(profit_margin, float) else profit_margin}")
        print(f"Operating Margin  : {str(round(operating_margin*100, 2))+'%' if isinstance(operating_margin, float) else operating_margin}")

        print(f"\n-- Financial Health --")
        print(f"Debt/Equity       : {debt_to_equity}")
        print(f"Current Ratio     : {current_ratio}")

        return {
            "pe": pe_ratio, "forward_pe": forward_pe,
            "pb": pb_ratio, "ev_ebitda": ev_to_ebitda,
            "roe": roe, "profit_margin": profit_margin,
            "debt_equity": debt_to_equity
        }

    except Exception as e:
        print(f"Ratios Error: {e}")
        return {}

if __name__ == "__main__":
    calculate_ratios("RELIANCE.NS")