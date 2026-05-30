# 📈 Quantivo — AI-Powered Equity Research Platform

> Built from scratch by a BTech 2nd Year student passionate about Quantitative Finance

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-app.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

## 🎯 What Is This?

**Quantivo** is a professional-grade stock research and valuation platform that replicates the analytical workflow used by equity analysts at top investment banks — built entirely from scratch in Python.

It combines three things that make it unique:

- ✅ **Investment-bank-grade valuation models** (DCF, comparable analysis)
- ✅ **Quantitative technical analysis** (RSI, MACD, Bollinger Bands)
- ✅ **Generative AI** that writes Goldman Sachs-style research reports from live data

---

## 🚀 Live Demo

🔗 **[Open Quantivo →](https://your-app.streamlit.app)**

Enter any stock ticker (e.g. `RELIANCE.NS`, `TCS.NS`, `AAPL`) and get a full research report in seconds.

---

## ✨ Features

| Feature | What it does |
|---|---|
| 💹 **DCF Valuation** | Projects free cash flows, calculates WACC & terminal value to find intrinsic stock price |
| 📐 **Ratio Analysis** | P/E, EV/EBITDA, ROE, Debt/Equity — live data from Yahoo Finance |
| 📡 **Technical Signals** | RSI, MACD, Bollinger Bands, Golden Cross / Death Cross detection |
| 🤖 **AI Analyst Reports** | Gemini 2.5 Flash writes Goldman Sachs-style research notes with price targets |
| 🔍 **Smart Screener** | Filter any stock universe by fundamentals with AI commentary on results |
| 💼 **Portfolio Tracker** | Add positions, track live P&L, allocation pie chart, total return |
| 📰 **News Feed** | Real-time headlines with publisher info and direct article links |
| ⚖️ **Peer Comparison** | Side-by-side metrics table, bar charts and multi-metric radar chart |

---

## 🖥️ Screenshots

> Enter any ticker → instant full analysis

```
📊 Candlestick chart  +  Volume  +  MA overlays  (Dark TradingView-style)
💹 DCF Fair Value     +  Upside/Downside potential
📐 8 financial ratios live
📡 RSI + MACD charts
🤖 AI research note written by Gemini
```

---

## 🛠️ Tech Stack

```
Language      →  Python 3.11
Dashboard     →  Streamlit
Charts        →  Plotly (candlestick, bar, pie, radar)
Data          →  yfinance (Yahoo Finance API — free)
AI            →  Google Gemini 2.5 Flash (google-genai SDK)
Finance       →  pandas, numpy, ta (technical analysis)
Environment   →  python-dotenv
```

---

## ⚙️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/kartikverma-03/Quant-Research-System.git
cd Quant-Research-System
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

### 5. Run the app
```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
Quant-Research-System/
│
├── 📁 data/
│   ├── fetch_data.py          # Pulls live stock data from Yahoo Finance
│   ├── raw/                   # Downloaded price & financial CSVs
│   └── processed/             # AI-generated reports saved here
│
├── 📁 models/
│   ├── dcf.py                 # DCF valuation — WACC, terminal value, fair price
│   ├── ratios.py              # P/E, EV/EBITDA, ROE, Debt/Equity calculator
│   └── technical.py           # RSI, MACD, Bollinger Bands, Moving Averages
│
├── 📁 ai/
│   └── analyst.py             # Gemini AI equity report generator
│
├── 📁 dashboard/
│   └── app.py                 # Full Streamlit web application
│
├── .env                       # ← NOT on GitHub (API key stored here)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 How the DCF Model Works

The DCF (Discounted Cash Flow) model is the primary valuation method used by investment banks:

```
1. Pull latest Free Cash Flow from Yahoo Finance
2. Project FCF for next 5 years at 10% growth rate
3. Discount each year back using WACC (12%)
4. Calculate Terminal Value at 4% perpetuity growth
5. Sum all discounted cash flows
6. Divide by shares outstanding → Fair Value Per Share
7. Compare to market price → Upside / Downside %
```

---

## 🤖 How the AI Report Works

```
1. Pull 10+ financial metrics from Yahoo Finance live
2. Build a structured prompt with all the data
3. Send to Google Gemini 2.5 Flash API
4. Gemini writes a 200-word Goldman Sachs-style research note
5. Report includes: Overview, Valuation, Health, Catalysts, Risks, Verdict + Price Target
6. Displayed in dashboard + downloadable as .txt
```

---

## 📊 Supported Markets

| Market | Format | Example |
|---|---|---|
| NSE India | `SYMBOL.NS` | `RELIANCE.NS` |
| BSE India | `SYMBOL.BO` | `TCS.BO` |
| US Stocks | `SYMBOL` | `AAPL`, `MSFT` |
| Crypto | `SYMBOL-USD` | `BTC-USD` |

---

## 🎓 What I Learned Building This

- How DCF valuation and WACC actually work in practice, not just theory
- How equity analysts structure research reports at investment banks
- Integrating Generative AI into a real financial analysis pipeline
- Building production-quality, multi-feature Python applications
- Git, GitHub, deployment, API key security, virtual environments

---

## 🗺️ Roadmap

- [ ] Deploy on Streamlit Cloud with public URL
- [ ] Add earnings calendar and upcoming results dates
- [ ] Add price alerts via email
- [ ] Rebuild frontend in React.js (Quantivo v2)
- [ ] Add international exchange coverage (LSE, TSE, HKEX)
- [ ] Add user authentication and saved portfolios

---

## 👨‍💻 Author

**Kartik Verma**
BTech Student | Interested in Quantitative Finance & FinTech

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/kartikverma-03)

---

## ⚠️ Disclaimer

This project is built for **educational and portfolio purposes only**.
Nothing in this application constitutes financial advice.
Always consult a qualified financial advisor before making investment decisions.

---

<p align="center">
  Built with ❤️ and Python · Star ⭐ this repo if you found it useful
</p>