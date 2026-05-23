import yfinance as yf
import pandas as pd
import ta

def calculate_technicals(ticker, period="1y"):
    """
    Technical analysis looks at price and volume patterns.
    RSI tells if stock is overbought or oversold.
    MACD tells if momentum is turning up or down.
    These are used by traders to time their entry and exit.
    """
    try:
        stock = yf.Ticker(ticker)
        df    = stock.history(period=period)

        # --- RSI (Relative Strength Index) ---
        # above 70 = overbought (might fall), below 30 = oversold (might rise)
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

        # --- MACD (Moving Average Convergence Divergence) ---
        # when MACD crosses above signal line = bullish, below = bearish
        macd = ta.trend.MACD(df["Close"])
        df["MACD"]        = macd.macd()
        df["MACD_Signal"]  = macd.macd_signal()
        df["MACD_Hist"]    = macd.macd_diff()

        # --- Bollinger Bands ---
        # price near upper band = overbought, near lower band = oversold
        bb = ta.volatility.BollingerBands(df["Close"], window=20)
        df["BB_Upper"] = bb.bollinger_hband()
        df["BB_Lower"] = bb.bollinger_lband()
        df["BB_Mid"]   = bb.bollinger_mavg()

        # --- Moving Averages ---
        df["MA_50"]  = df["Close"].rolling(window=50).mean()
        df["MA_200"] = df["Close"].rolling(window=200).mean()

        # --- latest readings ---
        latest = df.iloc[-1]
        rsi_val  = round(latest["RSI"], 2)
        macd_val = round(latest["MACD"], 2)
        sig_val  = round(latest["MACD_Signal"], 2)
        price    = round(latest["Close"], 2)
        ma50     = round(latest["MA_50"], 2)
        ma200    = round(latest["MA_200"], 2)

        print(f"\n===== Technical Analysis: {ticker} =====")
        print(f"Current Price : {price}")
        print(f"RSI (14)      : {rsi_val}  {'— Overbought' if rsi_val > 70 else '— Oversold' if rsi_val < 30 else '— Neutral'}")
        print(f"MACD          : {macd_val}  |  Signal: {sig_val}  {'— Bullish' if macd_val > sig_val else '— Bearish'}")
        print(f"MA 50         : {ma50}  |  MA 200: {ma200}  {'— Golden Cross (Bullish)' if ma50 > ma200 else '— Death Cross (Bearish)'}")

        df.to_csv(f"data/raw/{ticker}_technicals.csv")
        print(f"Saved to data/raw/{ticker}_technicals.csv")
        return df

    except Exception as e:
        print(f"Technical Error: {e}")
        return None

if __name__ == "__main__":
    calculate_technicals("RELIANCE.NS")