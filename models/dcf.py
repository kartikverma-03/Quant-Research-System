import pandas as pd
import numpy as np

def calculate_dcf(ticker):
    """
    DCF = Discounted Cash Flow
    We project future cash flows and discount them back to today's value.
    This tells us what the stock is ACTUALLY worth, not just what it trades at.
    """
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        
        # --- get the numbers we need ---
        cash_flow   = stock.cashflow
        balance     = stock.balance_sheet
        info        = stock.info

        # free cash flow = operating cash flow minus capital expenditure
        # this is the real cash the business generates after spending on assets
        operating_cf = cash_flow.loc["Operating Cash Flow"].iloc[0]  
        capex        = cash_flow.loc["Capital Expenditure"].iloc[0]
        free_cash_flow = operating_cf + capex   # capex is negative so we add

        shares_outstanding = info.get("sharesOutstanding", 1)
        current_price      = info.get("currentPrice", 0)

        # --- DCF assumptions ---
        # these are standard assumptions used by analysts
        growth_rate    = 0.10    # 10% growth for next 5 years (conservative for Indian large cap)
        terminal_growth = 0.04   # 4% forever after 5 years (roughly India's long term GDP growth)
        discount_rate  = 0.12    # 12% WACC (cost of capital — what investors expect as return)
        years          = 5       # projection period

        # --- project cash flows for next 5 years ---
        projected_cf = []
        for year in range(1, years + 1):
            cf = free_cash_flow * ((1 + growth_rate) ** year)
            discounted = cf / ((1 + discount_rate) ** year)
            projected_cf.append(discounted)

        # --- terminal value (value of all cash flows beyond year 5) ---
        terminal_cf    = projected_cf[-1] * (1 + terminal_growth)
        terminal_value = terminal_cf / (discount_rate - terminal_growth)
        discounted_tv  = terminal_value / ((1 + discount_rate) ** years)

        # --- total intrinsic value ---
        total_value    = sum(projected_cf) + discounted_tv
        fair_value_per_share = total_value / shares_outstanding

        upside = ((fair_value_per_share - current_price) / current_price) * 100

        print(f"\n===== DCF Valuation: {ticker} =====")
        print(f"Free Cash Flow (latest) : {free_cash_flow:,.0f}")
        print(f"DCF Fair Value          : {fair_value_per_share:,.2f}")
        print(f"Current Market Price    : {current_price:,.2f}")
        print(f"Upside / Downside       : {upside:+.1f}%")

        if upside > 15:
            verdict = "Undervalued — potential BUY"
        elif upside < -15:
            verdict = "Overvalued — potential SELL"
        else:
            verdict = "Fairly valued — HOLD"

        print(f"Verdict                 : {verdict}")
        return fair_value_per_share, upside, verdict

    except Exception as e:
        print(f"DCF Error: {e}")
        return None, None, "Data unavailable"

if __name__ == "__main__":
    calculate_dcf("RELIANCE.NS")