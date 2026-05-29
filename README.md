# 🚀 Nexus Research - Advanced Equity Valuation System v2.0

A full-stack quantitative finance platform with modernized UI, real-time market intelligence, and AI-powered equity analysis.

---

## ✨ What's New in v2.0

### 🎨 **Complete Design Overhaul**
- Modern dark theme with glass morphism effects
- Smooth animations throughout the interface
- Professional gradient backgrounds
- Responsive, eye-catching layouts

### 📰 **Market Intelligence Hub**
- Real-time market news from Bloomberg & CNBC
- News display on home dashboard
- Automatic news sentiment analysis
- No ticker needed for market overview

### 🧭 **Smart Navigation**
- Multi-page system with 4 main sections
- Animated sidebar with quick navigation
- Live market status indicators
- Integrated watchlist management

### 🤖 **Enhanced AI Analysis**
- Goldman Sachs-style research reports
- Comprehensive valuation analysis
- 12-month price targets
- Catalysts and risk assessment

---

## 🎯 Features

### Core Analysis
✅ Live stock data fetching via yfinance  
✅ DCF (Discounted Cash Flow) valuation model  
✅ Financial ratio analysis (P/E, ROE, EV/EBITDA)  
✅ Technical indicators (RSI, MACD, Bollinger Bands)  

### AI & Intelligence
✅ AI-generated analyst reports via Google Gemini  
✅ Market news sentiment analysis  
✅ Automated stock screener with filters  

### Dashboard & Visualization
✅ Modern dark-theme Streamlit interface  
✅ Interactive Plotly charts  
✅ Glass morphism card designs  
✅ Smooth fade-in and slide animations  
✅ Mobile-responsive layouts  

### Markets & Watchlist
✅ Real-time market indices (Nifty, Sensex, etc)  
✅ Personal watchlist with price tracking  
✅ Peer comparison tools  
✅ Portfolio tracking capabilities  

---

## 🛠️ Tech Stack

```
Frontend: Streamlit 1.57+ · Plotly 6.7+
Data: yfinance · pandas 3.0+ · numpy
AI/ML: Google Gemini 2.5 Flash API
Utilities: feedparser (news) · textblob (sentiment)
Language: Python 3.10+
Styling: Custom CSS with glass morphism effects
```

---

## 🚀 Quick Start

### Installation
```bash
# 1. Navigate to project directory
cd "c:\Users\Pooja Devi\Desktop\quant research project"

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create .env file with:
# GEMINI_API_KEY=your_api_key_here
```

### Running the Dashboard
```bash
# Start Streamlit app
python -m streamlit run dashboard/app.py

# Dashboard will open at: http://localhost:8501
```

---

## 📖 Documentation

- **[DASHBOARD_GUIDE.md](./DASHBOARD_GUIDE.md)** — Complete user guide with features, usage, and tips
- **[REDESIGN_SUMMARY.md](./REDESIGN_SUMMARY.md)** — What's new in v2.0, before/after comparison

---

## 🎮 Usage Guide

### 🏠 Home Dashboard
- View live market indices
- Browse real-time market news
- Explore system features
- Check market status

### 📊 Stock Analysis
- Analyze any stock with deep dive metrics
- View candlestick charts with technicals
- Run custom stock screeners
- Read latest news specific to the stock
- Generate AI research reports

### 🔍 Smart Screener
- Filter by P/E ratio
- Filter by ROE percentage
- Filter by Debt-to-Equity ratio
- Filter by profit margins
- Analyze multiple stocks at once

### 👁️ Watchlist
- Add/remove stocks dynamically
- Track real-time prices
- Monitor percentage changes
- Quick sidebar preview

### 🤖 AI Analyst
- Generate professional research notes
- Get valuation insights
- Identify catalysts and risks
- Receive Buy/Hold/Sell verdicts
- View 12-month price targets

---

## 📊 Project Structure

```
quant research project/
├── README.md                          # Main documentation
├── DASHBOARD_GUIDE.md                # Detailed feature guide
├── REDESIGN_SUMMARY.md               # v2.0 changes summary
├── requirements.txt                  # Python dependencies
│
├── dashboard/
│   └── app.py                        # Main Streamlit app (v2.0)
│
├── data/
│   ├── fetch_data.py                 # Data fetching utilities
│   ├── raw/                          # Raw stock data
│   └── processed/                    # Processed data & reports
│
├── models/
│   ├── dcf.py                        # DCF valuation model
│   ├── ratios.py                     # Ratio analysis
│   └── technical.py                  # Technical indicators
│
├── ai/
│   └── analyst.py                    # Gemini AI integration
│
└── streamlit/                        # Streamlit config

```

---

## 🎨 Design Highlights

### Modern Aesthetic
- **Dark Theme**: Professional navy gradient backgrounds
- **Glass Cards**: Frosted glass effects with backdrop blur
- **Smooth Animations**: Fade-in, slide, pulse animations
- **Color System**: Blue accents, green gains, red losses
- **Typography**: Multiple modern fonts for hierarchy

### Interactive Elements
- Hover effects with 3D transforms
- Progress indicators for data loading
- Live animated pulse dots
- Gradient gradient buttons
- Color-coded badges and labels

### Responsive Design
- Desktop-optimized layouts
- Tablet compatibility
- Mobile considerations
- Touch-friendly controls

---

## 📈 Key Metrics Tracked

| Metric | Significance |
|--------|-------------|
| **P/E Ratio** | Valuation benchmark |
| **P/B Ratio** | Book value comparison |
| **ROE** | Profitability & efficiency |
| **D/E Ratio** | Financial leverage |
| **Profit Margin** | Operational efficiency |
| **52W High/Low** | Price volatility |

---

## 🤖 AI Features

### Gemini-Powered Reports
- **Model**: Google Gemini 2.5 Flash
- **Analysis**: Goldman Sachs-style research notes
- **Includes**:
  - Business overview
  - Valuation assessment
  - Financial health check
  - Growth catalysts
  - Risk analysis
  - Price target & verdict

### News Analysis
- Sentiment detection
- Automatic categorization
- Real-time parsing from RSS feeds
- Publisher attribution

---

## ⚙️ Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=your_google_gemini_api_key
```

### Streamlit Settings
Configure `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#0f0f1e"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e0e0e0"

[client]
showErrorDetails = false
```

---

## 🐛 Troubleshooting

### Dashboard won't load
```bash
pip install -r requirements.txt --upgrade
streamlit cache clear
```

### AI reports not generating
- Verify `GEMINI_API_KEY` is set in .env
- Check internet connection
- Ensure API quota is available

### News not displaying
- Check internet connection
- Verify RSS feed URLs are accessible
- Try restarting the application

---

## 📊 Performance Tips

- Use shorter time periods (3-6 months) for faster analysis
- Limit screener to 10-20 stocks for quick results
- Keep sessions open to cache data
- Clear cache regularly for fresh data

---

## 🎓 Learning Resources

Included documentation:
- **Feature Guide**: Complete walkthrough of all features
- **Usage Examples**: Real-world usage scenarios
- **Troubleshooting**: Common issues and solutions
- **Tips & Tricks**: Pro tips for better analysis
- **Best Practices**: Recommended analysis approaches

---

## ⚖️ Disclaimer

**For Educational & Research Purpose Only**

This project is designed for educational analysis and research. It is NOT:
- Financial advice
- Investment recommendation
- Professional analysis
- Trading signal

Always consult with licensed financial advisors before making investment decisions.

---

## 📝 Version History

- **v2.0 (Current)** — Complete redesign with modern UI, news integration, multi-page navigation
- **v1.0** — Original single-page dashboard with basic analysis tools

---

## 🤝 Contributing

To improve Nexus Research:
1. Identify areas for enhancement
2. Test thoroughly before changes
3. Document your improvements
4. Ensure backward compatibility

---

## 📞 Support

For issues:
1. Check the [DASHBOARD_GUIDE.md](./DASHBOARD_GUIDE.md) troubleshooting section
2. Verify all dependencies are installed
3. Ensure API keys are correctly configured
4. Review error messages in the terminal

---

**Version**: 2.0 (Complete Redesign)  
**Last Updated**: May 2026  
**Status**: Production Ready ✅  

🚀 **Ready to explore advanced equity valuation? Launch the dashboard now!**