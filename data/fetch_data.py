import yfinance as yf
import pandas as pd
import os

def fetch_stock_price(ticker, period="2y"):
    print(f"Fetching price data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    os.makedirs("data/raw", exist_ok=True)
    output_path = f"data/raw/{ticker}_prices.csv"
    df.to_csv(output_path)
    print(f"Saved to {output_path}")
    print(df.tail())
    return df

def fetch_financials(ticker):
    print(f"\nFetching financial statements for {ticker}...")
    stock = yf.Ticker(ticker)
    
    income_stmt  = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow    = stock.cashflow
    
    income_stmt.to_csv(f"data/raw/{ticker}_income.csv")
    balance_sheet.to_csv(f"data/raw/{ticker}_balance.csv")
    cash_flow.to_csv(f"data/raw/{ticker}_cashflow.csv")
    
    print("Financial statements saved.")
    print("\nIncome Statement preview:")
    print(income_stmt.head())
    return income_stmt, balance_sheet, cash_flow

def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    print(f"\n--- {info.get('longName', ticker)} ---")
    print(f"Sector     : {info.get('sector', 'N/A')}")
    print(f"Market Cap : {info.get('marketCap', 0):,.0f}")
    print(f"P/E Ratio  : {info.get('trailingPE', 'N/A')}")
    print(f"52W High   : {info.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"52W Low    : {info.get('fiftyTwoWeekLow', 'N/A')}")
    return info

if __name__ == "__main__":
    TICKER = "RELIANCE.NS"    # change this to any stock you want

    get_stock_info(TICKER)
    fetch_stock_price(TICKER, period="2y")
    fetch_financials(TICKER)
    print("\nDone! Check data/raw folder.")
