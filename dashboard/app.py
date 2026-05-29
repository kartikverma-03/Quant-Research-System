import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import sys, os, re
from datetime import datetime
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
st.sidebar.write("KEY:", os.getenv("GEMINI_API_KEY", "NOT FOUND"))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.dcf       import calculate_dcf
from models.ratios    import calculate_ratios
from models.technical import calculate_technicals

# ─────────────────────────────────────────────────────────────
#  AI  — uses new google-genai SDK, self-contained
# ─────────────────────────────────────────────────────────────
def run_ai_report(ticker, info):
    try:
        from google import genai
        import dotenv
        dotenv.load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return None, "GEMINI_API_KEY not found in .env file"
        prompt = f"""You are a senior equity analyst at Goldman Sachs.
Write a sharp, high-conviction research note for {info.get('longName', ticker)} ({ticker}).

Data: Sector={info.get('sector','N/A')}, Price={info.get('currentPrice','N/A')},
MarketCap={info.get('marketCap','N/A')}, P/E={info.get('trailingPE','N/A')},
P/B={info.get('priceToBook','N/A')}, ROE={info.get('returnOnEquity','N/A')},
ProfitMargin={info.get('profitMargins','N/A')}, D/E={info.get('debtToEquity','N/A')},
52W-High={info.get('fiftyTwoWeekHigh','N/A')}, 52W-Low={info.get('fiftyTwoWeekLow','N/A')}

Use exactly these headers:
**OVERVIEW** — one sentence on the business
**VALUATION** — cheap or expensive and why
**FINANCIAL HEALTH** — profitability and balance sheet quality
**CATALYSTS** — 2 things that could drive the stock higher
**RISKS** — 2 key downside risks
**VERDICT** — Buy / Hold / Sell with a 12-month price target

Be direct, use the actual numbers, sound like a real Wall Street analyst. 220 words max."""
        client   = genai.Client(api_key=key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text, None
    except Exception as e:
        return None, str(e)

def run_ai_screener(df):
    try:
        from google import genai
        import dotenv
        dotenv.load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return "Add GEMINI_API_KEY to .env to enable AI commentary."
        summary = df[["Ticker","Price","P/E","ROE %","Sector"]].to_string(index=False)
        prompt  = f"You are a quant analyst. In 3 sentences, which stock looks most interesting from this screener and why?\n{summary}"
        client   = genai.Client(api_key=key)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text
    except Exception as e:
        return f"AI commentary unavailable: {e}"

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quantivo Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  DESIGN SYSTEM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Playfair+Display:wght@600;700&display=swap');

:root {
  --white:      #ffffff;
  --bg:         #f7f8fc;
  --bg2:        #eef1f8;
  --sidebar-bg: #ffffff;
  --chart-bg:   #0d1117;
  --chart-surf: #161b22;
  --blue:       #1a56db;
  --blue-lt:    #3b82f6;
  --blue-pale:  #eff6ff;
  --blue-mid:   #dbeafe;
  --border:     #e2e8f0;
  --border-b:   rgba(26,86,219,0.15);
  --text:       #0f172a;
  --muted:      #64748b;
  --muted2:     #94a3b8;
  --green:      #059669;
  --green-bg:   #f0fdf4;
  --red:        #dc2626;
  --red-bg:     #fef2f2;
  --shadow:     0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(26,86,219,0.06);
  --shadow-md:  0 4px 24px rgba(26,86,219,0.1);
  --shadow-lg:  0 8px 40px rgba(26,86,219,0.14);
}

*, html, body { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1.8rem 2rem; max-width: 100%; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 20px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.6rem 1.1rem; }

[data-testid="collapsedControl"] {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 50% !important;
    box-shadow: var(--shadow) !important;
    color: var(--blue) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--blue), var(--blue-lt));
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.15rem !important;
    font-weight: 500 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.62rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: var(--blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    width: 100% !important;
    box-shadow: 0 2px 8px rgba(26,86,219,0.3) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #1648c0 !important;
    box-shadow: 0 4px 16px rgba(26,86,219,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 9px 12px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(26,86,219,0.08) !important;
}
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stTextArea label {
    color: var(--muted) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    box-shadow: var(--shadow);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 8px 14px !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--blue) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(26,86,219,0.25) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: var(--blue-pale) !important;
    color: var(--blue) !important;
}

/* ── DIVIDER ── */
hr { border: none; border-top: 1px solid var(--border); margin: 1.2rem 0; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--blue-mid); border-radius: 4px; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ── ALERTS ── */
.stSuccess { background: var(--green-bg) !important; border: 1px solid #bbf7d0 !important; border-radius: 8px !important; }
.stError   { background: var(--red-bg)   !important; border: 1px solid #fecaca !important; border-radius: 8px !important; }
.stInfo    { background: var(--blue-pale) !important; border: 1px solid var(--blue-mid) !important; border-radius: 8px !important; }
.stWarning { background: #fffbeb !important; border: 1px solid #fde68a !important; border-radius: 8px !important; }

/* ── DOWNLOAD BTN ── */
[data-testid="stDownloadButton"] > button {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    color: var(--blue) !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: var(--shadow) !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden !important; }

/* ── ANIMATIONS ── */
@keyframes fadeUp   { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn   { from { opacity:0; } to { opacity:1; } }
@keyframes floatAni { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-5px);} }
@keyframes pulse    { 0%,100%{opacity:1;} 50%{opacity:.5;} }
@keyframes slideL   { from{opacity:0;transform:translateX(-16px);} to{opacity:1;transform:translateX(0);} }

.card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s, transform 0.2s;
    animation: fadeUp 0.4s ease both;
    margin-bottom: 0;
}
.card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }

.card-dark {
    background: var(--chart-bg);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    animation: fadeUp 0.4s ease both;
}

.badge {
    display: inline-block;
    background: var(--blue-pale);
    color: var(--blue);
    border: 1px solid var(--blue-mid);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-right: 4px;
}
.badge-green { background:#f0fdf4; color:#059669; border-color:#bbf7d0; }
.badge-red   { background:#fef2f2; color:#dc2626; border-color:#fecaca; }
.badge-gray  { background:#f8fafc; color:#64748b; border-color:#e2e8f0; }

.tag { display:inline-block; background:var(--bg2); color:var(--muted); border-radius:6px; padding:2px 8px; font-size:0.68rem; font-weight:500; margin-right:4px; }

.stat-row { display:flex; justify-content:space-between; align-items:center; padding:7px 0; border-bottom:1px solid var(--bg2); }
.stat-lbl  { font-size:0.72rem; color:var(--muted); font-weight:500; }
.stat-val  { font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:var(--text); font-weight:500; }

.section-label { font-size:0.62rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--muted2); margin:0 0 10px; }

.live-dot { display:inline-block; width:7px; height:7px; background:#22c55e; border-radius:50%; animation:pulse 2s infinite; box-shadow:0 0 6px rgba(34,197,94,0.5); margin-right:5px; }

.nav-item { padding:8px 10px; border-radius:8px; cursor:pointer; transition:all 0.15s; display:flex; align-items:center; gap:8px; font-size:0.82rem; font-weight:500; color:var(--muted); margin-bottom:2px; }
.nav-item:hover { background:var(--blue-pale); color:var(--blue); }
.nav-item.active { background:var(--blue-pale); color:var(--blue); font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","AAPL"]
if "analyse" not in st.session_state:
    st.session_state.analyse = False
if "analysed_ticker" not in st.session_state:
    st.session_state.analysed_ticker = ""
if "analysed_period" not in st.session_state:
    st.session_state.analysed_period = "2y"

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0 4px 20px;animation:slideL 0.4s ease both;">
      <div style="width:36px;height:36px;border-radius:10px;
           background:linear-gradient(135deg,#1a56db,#3b82f6);
           display:flex;align-items:center;justify-content:center;
           font-size:17px;box-shadow:0 4px 12px rgba(26,86,219,0.3);
           animation:floatAni 3s ease-in-out infinite;">📈</div>
      <div>
        <p style="margin:0;font-family:'Playfair Display',serif;font-size:1.1rem;
           font-weight:700;color:#0f172a;letter-spacing:-0.3px;">Quantivo</p>
        <p style="margin:0;font-size:0.58rem;color:#94a3b8;font-weight:600;letter-spacing:1.5px;">RESEARCH PLATFORM</p>
      </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,#1a56db22,transparent);margin-bottom:18px;"></div>
    """, unsafe_allow_html=True)

    # Search
    st.markdown('<p class="section-label">Stock Lookup</p>', unsafe_allow_html=True)
    ticker = st.text_input("", value="RELIANCE.NS", placeholder="e.g. TCS.NS, AAPL").upper().strip()
    period = st.selectbox("", ["3mo","6mo","1y","2y","5y"], index=3,
                          format_func=lambda x: {"3mo":"3 Months","6mo":"6 Months",
                                                  "1y":"1 Year","2y":"2 Years","5y":"5 Years"}[x])

    # ── FIX: store analyse state in session_state so other buttons don't reset it ──
    if st.button("📊  Analyse Stock"):
        st.session_state.analyse = True
        st.session_state.analysed_ticker = ticker
        st.session_state.analysed_period = period

    # Reset if ticker changed manually
    if st.session_state.analysed_ticker and st.session_state.analysed_ticker != ticker:
        st.session_state.analyse = False

    analyse = st.session_state.analyse

    st.markdown("<hr>", unsafe_allow_html=True)

    # Live watchlist
    st.markdown('<p class="section-label">Watchlist</p>', unsafe_allow_html=True)
    for sym in st.session_state.watchlist[:5]:
        try:
            inf = yf.Ticker(sym).info
            p   = inf.get("currentPrice",0) or 0
            c   = inf.get("regularMarketChangePercent",0) or 0
            cc  = "#059669" if c>=0 else "#dc2626"
            cbg = "#f0fdf4" if c>=0 else "#fef2f2"
            ar  = "▲" if c>=0 else "▼"
            st.markdown(f"""
            <div style="background:white;border:1px solid #e2e8f0;border-radius:9px;
                 padding:8px 11px;margin-bottom:4px;display:flex;
                 justify-content:space-between;align-items:center;
                 transition:all 0.15s;animation:fadeUp 0.4s ease both;">
              <div>
                <p style="margin:0;font-size:0.8rem;font-weight:600;color:#0f172a;">{sym}</p>
                <p style="margin:0;font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#64748b;">₹{p:,.0f}</p>
              </div>
              <span style="background:{cbg};color:{cc};font-size:0.68rem;font-weight:700;
                   padding:3px 8px;border-radius:6px;font-family:'IBM Plex Mono',monospace;">
                {ar} {abs(c):.1f}%
              </span>
            </div>""", unsafe_allow_html=True)
        except:
            pass

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;
         border-radius:10px;padding:12px;animation:fadeUp 0.5s ease both;">
      <p style="margin:0 0 6px;font-size:0.62rem;font-weight:700;color:#1a56db;letter-spacing:1px;">TICKER FORMAT</p>
      <p style="margin:2px 0;font-size:0.76rem;color:#64748b;">🇮🇳 NSE → symbol<b style="color:#1a56db;">.NS</b></p>
      <p style="margin:2px 0;font-size:0.76rem;color:#64748b;">🇮🇳 BSE → symbol<b style="color:#1a56db;">.BO</b></p>
      <p style="margin:2px 0;font-size:0.76rem;color:#64748b;">🇺🇸 US → <b style="color:#1a56db;">AAPL MSFT GOOGL</b></p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  TOP NAV BAR
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:white;border-bottom:1px solid #e2e8f0;
     padding:12px 0 12px;margin-bottom:20px;display:flex;
     align-items:center;justify-content:space-between;
     box-shadow:0 1px 4px rgba(0,0,0,0.04);animation:fadeIn 0.4s ease both;">
  <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;">
      <span class="live-dot"></span>
      <span style="font-size:0.72rem;font-weight:600;color:#059669;">Markets Open</span>
    </div>
    <span style="font-size:0.72rem;color:#94a3b8;">|</span>
    <span style="font-size:0.72rem;color:#64748b;font-family:'IBM Plex Mono',monospace;">
      NSE · BSE · NYSE · NASDAQ · LSE
    </span>
  </div>
  <div style="display:flex;align-items:center;gap:8px;">
    <span style="background:#eff6ff;color:#1a56db;font-size:0.68rem;font-weight:700;
         padding:3px 10px;border-radius:20px;border:1px solid #dbeafe;">
      ✨ AI-Powered Research
    </span>
    <span style="background:#f0fdf4;color:#059669;font-size:0.68rem;font-weight:700;
         padding:3px 10px;border-radius:20px;border:1px solid #bbf7d0;">
      DCF · Ratios · Technicals
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  LANDING PAGE
# ─────────────────────────────────────────────────────────────
if not analyse:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 32px;animation:fadeUp 0.5s ease both;">
      <div style="display:inline-block;background:linear-gradient(135deg,#eff6ff,#dbeafe);
           border:1px solid #bfdbfe;border-radius:20px;padding:5px 16px;
           font-size:0.68rem;font-weight:700;color:#1a56db;letter-spacing:2px;margin-bottom:18px;">
        QUANTITATIVE EQUITY RESEARCH · AI-POWERED
      </div>
      <h1 style="font-family:'Playfair Display',serif;font-size:3rem;font-weight:700;
          color:#0f172a;margin:0 0 12px;letter-spacing:-1px;line-height:1.15;">
        Professional Stock Research,<br>
        <span style="background:linear-gradient(135deg,#1a56db,#3b82f6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
          Built from Scratch.
        </span>
      </h1>
      <p style="color:#64748b;font-size:1rem;max-width:560px;margin:0 auto 16px;line-height:1.7;">
        Investment-bank-grade DCF modelling · Ratio analysis · Technical signals ·
        AI-generated equity research notes — all in one platform.
      </p>
      <p style="color:#94a3b8;font-size:0.78rem;margin:0;">
        ← Enter a ticker in the sidebar and click <b style="color:#1a56db;">Analyse Stock</b>
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    cols = st.columns(3)
    features = [
        ("📊","DCF Valuation","Replicates the exact discounted cash flow model used by investment banks. Projects free cash flows, calculates WACC and terminal value to find intrinsic stock value.","blue"),
        ("📐","Ratio Analysis","P/E, EV/EBITDA, ROE, Debt/Equity and 8 more ratios pulled live. Compare against sector peers to identify mis-priced stocks.","blue"),
        ("📡","Technical Signals","RSI, MACD, Bollinger Bands and moving average crossover signals. Golden Cross / Death Cross detection with live chart overlays.","blue"),
        ("🤖","AI Analyst Reports","Gemini 2.5 Flash writes a Goldman Sachs-style research note from live financial data — with catalysts, risks and a 12-month price target.","blue"),
        ("🔍","Smart Screener","Filter any universe of stocks by P/E, ROE, debt ratio and margin. AI commentary identifies the most compelling opportunity from results.","blue"),
        ("💼","Portfolio Tracker","Track positions with live P&L, allocation pie chart and total return metrics. Add any global stock and see performance in real time.","blue"),
    ]
    for i,(icon,title,desc,_) in enumerate(features):
        with cols[i%3]:
            delay = i * 0.07
            st.markdown(f"""
            <div class="card" style="animation-delay:{delay}s;margin-bottom:14px;">
              <div style="width:40px;height:40px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                   border:1px solid #bfdbfe;border-radius:12px;display:flex;align-items:center;
                   justify-content:center;font-size:20px;margin-bottom:12px;">{icon}</div>
              <p style="font-weight:700;font-size:0.92rem;color:#0f172a;margin:0 0 6px;">{title}</p>
              <p style="color:#64748b;font-size:0.78rem;line-height:1.6;margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    # Resume callout
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a56db,#1648c0);border-radius:16px;
         padding:28px 32px;margin-top:12px;animation:fadeUp 0.6s ease both;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
        <div>
          <p style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;
             color:white;margin:0 0 6px;">Built as a BTech 2nd Year Project</p>
          <p style="color:rgba(255,255,255,0.75);font-size:0.85rem;margin:0;">
            DCF modelling · Quantitative finance · Generative AI integration · Full-stack Python
          </p>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <span style="background:rgba(255,255,255,0.15);color:white;border-radius:8px;
               padding:5px 12px;font-size:0.72rem;font-weight:600;">Python</span>
          <span style="background:rgba(255,255,255,0.15);color:white;border-radius:8px;
               padding:5px 12px;font-size:0.72rem;font-weight:600;">Streamlit</span>
          <span style="background:rgba(255,255,255,0.15);color:white;border-radius:8px;
               padding:5px 12px;font-size:0.72rem;font-weight:600;">Gemini AI</span>
          <span style="background:rgba(255,255,255,0.15);color:white;border-radius:8px;
               padding:5px 12px;font-size:0.72rem;font-weight:600;">Plotly</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────
#  FETCH DATA  — use the saved ticker/period from session state
# ─────────────────────────────────────────────────────────────
ticker = st.session_state.analysed_ticker
period = st.session_state.analysed_period

with st.spinner(f"Fetching live data for {ticker}..."):
    try:
        stock = yf.Ticker(ticker)
        info  = stock.info
        hist  = stock.history(period=period)
        news  = stock.news or []
        if hist.empty:
            st.error(f"No data found for **{ticker}**. Check the symbol.")
            st.stop()
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

name     = info.get("longName", ticker)
price    = info.get("currentPrice",0) or 0
change   = info.get("regularMarketChangePercent",0) or 0
sector   = info.get("sector","N/A")
industry = info.get("industry","N/A")
mktcap   = info.get("marketCap",0) or 0
chg_c    = "#059669" if change>=0 else "#dc2626"
chg_bg   = "#f0fdf4" if change>=0 else "#fef2f2"
arrow    = "▲" if change>=0 else "▼"

# ─────────────────────────────────────────────────────────────
#  COMPANY HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:white;border:1px solid #e2e8f0;border-radius:16px;
     padding:20px 24px;margin-bottom:18px;box-shadow:var(--shadow);
     animation:fadeUp 0.4s ease both;
     background:linear-gradient(135deg,white 65%,#f0f7ff 100%);">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
        <span class="live-dot"></span>
        <span style="font-size:0.62rem;font-weight:700;color:#64748b;letter-spacing:2px;">LIVE · EQUITY RESEARCH</span>
      </div>
      <h2 style="font-family:'Playfair Display',serif;font-size:1.55rem;font-weight:700;
          color:#0f172a;margin:0 0 8px;letter-spacing:-0.3px;">{name}</h2>
      <div>
        <span class="badge">{ticker}</span>
        <span class="tag">{sector}</span>
        <span class="tag">{industry}</span>
      </div>
    </div>
    <div style="text-align:right;">
      <p style="font-family:'IBM Plex Mono',monospace;font-size:1.9rem;font-weight:600;
          color:#0f172a;margin:0;letter-spacing:-0.5px;">₹{price:,.2f}</p>
      <div style="display:inline-block;background:{chg_bg};color:{chg_c};
           font-family:'IBM Plex Mono',monospace;font-size:0.85rem;font-weight:700;
           padding:4px 12px;border-radius:6px;margin-top:4px;">
        {arrow} {abs(change):.2f}% today
      </div>
      <p style="color:#94a3b8;font-size:0.7rem;margin:5px 0 0;
          font-family:'IBM Plex Mono',monospace;">
        Mkt Cap ₹{mktcap/1e7:,.0f} Cr
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# KEY METRICS ROW
cols7 = st.columns(7)
metrics = [
    ("P/E Ratio",   f"{info.get('trailingPE','—')}"),
    ("Fwd P/E",     f"{info.get('forwardPE','—')}"),
    ("Price/Book",  f"{info.get('priceToBook','—')}"),
    ("ROE",         f"{round((info.get('returnOnEquity') or 0)*100,1)}%"),
    ("Debt/Equity", f"{info.get('debtToEquity','—')}"),
    ("52W High",    f"₹{info.get('fiftyTwoWeekHigh','—')}"),
    ("52W Low",     f"₹{info.get('fiftyTwoWeekLow','—')}"),
]
for col,(lbl,val) in zip(cols7,metrics):
    col.metric(lbl,val)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────────────────────
t1,t2,t3,t4,t5,t6 = st.tabs([
    "📊 Charts & Valuation",
    "🔍 Screener",
    "💼 Portfolio",
    "📰 News",
    "⚖️ Peers",
    "🤖 AI Analyst"
])

# plotly dark theme for charts
DARK = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    font=dict(family="IBM Plex Mono", color="#8b949e", size=10),
    margin=dict(l=0,r=0,t=10,b=0),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d",
               tickfont=dict(size=9,color="#8b949e")),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d",
               tickfont=dict(size=9,color="#8b949e"), side="right"),
)

# ══════════════════════════════════════════════════════════
#  TAB 1 — CHARTS & VALUATION
# ══════════════════════════════════════════════════════════
with t1:
    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3,1])

    with left:
        st.markdown('<p class="section-label">Price Action — Dark Chart</p>', unsafe_allow_html=True)
        # Candlestick — dark theme
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist.index, open=hist["Open"], high=hist["High"],
            low=hist["Low"], close=hist["Close"], name="OHLC",
            increasing=dict(line=dict(color="#3fb950",width=1),fillcolor="#196c2e"),
            decreasing=dict(line=dict(color="#f85149",width=1),fillcolor="#8e1519"),
        ))
        ma20 = hist["Close"].rolling(20).mean()
        ma50 = hist["Close"].rolling(50).mean()
        fig.add_trace(go.Scatter(x=hist.index,y=ma20,name="MA20",
            line=dict(color="#58a6ff",width=1.5)))
        fig.add_trace(go.Scatter(x=hist.index,y=ma50,name="MA50",
            line=dict(color="#f59e0b",width=1.2,dash="dot")))
        # FIX: avoid duplicate xaxis key by using update_xaxes separately
        fig.update_layout(**DARK, height=360,
            legend=dict(bgcolor="#161b22",bordercolor="#30363d",
                        borderwidth=1,font=dict(size=9,color="#8b949e"),x=0.01,y=0.99))
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Volume — dark
        vc = ["#196c2e" if c>=o else "#8e1519"
              for c,o in zip(hist["Close"],hist["Open"])]
        fv = go.Figure()
        fv.add_trace(go.Bar(x=hist.index,y=hist["Volume"],
                            marker_color=vc,name="Volume"))
        fv.update_layout(**DARK,height=100,showlegend=False)
        st.plotly_chart(fv, use_container_width=True)

    with right:
        st.markdown('<p class="section-label">Company Stats</p>', unsafe_allow_html=True)
        stats = [
            ("Revenue",     f"₹{(info.get('totalRevenue') or 0)/1e7:,.0f} Cr"),
            ("Net Income",  f"₹{(info.get('netIncomeToCommon') or 0)/1e7:,.0f} Cr"),
            ("Gross Margin",f"{round((info.get('grossMargins') or 0)*100,1)}%"),
            ("Op Margin",   f"{round((info.get('operatingMargins') or 0)*100,1)}%"),
            ("Beta",        f"{info.get('beta','—')}"),
            ("Div Yield",   f"{round((info.get('dividendYield') or 0)*100,2)}%"),
            ("EV/EBITDA",   f"{info.get('enterpriseToEbitda','—')}"),
            ("Float Shares",f"{(info.get('floatShares') or 0)/1e7:,.1f} Cr"),
        ]
        rows = "".join([f'<div class="stat-row"><span class="stat-lbl">{l}</span><span class="stat-val">{v}</span></div>' for l,v in stats])
        st.markdown(f'<div class="card">{rows}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">Valuation Models</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    v1,v2,v3 = st.columns(3)

    with v1:
        with st.spinner(""):
            fv_val,upside,verdict = calculate_dcf(ticker)
        uc  = "#059669" if (upside and upside>0) else "#dc2626"
        ubg = "#f0fdf4" if (upside and upside>0) else "#fef2f2"
        fvs = f"₹{fv_val:,.2f}" if fv_val else "—"
        ups = f"{upside:+.1f}%" if upside else "—"
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                 border:1px solid #bfdbfe;border-radius:10px;display:flex;align-items:center;
                 justify-content:center;font-size:17px;">💹</div>
            <div>
              <p style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0;">DCF Valuation</p>
              <p style="font-size:0.68rem;color:#94a3b8;margin:0;">Discounted Cash Flow Model</p>
            </div>
          </div>
          <p class="section-label">Intrinsic Value</p>
          <p style="font-family:'IBM Plex Mono',monospace;font-size:1.6rem;font-weight:600;
              color:#1a56db;margin:0 0 12px;">{fvs}</p>
          <p class="section-label">Upside / Downside</p>
          <div style="background:{ubg};border-radius:8px;padding:8px 12px;margin-bottom:10px;">
            <p style="font-family:'IBM Plex Mono',monospace;font-size:1.1rem;
                font-weight:700;color:{uc};margin:0;">{ups}</p>
          </div>
          <p style="font-size:0.8rem;font-weight:600;color:{uc};margin:0;">{verdict}</p>
        </div>""", unsafe_allow_html=True)

    with v2:
        with st.spinner(""):
            ratios = calculate_ratios(ticker) or {}
        items = [
            ("EV / EBITDA",  str(ratios.get("ev_ebitda","—"))),
            ("P / E Ratio",  str(ratios.get("pe","—"))),
            ("Price / Book", str(ratios.get("pb","—"))),
            ("Profit Margin",f"{round((info.get('profitMargins') or 0)*100,1)}%"),
            ("Return on Eq", f"{round((info.get('returnOnEquity') or 0)*100,1)}%"),
            ("Debt / Equity",str(ratios.get("debt_equity","—"))),
        ]
        rows = "".join([f'<div class="stat-row"><span class="stat-lbl">{l}</span><span class="stat-val">{v}</span></div>' for l,v in items])
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
            <div style="width:34px;height:34px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                 border:1px solid #bfdbfe;border-radius:10px;display:flex;align-items:center;
                 justify-content:center;font-size:17px;">📐</div>
            <div>
              <p style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0;">Ratio Analysis</p>
              <p style="font-size:0.68rem;color:#94a3b8;margin:0;">Key Financial Ratios</p>
            </div>
          </div>
          {rows}
        </div>""", unsafe_allow_html=True)

    with v3:
        with st.spinner(""):
            tech_df = calculate_technicals(ticker)
        if tech_df is not None:
            lt      = tech_df.iloc[-1]
            rsi     = round(lt["RSI"],1)
            macd_v  = round(lt["MACD"],2)
            sig_v   = round(lt["MACD_Signal"],2)
            ma50_v  = round(lt["MA_50"],1)
            ma200_v = round(lt["MA_200"],1)
            rc  = "#dc2626" if rsi>70 else "#059669" if rsi<30 else "#f59e0b"
            rl  = "Overbought" if rsi>70 else "Oversold" if rsi<30 else "Neutral"
            mc2 = "#059669" if macd_v>sig_v else "#dc2626"
            ml  = "Bullish" if macd_v>sig_v else "Bearish"
            xc  = "#059669" if ma50_v>ma200_v else "#dc2626"
            xl  = "Golden Cross 🟢" if ma50_v>ma200_v else "Death Cross 🔴"
            tech_items = [
                ("RSI (14)",   f'<span style="color:{rc};font-weight:700;">{rsi} — {rl}</span>'),
                ("MACD",       f'<span style="color:{mc2};font-weight:700;">{ml}</span>'),
                ("MA Cross",   f'<span style="color:{xc};font-weight:700;">{xl}</span>'),
                ("MA 50",      str(ma50_v)),
                ("MA 200",     str(ma200_v)),
                ("MACD Val",   str(macd_v)),
            ]
            rows = "".join([f'<div class="stat-row"><span class="stat-lbl">{l}</span><span class="stat-val">{v}</span></div>' for l,v in tech_items])
            st.markdown(f"""
            <div class="card">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                <div style="width:34px;height:34px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                     border:1px solid #bfdbfe;border-radius:10px;display:flex;align-items:center;
                     justify-content:center;font-size:17px;">📡</div>
                <div>
                  <p style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0;">Technical Signals</p>
                  <p style="font-size:0.68rem;color:#94a3b8;margin:0;">RSI · MACD · Moving Averages</p>
                </div>
              </div>
              {rows}
            </div>""", unsafe_allow_html=True)

    # RSI + MACD side by side — dark charts
    st.markdown("<hr>", unsafe_allow_html=True)
    r1,r2 = st.columns(2)
    with r1:
        st.markdown('<p class="section-label">RSI Indicator</p>', unsafe_allow_html=True)
        if tech_df is not None:
            fr = go.Figure()
            fr.add_trace(go.Scatter(x=tech_df.index,y=tech_df["RSI"],
                line=dict(color="#58a6ff",width=1.5),name="RSI",
                fill="tozeroy",fillcolor="rgba(88,166,255,0.07)"))
            fr.add_hline(y=70,line=dict(color="#f85149",width=1,dash="dot"))
            fr.add_hline(y=30,line=dict(color="#3fb950",width=1,dash="dot"))
            # FIX: avoid duplicate yaxis key by using update_yaxes separately
            fr.update_layout(**DARK,height=180,showlegend=False)
            fr.update_yaxes(range=[0,100])
            st.plotly_chart(fr,use_container_width=True)
    with r2:
        st.markdown('<p class="section-label">MACD</p>', unsafe_allow_html=True)
        if tech_df is not None:
            fm = go.Figure()
            fm.add_trace(go.Scatter(x=tech_df.index,y=tech_df["MACD"],
                line=dict(color="#58a6ff",width=1.5),name="MACD"))
            fm.add_trace(go.Scatter(x=tech_df.index,y=tech_df["MACD_Signal"],
                line=dict(color="#f59e0b",width=1.2,dash="dot"),name="Signal"))
            hc = ["#196c2e" if v>=0 else "#8e1519" for v in tech_df["MACD_Hist"]]
            fm.add_trace(go.Bar(x=tech_df.index,y=tech_df["MACD_Hist"],
                marker_color=hc,name="Histogram",opacity=0.7))
            fm.update_layout(**DARK,height=180,
                legend=dict(bgcolor="#161b22",bordercolor="#30363d",
                            font=dict(size=8,color="#8b949e"),x=0.01,y=0.99))
            st.plotly_chart(fm,use_container_width=True)

# ══════════════════════════════════════════════════════════
#  TAB 2 — SCREENER
# ══════════════════════════════════════════════════════════
with t2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="margin-bottom:18px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <span style="font-size:22px;">🔍</span>
        <div>
          <p style="font-weight:700;font-size:1rem;color:#0f172a;margin:0;">Smart Stock Screener</p>
          <p style="color:#64748b;font-size:0.78rem;margin:0;">Filter any universe of stocks by fundamental criteria</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    sc1,sc2,sc3 = st.columns(3)
    with sc1:
        pe_max  = st.number_input("Max P/E Ratio",     value=30.0, step=1.0)
        roe_min = st.number_input("Min ROE (%)",       value=10.0, step=1.0)
    with sc2:
        de_max  = st.number_input("Max Debt/Equity",   value=1.5,  step=0.1)
        pm_min  = st.number_input("Min Profit Margin (%)", value=5.0, step=1.0)
    with sc3:
        screen_tickers = st.text_input("Tickers to Screen (comma separated)",
            value="RELIANCE.NS,TCS.NS,INFY.NS,HDFCBANK.NS,WIPRO.NS,AAPL,MSFT,GOOGL")

    if st.button("🔍  Run Screener"):
        tlist   = [t.strip().upper() for t in screen_tickers.split(",") if t.strip()]
        results = []
        prog    = st.progress(0)
        for i,sym in enumerate(tlist):
            try:
                inf = yf.Ticker(sym).info
                pe  = inf.get("trailingPE") or 999
                roe = (inf.get("returnOnEquity") or 0)*100
                de  = inf.get("debtToEquity")  or 999
                pm  = (inf.get("profitMargins") or 0)*100
                if pe<=pe_max and roe>=roe_min and de<=de_max and pm>=pm_min:
                    results.append({
                        "Ticker":   sym,
                        "Name":     (inf.get("longName","") or sym)[:22],
                        "Sector":   inf.get("sector","N/A"),
                        "Price":    f"₹{inf.get('currentPrice',0):,.2f}",
                        "P/E":      round(pe,1),
                        "ROE %":    round(roe,1),
                        "D/E":      round(inf.get("debtToEquity",0) or 0,2),
                        "Margin %": round(pm,1),
                        "Mkt Cap":  f"₹{(inf.get('marketCap',0) or 0)/1e7:,.0f}Cr",
                    })
            except: pass
            prog.progress((i+1)/len(tlist))
        prog.empty()

        if results:
            st.success(f"✅ {len(results)} stock(s) passed your filters")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)
            with st.spinner("Gemini AI reviewing results..."):
                comment = run_ai_screener(df)
            st.markdown(f"""
            <div class="card" style="margin-top:14px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <span style="font-size:18px;">🤖</span>
                <p style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0;">AI Screener Commentary</p>
                <span class="badge">Gemini 2.5 Flash</span>
              </div>
              <div style="height:1px;background:linear-gradient(90deg,#dbeafe,transparent);margin-bottom:12px;"></div>
              <p style="color:#475569;font-size:0.88rem;line-height:1.85;margin:0;">{comment}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("No stocks passed your filters. Try relaxing the criteria.")

# ══════════════════════════════════════════════════════════
#  TAB 3 — PORTFOLIO
# ══════════════════════════════════════════════════════════
with t3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card" style="margin-bottom:18px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:22px;">💼</span>
        <div>
          <p style="font-weight:700;font-size:1rem;color:#0f172a;margin:0;">Portfolio Tracker</p>
          <p style="color:#64748b;font-size:0.78rem;margin:0;">Track positions with live P&L and allocation analytics</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    p1,p2,p3 = st.columns([2,1,1])
    with p1: add_t = st.text_input("Ticker",     placeholder="e.g. TCS.NS").upper().strip()
    with p2: add_q = st.number_input("Quantity",  min_value=1, value=10)
    with p3: add_p = st.number_input("Buy Price", min_value=0.01, value=100.0, step=0.01)

    ca,cb = st.columns(2)
    with ca:
        if st.button("➕  Add Position"):
            if add_t:
                st.session_state.portfolio.append({"ticker":add_t,"qty":add_q,"buy":add_p})
                st.success(f"Added {add_t} × {add_q} @ ₹{add_p:.2f}")
    with cb:
        if st.button("🗑️  Clear All"):
            st.session_state.portfolio = []
            st.rerun()

    if st.session_state.portfolio:
        st.markdown("<br>", unsafe_allow_html=True)
        rows=[]; total_val=0; total_cost=0
        for pos in st.session_state.portfolio:
            try:
                cur  = yf.Ticker(pos["ticker"]).info.get("currentPrice",0) or 0
                val  = cur*pos["qty"]; cost=pos["buy"]*pos["qty"]
                pnl  = val-cost; pp=(pnl/cost)*100 if cost else 0
                total_val+=val; total_cost+=cost
                rows.append({
                    "Ticker":  pos["ticker"], "Qty": pos["qty"],
                    "Buy":     f"₹{pos['buy']:,.2f}", "Current": f"₹{cur:,.2f}",
                    "Value":   f"₹{val:,.0f}", "P&L": f"₹{pnl:+,.0f}",
                    "Return":  f"{pp:+.1f}%",
                })
            except: pass

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)
            s1,s2,s3,s4 = st.columns(4)
            total_pnl = total_val-total_cost
            ret_pct   = (total_pnl/total_cost)*100 if total_cost else 0
            s1.metric("Total Value",   f"₹{total_val:,.0f}")
            s2.metric("Total Cost",    f"₹{total_cost:,.0f}")
            s3.metric("Total P&L",     f"₹{total_pnl:+,.0f}")
            s4.metric("Overall Return",f"{ret_pct:+.1f}%")

            labels = [r["Ticker"] for r in rows]
            values = [float(r["Value"].replace("₹","").replace(",","")) for r in rows]
            colors = ["#1a56db","#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#dbeafe"]
            fp = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.58,
                marker=dict(colors=colors[:len(labels)],
                            line=dict(color="white",width=2)),
                textfont=dict(family="Inter",size=10)
            ))
            fp.update_layout(paper_bgcolor="white",plot_bgcolor="white",height=240,
                margin=dict(l=0,r=0,t=8,b=0),
                legend=dict(bgcolor="white",bordercolor="#e2e8f0",font=dict(size=9)),
                annotations=[dict(text="Portfolio",x=0.5,y=0.5,showarrow=False,
                                  font=dict(family="Inter",size=11,color="#64748b"))])
            st.plotly_chart(fp, use_container_width=True)
    else:
        st.info("No positions yet — add tickers above to start tracking.")

# ══════════════════════════════════════════════════════════
#  TAB 4 — NEWS
# ══════════════════════════════════════════════════════════
with t4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card" style="margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:20px;">📰</span>
        <p style="font-weight:700;font-size:1rem;color:#0f172a;margin:0;">
          Live News — {name}
        </p>
        <span class="live-dot" style="margin-left:4px;"></span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if news:
        for i,item in enumerate(news[:12]):
            try:
                title     = (item.get("content",{}).get("title") or item.get("title","No title"))
                pub       = (item.get("content",{}).get("pubDate") or item.get("providerPublishTime",""))
                publisher = (item.get("content",{}).get("provider",{}).get("displayName","") or item.get("publisher",""))
                url_link  = (item.get("content",{}).get("canonicalUrl",{}).get("url","#") or item.get("link","#"))
                if isinstance(pub,int):
                    pub = datetime.fromtimestamp(pub).strftime("%d %b %Y %H:%M")
                accent = "#1a56db" if i<3 else "#e2e8f0"
                delay  = i*0.04
                st.markdown(f"""
                <div style="background:white;border:1px solid #e2e8f0;border-left:3px solid {accent};
                     border-radius:10px;padding:12px 16px;margin-bottom:7px;
                     transition:box-shadow 0.15s;animation:fadeUp 0.4s ease {delay}s both;">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                    <div style="flex:1;">
                      <p style="font-size:0.88rem;font-weight:600;color:#0f172a;
                          margin:0 0 5px;line-height:1.5;">{title}</p>
                      <div style="display:flex;gap:8px;align-items:center;">
                        <span style="background:#eff6ff;color:#1a56db;font-size:0.65rem;
                             font-weight:700;padding:2px 8px;border-radius:6px;">{publisher}</span>
                        <span style="color:#94a3b8;font-size:0.68rem;">{pub}</span>
                      </div>
                    </div>
                    <a href="{url_link}" target="_blank"
                       style="font-size:0.7rem;color:#1a56db;font-weight:600;
                              text-decoration:none;white-space:nowrap;
                              border:1px solid #bfdbfe;border-radius:6px;
                              padding:4px 10px;background:#eff6ff;">Read →</a>
                  </div>
                </div>""", unsafe_allow_html=True)
            except: pass
    else:
        st.info(f"No recent headlines found for {ticker}.")

# ══════════════════════════════════════════════════════════
#  TAB 5 — PEERS
# ══════════════════════════════════════════════════════════
with t5:
    st.markdown("<br>", unsafe_allow_html=True)
    default = f"{ticker},TCS.NS,INFY.NS" if ".NS" in ticker else f"{ticker},MSFT,GOOGL"
    peer_in = st.text_input("Enter peer tickers (comma separated)", value=default)

    if st.button("⚖️  Compare Peers"):
        peers     = [p.strip().upper() for p in peer_in.split(",") if p.strip()]
        peer_data = []
        for sym in peers:
            try:
                inf = yf.Ticker(sym).info
                peer_data.append({
                    "Ticker":    sym,
                    "Name":      (inf.get("longName","") or sym)[:20],
                    "Price":     f"₹{inf.get('currentPrice',0):,.2f}",
                    "P/E":       round(inf.get("trailingPE",0) or 0,1),
                    "Fwd P/E":   round(inf.get("forwardPE",0) or 0,1),
                    "P/B":       round(inf.get("priceToBook",0) or 0,2),
                    "EV/EBITDA": round(inf.get("enterpriseToEbitda",0) or 0,1),
                    "ROE %":     round((inf.get("returnOnEquity",0) or 0)*100,1),
                    "Margin %":  round((inf.get("profitMargins",0) or 0)*100,1),
                    "D/E":       round(inf.get("debtToEquity",0) or 0,2),
                })
            except: pass

        if peer_data:
            df_p = pd.DataFrame(peer_data)
            st.markdown('<p class="section-label">Comparative Metrics</p>', unsafe_allow_html=True)
            st.dataframe(df_p, use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)

            clrs = ["#1a56db" if t==ticker else "#bfdbfe" for t in df_p["Ticker"]]
            b1,b2 = st.columns(2)
            with b1:
                st.markdown('<p class="section-label">P/E Ratio Comparison</p>', unsafe_allow_html=True)
                fb = go.Figure(go.Bar(x=df_p["Ticker"],y=df_p["P/E"],
                    marker=dict(color=clrs,line=dict(color="white",width=1)),
                    text=df_p["P/E"],textposition="outside",
                    textfont=dict(family="Inter",size=9,color="#64748b")))
                fb.update_layout(paper_bgcolor="white",plot_bgcolor="#f8fafc",height=220,
                    margin=dict(l=0,r=0,t=8,b=0),showlegend=False,
                    font=dict(family="Inter",color="#64748b",size=9),
                    xaxis=dict(gridcolor="#e2e8f0",linecolor="#e2e8f0"),
                    yaxis=dict(gridcolor="#e2e8f0",linecolor="#e2e8f0"))
                st.plotly_chart(fb, use_container_width=True)
            with b2:
                st.markdown('<p class="section-label">ROE % Comparison</p>', unsafe_allow_html=True)
                fb2 = go.Figure(go.Bar(x=df_p["Ticker"],y=df_p["ROE %"],
                    marker=dict(color=clrs,line=dict(color="white",width=1)),
                    text=df_p["ROE %"],textposition="outside",
                    textfont=dict(family="Inter",size=9,color="#64748b")))
                fb2.update_layout(paper_bgcolor="white",plot_bgcolor="#f8fafc",height=220,
                    margin=dict(l=0,r=0,t=8,b=0),showlegend=False,
                    font=dict(family="Inter",color="#64748b",size=9),
                    xaxis=dict(gridcolor="#e2e8f0",linecolor="#e2e8f0"),
                    yaxis=dict(gridcolor="#e2e8f0",linecolor="#e2e8f0"))
                st.plotly_chart(fb2, use_container_width=True)

            # Radar
            st.markdown('<p class="section-label">Multi-Metric Radar</p>', unsafe_allow_html=True)
            rm = ["P/E","ROE %","Margin %","P/B","EV/EBITDA"]
            rc = ["#1a56db","#3b82f6","#60a5fa","#93c5fd"]
            fig_r = go.Figure()
            for idx,row_d in df_p.iterrows():
                vals = [row_d[m] for m in rm]+[row_d[rm[0]]]
                fig_r.add_trace(go.Scatterpolar(
                    r=vals,theta=rm+[rm[0]],fill="toself",
                    name=row_d["Ticker"],
                    line=dict(color=rc[idx%len(rc)],width=2),
                    fillcolor=rc[idx%len(rc)],opacity=0.12))
            fig_r.update_layout(
                paper_bgcolor="white",plot_bgcolor="white",height=300,
                margin=dict(l=30,r=30,t=20,b=20),
                polar=dict(bgcolor="#f8fafc",
                           radialaxis=dict(visible=True,gridcolor="#e2e8f0",
                                          tickfont=dict(size=8,color="#94a3b8")),
                           angularaxis=dict(gridcolor="#e2e8f0",
                                           tickfont=dict(size=9,color="#64748b"))),
                legend=dict(bgcolor="white",bordercolor="#e2e8f0",font=dict(size=9)),
                font=dict(family="Inter",color="#64748b"))
            st.plotly_chart(fig_r, use_container_width=True)

# ══════════════════════════════════════════════════════════
#  TAB 6 — AI ANALYST
# ══════════════════════════════════════════════════════════
with t6:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a56db,#1648c0);border-radius:16px;
         padding:24px 28px;margin-bottom:20px;animation:fadeUp 0.4s ease both;">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="width:46px;height:46px;background:rgba(255,255,255,0.15);
             border-radius:14px;display:flex;align-items:center;justify-content:center;
             font-size:24px;animation:floatAni 3s ease-in-out infinite;">🤖</div>
        <div>
          <p style="font-family:'Playfair Display',serif;font-weight:700;
              font-size:1.1rem;color:white;margin:0;">Quantivo AI Analyst</p>
          <p style="font-size:0.72rem;color:rgba(255,255,255,0.65);margin:0;letter-spacing:0.5px;">
            Powered by Google Gemini 2.5 Flash
          </p>
        </div>
        <span style="margin-left:auto;background:rgba(255,255,255,0.15);color:white;
             font-size:0.68rem;font-weight:700;padding:4px 12px;border-radius:20px;">
          Goldman Sachs-style Research
        </span>
      </div>
      <p style="color:rgba(255,255,255,0.75);font-size:0.85rem;margin:0;line-height:1.7;">
        Generates a high-conviction equity research note with business overview,
        valuation assessment, catalysts, key risks and a 12-month price target
        — from live financial data for <b style="color:white;">{ticker}</b>.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"🤖  Generate Research Note — {ticker}"):
        with st.spinner("Gemini is analysing fundamentals and writing your report..."):
            report, error = run_ai_report(ticker, info)

        if report:
            formatted = re.sub(r'\*\*(.*?)\*\*',
                r'<span style="color:#0f172a;font-weight:700;">\1</span>', report)
            formatted = formatted.replace("\n","<br>")

            st.markdown(f"""
            <div class="card" style="margin-top:4px;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;flex-wrap:wrap;">
                <span style="background:#eff6ff;color:#1a56db;border:1px solid #bfdbfe;
                     font-size:0.65rem;font-weight:700;padding:3px 10px;
                     border-radius:20px;">✨ AI GENERATED</span>
                <span style="background:#f0fdf4;color:#059669;border:1px solid #bbf7d0;
                     font-size:0.65rem;font-weight:700;padding:3px 10px;
                     border-radius:20px;">Gemini 2.5 Flash</span>
                <span style="color:#94a3b8;font-size:0.72rem;">
                  {name} · {ticker} · {datetime.now().strftime('%d %b %Y')}
                </span>
              </div>
              <div style="height:1px;background:linear-gradient(90deg,#bfdbfe,transparent);
                   margin-bottom:16px;"></div>
              <div style="color:#334155;line-height:2;font-size:0.9rem;">{formatted}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label     = "⬇ Download Research Note (.txt)",
                data      = report,
                file_name = f"{ticker}_quantivo_{datetime.now().strftime('%Y%m%d')}.txt",
                mime      = "text/plain"
            )
        else:
            st.error(f"Report generation failed: {error}")
            st.markdown(f"""
            <div class="card">
              <p style="font-weight:700;color:#0f172a;margin:0 0 10px;">🔧 Fix Steps</p>
              <p style="color:#64748b;font-size:0.85rem;margin:4px 0;">
                1. Open <code>.env</code> in your project root folder</p>
              <p style="color:#64748b;font-size:0.85rem;margin:4px 0;">
                2. It must contain exactly:<br>
                <code style="background:#f1f5f9;padding:2px 8px;border-radius:4px;color:#1a56db;">
                GEMINI_API_KEY=your_key_here</code></p>
              <p style="color:#64748b;font-size:0.85rem;margin:4px 0;">
                3. No spaces, no quotes around the key</p>
              <p style="color:#64748b;font-size:0.85rem;margin:4px 0;">
                4. Restart: <code style="background:#f1f5f9;padding:2px 8px;border-radius:4px;">
                streamlit run dashboard/app.py</code></p>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:8px 0 4px;">
  <p style="font-family:'Playfair Display',serif;font-size:0.9rem;color:#0f172a;
      margin:0 0 4px;font-weight:600;">Quantivo Research Platform</p>
  <p style="color:#94a3b8;font-size:0.7rem;margin:0;">
    Built with Python · Streamlit · Plotly · Gemini AI ·
    For educational purposes only · Not financial advice
  </p>
</div>
""", unsafe_allow_html=True)