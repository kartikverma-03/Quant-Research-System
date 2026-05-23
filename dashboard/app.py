import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import sys, os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.dcf       import calculate_dcf
from models.ratios    import calculate_ratios
from models.technical import calculate_technicals

# ── AI report directly inside app ────────────────────────────
def run_ai_report(ticker):
    try:
        from google import genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None, "GEMINI_API_KEY not found in .env file"

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
Write a professional stock research report for {name} ({ticker}).

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

Write a 200-word analyst report covering:
1. Business overview (1 sentence)
2. Valuation assessment based on the ratios
3. Financial health and profitability
4. Key risks
5. Final verdict: Buy, Hold, or Sell with reason

Be specific and use the actual numbers provided.
        """

        client   = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model    = "gemini-2.5-flash",
            contents = prompt
        )
        return response.text, None

    except Exception as e:
        return None, str(e)

# ── page config ───────────────────────────────────────────────
st.set_page_config(
    page_title = "QuantEdge Research",
    page_icon  = "⚡",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1224 50%, #0a0e1a 100%); color: #e2e8f0; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1224 0%, #111827 100%); border-right: 1px solid #1e3a5f; }
[data-testid="stMetric"] { background: linear-gradient(135deg, #0d1f3c 0%, #0a1628 100%); border: 1px solid #1e3a5f; border-radius: 12px; padding: 16px; }
[data-testid="stMetricValue"] { color: #60a5fa !important; font-size: 1.4rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 1px; }
.stButton > button { background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%); color: white; border: none; border-radius: 8px; font-weight: 600; letter-spacing: 0.5px; width: 100%; box-shadow: 0 0 20px rgba(29,78,216,0.4); }
.stButton > button:hover { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); box-shadow: 0 0 30px rgba(29,78,216,0.6); transform: translateY(-1px); }
.stTextInput > div > div > input { background: #0d1f3c; border: 1px solid #1e3a5f; border-radius: 8px; color: #e2e8f0; }
.stSelectbox > div > div { background: #0d1f3c; border: 1px solid #1e3a5f; border-radius: 8px; color: #e2e8f0; }
hr { border-color: #1e3a5f; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── header ────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0d1f3c 0%,#0a1628 100%);border:1px solid #1e3a5f;border-radius:16px;padding:28px 36px;margin-bottom:24px;">
    <div style="display:flex;align-items:center;gap:16px;">
        <div style="background:linear-gradient(135deg,#1d4ed8,#7c3aed);border-radius:12px;width:52px;height:52px;display:flex;align-items:center;justify-content:center;font-size:26px;">⚡</div>
        <div>
            <h1 style="margin:0;font-size:1.8rem;font-weight:700;background:linear-gradient(90deg,#60a5fa,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">QuantEdge Research</h1>
            <p style="margin:0;color:#64748b;font-size:0.82rem;letter-spacing:2px;">PROFESSIONAL STOCK RESEARCH & VALUATION PLATFORM</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="color:#94a3b8;font-size:0.72rem;letter-spacing:1px;margin-bottom:6px;">STOCK LOOKUP</p>', unsafe_allow_html=True)
    ticker  = st.text_input("", value="RELIANCE.NS", placeholder="e.g. TCS.NS, AAPL").upper()
    period  = st.selectbox("Time Period", ["6mo","1y","2y","5y"], index=2,
                           format_func=lambda x: {"6mo":"6 Months","1y":"1 Year","2y":"2 Years","5y":"5 Years"}[x])
    analyse = st.button("⚡  ANALYSE STOCK")

    st.markdown("---")
    st.markdown("""
    <div style="background:#0d1f3c;border:1px solid #1e3a5f;border-radius:10px;padding:14px;">
        <p style="color:#94a3b8;font-size:0.72rem;letter-spacing:1px;margin:0 0 8px;">QUICK PICKS</p>
        <p style="color:#60a5fa;font-size:0.82rem;margin:4px 0;">🇮🇳 RELIANCE.NS · TCS.NS</p>
        <p style="color:#60a5fa;font-size:0.82rem;margin:4px 0;">🇮🇳 INFY.NS · HDFCBANK.NS</p>
        <p style="color:#60a5fa;font-size:0.82rem;margin:4px 0;">🇺🇸 AAPL · MSFT · GOOGL</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top:12px;background:#0d1f3c;border:1px solid #1e3a5f;border-radius:10px;padding:14px;">
        <p style="color:#94a3b8;font-size:0.72rem;letter-spacing:1px;margin:0 0 6px;">TICKER FORMAT</p>
        <p style="color:#64748b;font-size:0.8rem;margin:2px 0;">NSE → add <b style="color:#60a5fa">.NS</b></p>
        <p style="color:#64748b;font-size:0.8rem;margin:2px 0;">BSE → add <b style="color:#60a5fa">.BO</b></p>
        <p style="color:#64748b;font-size:0.8rem;margin:2px 0;">US  → just the symbol</p>
    </div>
    """, unsafe_allow_html=True)

# ── landing page ──────────────────────────────────────────────
if not analyse:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px 40px;">
        <div style="font-size:4rem;margin-bottom:12px;">📊</div>
        <h2 style="color:#60a5fa;font-weight:600;margin-bottom:8px;">Enter a stock ticker to begin</h2>
        <p style="color:#475569;font-size:1rem;">DCF Valuation · Ratio Analysis · Technical Signals · AI Analyst Reports</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, desc in [
        (c1, "💹", "DCF Valuation",    "Intrinsic value from cash flows"),
        (c2, "📐", "Ratio Analysis",   "P/E, ROE, EV/EBITDA & more"),
        (c3, "📡", "Technical Signals","RSI, MACD, Bollinger Bands"),
        (c4, "🤖", "AI Reports",       "Gemini-powered analyst reports"),
    ]:
        col.markdown(f"""
        <div style="background:#0d1f3c;border:1px solid #1e3a5f;border-radius:12px;padding:20px;text-align:center;min-height:130px;">
            <div style="font-size:2rem;">{icon}</div>
            <p style="color:#60a5fa;font-weight:600;margin:8px 0 4px;font-size:0.95rem;">{title}</p>
            <p style="color:#475569;font-size:0.8rem;margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── fetch data ────────────────────────────────────────────
    with st.spinner(f"Fetching live data for {ticker}..."):
        try:
            stock = yf.Ticker(ticker)
            info  = stock.info
            hist  = stock.history(period=period)
            if hist.empty:
                st.error(f"No data found for **{ticker}**. Please check the ticker symbol.")
                st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    name     = info.get("longName", ticker)
    price    = info.get("currentPrice", 0)
    change   = info.get("regularMarketChangePercent", 0) or 0
    sector   = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    mktcap   = info.get("marketCap", 0) or 0
    color    = "#22c55e" if change >= 0 else "#ef4444"
    arrow    = "▲" if change >= 0 else "▼"

    # ── company banner ────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1f3c 0%,#0a1628 100%);border:1px solid #1e3a5f;border-radius:16px;padding:24px 32px;margin-bottom:20px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
                <h2 style="margin:0;color:#f1f5f9;font-size:1.5rem;font-weight:700;">{name}</h2>
                <p style="margin:4px 0 0;color:#64748b;font-size:0.85rem;">{ticker} &nbsp;·&nbsp; {sector} &nbsp;·&nbsp; {industry}</p>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2rem;font-weight:700;color:#f1f5f9;">₹{price:,.2f}</div>
                <div style="font-size:1rem;color:{color};font-weight:600;">{arrow} {abs(change):.2f}% today</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── metrics ───────────────────────────────────────────────
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Market Cap",   f"₹{mktcap/1e7:,.0f} Cr")
    m2.metric("P/E Ratio",    f"{info.get('trailingPE','N/A')}")
    m3.metric("Price/Book",   f"{info.get('priceToBook','N/A')}")
    m4.metric("ROE",          f"{round((info.get('returnOnEquity') or 0)*100,1)}%")
    m5.metric("Debt/Equity",  f"{info.get('debtToEquity','N/A')}")
    m6.metric("52W High",     f"₹{info.get('fiftyTwoWeekHigh','N/A')}")

    st.markdown("---")

    # ── candlestick chart ─────────────────────────────────────
    st.markdown('<p style="color:#94a3b8;font-size:0.75rem;letter-spacing:1px;margin-bottom:6px;">PRICE CHART</p>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"], name="Price",
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444"
    ))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(20).mean(),
                             name="MA 20", line=dict(color="#60a5fa", width=1.5)))
    fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(50).mean(),
                             name="MA 50", line=dict(color="#a78bfa", width=1.5)))
    fig.update_layout(
        paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1224", font_color="#94a3b8",
        height=420, margin=dict(l=0,r=0,t=10,b=0),
        legend=dict(bgcolor="#0d1f3c", bordercolor="#1e3a5f", borderwidth=1),
        xaxis=dict(gridcolor="#1e2a3a", rangeslider_visible=False),
        yaxis=dict(gridcolor="#1e2a3a"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── volume bar chart ──────────────────────────────────────
    vol_colors = ["#22c55e" if c >= o else "#ef4444"
                  for c, o in zip(hist["Close"], hist["Open"])]
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(x=hist.index, y=hist["Volume"],
                             marker_color=vol_colors, name="Volume"))
    fig_vol.update_layout(
        paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1224", font_color="#94a3b8",
        height=150, margin=dict(l=0,r=0,t=4,b=0), showlegend=False,
        xaxis=dict(gridcolor="#1e2a3a"), yaxis=dict(gridcolor="#1e2a3a")
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("---")

    # ── valuation columns ─────────────────────────────────────
    st.markdown('<p style="color:#94a3b8;font-size:0.75rem;letter-spacing:1px;margin-bottom:10px;">VALUATION ANALYSIS</p>', unsafe_allow_html=True)

    col_dcf, col_ratio, col_tech = st.columns(3)

    with col_dcf:
        st.markdown('<div style="background:#0d1f3c;border:1px solid #1e3a5f;border-radius:12px;padding:16px;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#60a5fa;font-size:0.72rem;letter-spacing:1px;margin:0 0 12px;">💹 DCF VALUATION</p>', unsafe_allow_html=True)
        with st.spinner(""):
            fair_value, upside, verdict = calculate_dcf(ticker)
        if fair_value:
            st.metric("Fair Value",  f"₹{fair_value:,.2f}")
            st.metric("Upside",      f"{upside:+.1f}%")
            vc = "#22c55e" if upside and upside > 0 else "#ef4444"
            st.markdown(f'<p style="color:{vc};font-weight:600;font-size:0.9rem;margin-top:8px;">{verdict}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ratio:
        st.markdown('<div style="background:#0d1f3c;border:1px solid #1e3a5f;border-radius:12px;padding:16px;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#a78bfa;font-size:0.72rem;letter-spacing:1px;margin:0 0 12px;">📐 RATIO ANALYSIS</p>', unsafe_allow_html=True)
        with st.spinner(""):
            ratios = calculate_ratios(ticker)
        if ratios:
            for label, key in [("EV/EBITDA","ev_ebitda"),("P/E Ratio","pe"),("P/B Ratio","pb")]:
                val = ratios.get(key, "N/A")
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #1e2a3a;">
                    <span style="color:#64748b;font-size:0.85rem;">{label}</span>
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.85rem;">{val}</span>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tech:
        st.markdown('<div style="background:#0d1f3c;border:1px solid #1e3a5f;border-radius:12px;padding:16px;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#f59e0b;font-size:0.72rem;letter-spacing:1px;margin:0 0 12px;">📡 TECHNICAL SIGNALS</p>', unsafe_allow_html=True)
        with st.spinner(""):
            tech_df = calculate_technicals(ticker)
        if tech_df is not None:
            latest    = tech_df.iloc[-1]
            rsi       = round(latest["RSI"], 1)
            macd_v    = round(latest["MACD"], 2)
            sig_v     = round(latest["MACD_Signal"], 2)
            rsi_color = "#ef4444" if rsi > 70 else "#22c55e" if rsi < 30 else "#f59e0b"
            rsi_label = "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"
            mc        = "#22c55e" if macd_v > sig_v else "#ef4444"
            ml        = "Bullish" if macd_v > sig_v else "Bearish"
            st.markdown(f"""
            <div style="padding:7px 0;border-bottom:1px solid #1e2a3a;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#64748b;font-size:0.85rem;">RSI (14)</span>
                    <span style="color:{rsi_color};font-weight:600;font-size:0.85rem;">{rsi} — {rsi_label}</span>
                </div>
            </div>
            <div style="padding:7px 0;border-bottom:1px solid #1e2a3a;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#64748b;font-size:0.85rem;">MACD</span>
                    <span style="color:{mc};font-weight:600;font-size:0.85rem;">{ml}</span>
                </div>
            </div>
            <div style="padding:7px 0;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="color:#64748b;font-size:0.85rem;">MA 50 / 200</span>
                    <span style="color:#e2e8f0;font-size:0.85rem;">{round(latest['MA_50'],1)} / {round(latest['MA_200'],1)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── AI report ─────────────────────────────────────────────
    st.markdown('<p style="color:#94a3b8;font-size:0.75rem;letter-spacing:1px;margin-bottom:10px;">AI ANALYST REPORT</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a0a2e 0%,#0d0a1f 100%);border:1px solid #4c1d95;border-radius:12px;padding:20px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.6rem;">🤖</span>
            <div>
                <p style="margin:0;color:#a78bfa;font-weight:600;font-size:1rem;">Gemini AI Analyst</p>
                <p style="margin:0;color:#6d28d9;font-size:0.75rem;">Powered by Google Gemini 2.5 Flash</p>
            </div>
        </div>
        <p style="margin:12px 0 0;color:#64748b;font-size:0.85rem;">
            Click below to generate a professional equity research report with
            valuation assessment, risk analysis, and investment verdict.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🤖  GENERATE AI ANALYST REPORT"):
        with st.spinner("Gemini is analysing the financials and writing your report..."):
            report, error = run_ai_report(ticker)

        if report:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0a1628 0%,#0d1f3c 100%);border:1px solid #1e3a5f;border-radius:12px;padding:24px;margin-top:8px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
                    <span style="background:#7c3aed;color:white;font-size:0.7rem;padding:3px 10px;border-radius:20px;font-weight:600;">AI GENERATED</span>
                    <span style="color:#475569;font-size:0.8rem;">{name} · {ticker}</span>
                </div>
                <div style="color:#cbd5e1;line-height:1.9;font-size:0.95rem;">
                    {report.replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label     = "⬇  Download Report",
                data      = report,
                file_name = f"{ticker}_analyst_report.txt",
                mime      = "text/plain"
            )
        else:
            st.error(f"Report failed: {error}")

    st.markdown("---")
    st.markdown('<p style="text-align:center;color:#1e3a5f;font-size:0.75rem;">QuantEdge Research · Built with Python, Streamlit & Gemini AI · For educational purposes only</p>', unsafe_allow_html=True)