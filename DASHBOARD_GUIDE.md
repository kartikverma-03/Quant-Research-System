# 🚀 Nexus Research Valuation System v2.0 - Complete Guide

## Overview
Nexus Research v2.0 is a completely redesigned, modern equity valuation and market intelligence dashboard built with Streamlit. The system features advanced analytics, AI-powered insights, and a sleek dark-theme interface.

---

## ✨ Key Features

### 1. **Modern Design System**
- 🌙 **Dark Theme**: Professional dark background with gradient overlays
- 🎨 **Glass Morphism**: Frosted glass card effects with blur backdrop filters
- ✨ **Smooth Animations**: Fade-in, slide, and pulse animations throughout the interface
- 🎯 **Responsive Layout**: Optimized for desktop viewing with mobile considerations

### 2. **Intelligent Navigation**
- **Sidebar Toggle**: Left sidebar collapses smoothly with animation
- **Quick Navigation**: 4 main sections accessible via icon buttons
  - 🏠 **Home** - Market overview and news dashboard
  - 📊 **Analyze** - Deep stock analysis with AI insights
  - 🔍 **Screener** - Filter stocks by financial metrics
  - 👁️ **Watchlist** - Track your favorite stocks

### 3. **Home Dashboard**
- **Market Overview**: Live indices (Nifty 50, Sensex, USD/INR, Gold, Oil)
- **News Feed**: Real-time market news from Bloomberg & CNBC
- **Feature Showcase**: Visual cards highlighting all system capabilities
- **Live Indicators**: Animated pulse dots showing market status

### 4. **Stock Analysis Page**
Complete analysis tools for any stock:

#### Charts Tab
- Interactive candlestick charts
- Technical analysis with moving averages
- Volume analysis
- Price trends over custom periods

#### Screener Tab
- Filter by P/E ratio
- ROE (Return on Equity) minimum
- Debt-to-Equity ratio
- Profit margin requirements
- Compare multiple stocks simultaneously

#### News Tab
- Real-time news feed specific to the stock
- News categorization and timestamps
- Direct links to full articles
- News sentiment indicators

#### AI Analyst Tab
- **Gemini-Powered Reports**: Uses Google Gemini 2.5 Flash AI
- **Research Notes**: Goldman Sachs-style analysis
- **Valuation Insights**: Detailed P/E, P/B analysis
- **Catalysts & Risks**: Key drivers and downside risks
- **Price Targets**: 12-month price target recommendations
- **Verdict**: Buy/Hold/Sell recommendations

#### Peer Comparison
- Multi-stock radar charts
- Side-by-side metric comparison
- Financial health assessment

### 5. **Watchlist Feature**
- Add/remove stocks instantly
- Real-time price tracking
- Percentage change display
- P/E ratio display for each holding
- Persistent storage via session state

### 6. **Real-Time Market Data**
- Stock prices updated live
- Market indices (NSE, BSE, NYSE, NASDAQ)
- Sector classification
- Market capitalization
- 52-week high/low tracking

---

## 🎮 How to Use

### Getting Started
```bash
# Navigate to project directory
cd "c:\Users\Pooja Devi\Desktop\quant research project"

# Run the dashboard
python -m streamlit run dashboard/app.py
```

### Using the Sidebar
1. **Quick Search Box**: Enter any stock ticker (e.g., RELIANCE.NS, AAPL, GOOGL)
2. **Period Selector**: Choose analysis period (3mo, 6mo, 1y, 2y, 5y)
3. **Navigation Buttons**: Click icons to switch between pages
4. **Watchlist**: See your 5 most-tracked stocks with live prices

### Analyzing a Stock
1. Go to **📊 Analyze** section
2. Enter a ticker in sidebar (or use default)
3. Click "Analyze" button
4. Explore different tabs:
   - View candlestick charts
   - Run screener to find similar stocks
   - Read latest news
   - Generate AI research report

### Screening Stocks
1. Go to **🔍 Screener**
2. Set financial criteria:
   - Max P/E ratio
   - Min ROE percentage
   - Max Debt-to-Equity
   - Min Profit Margin
3. Enter comma-separated tickers
4. Click "Run Screener"
5. View results in formatted table

### Managing Watchlist
1. Go to **👁️ Watchlist**
2. Add ticker: Type ticker and click "Add"
3. View all tracked stocks with live prices and changes
4. Remove stocks: Click "Remove" button

---

## 📊 Key Metrics Explained

| Metric | What It Means | Good Range |
|--------|-------------|-----------|
| **P/E Ratio** | Price-to-Earnings | 15-25 (typically) |
| **P/B Ratio** | Price-to-Book | < 2.0 often value |
| **ROE** | Return on Equity | > 15% is good |
| **D/E Ratio** | Debt-to-Equity | < 1.0 is healthy |
| **Margin** | Profit Margin | > 10% for quality |

---

## 🎨 Design Features

### Colors & Meaning
- 🔵 **Blue** - Primary accent, information
- 🟢 **Green** - Positive movement, gains
- 🔴 **Red** - Negative movement, losses
- 🟡 **Yellow** - Neutral, warning
- 🟣 **Purple** - Sectors, categories

### Animations
- **Fade-In-Up**: Cards appear from bottom with fade
- **Slide-In-Right**: News items slide from right
- **Pulse**: Live indicators pulse to show active status
- **Hover Effects**: Cards lift on mouse hover with shadow enhancement

---

## 🤖 AI Analyst Features

### How AI Reports Work
1. **Data Collection**: Gathers latest financial metrics
2. **Analysis**: Processes with Gemini 2.5 Flash AI
3. **Report Generation**: Creates professional research note
4. **Recommendations**: Provides Buy/Hold/Sell verdict

### What's Included
- Company overview and business summary
- Valuation assessment (cheap/expensive)
- Financial health evaluation
- Growth catalysts (2 key drivers)
- Risk analysis (2 key downside risks)
- 12-month price target
- Investment recommendation

### Using AI Reports
```
1. Select stock in Analysis page
2. Go to "AI Analyst" tab
3. Click "Generate AI Report"
4. Wait for analysis (10-20 seconds)
5. Review professional research note
```

---

## 📰 Market News Integration

### News Sources
- Bloomberg Markets RSS Feed
- CNBC News RSS Feed
- Real-time updates

### News Features
- Automatic categorization
- Sentiment indicators
- Publish timestamps
- Direct article links
- Market relevance filtering

---

## 🛠️ Technical Stack

### Dependencies Added
- **feedparser**: RSS feed parsing for news
- **lxml**: XML/HTML parsing
- **textblob**: Sentiment analysis
- **streamlit**: Web interface
- **plotly**: Interactive charts
- **yfinance**: Stock data API
- **pandas**: Data manipulation
- **Google Gemini**: AI analysis

### Architecture
```
dashboard/
├── app.py              # Main Streamlit app
├── ../models/
│   ├── dcf.py         # DCF valuation
│   ├── ratios.py      # Ratio analysis
│   └── technical.py   # Technical analysis
├── ../data/
│   ├── fetch_data.py  # Data fetching
│   └── processed/     # Cached data
```

---

## 🔧 Configuration

### Environment Variables (.env)
```
GEMINI_API_KEY=your_api_key_here
```

### Streamlit Config
Edit `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#0f0f1e"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e0e0e0"
```

---

## 💡 Tips & Tricks

### Performance Tips
- Use shorter time periods for faster loading (3-6 months)
- Limit screener to 10-20 tickers for quick results
- Cache data by keeping sessions open

### Analysis Tips
- Compare P/E ratios across sectors for context
- Look at 5-year trends, not just recent prices
- Use AI reports as starting point, not final verdict
- Verify news sentiment with multiple sources

### Best Practices
- Always diversify your watchlist across sectors
- Review metrics quarterly for long-term trends
- Use screener to find patterns, not just outliers
- Combine technical and fundamental analysis

---

## 🚀 Quick Start Examples

### Example 1: Analyze a Tech Stock
```
1. Enter "TCS.NS" in sidebar
2. Click "Analyze"
3. View Charts → Check 1-year trend
4. View AI Analyst → Get research note
5. Compare P/E with INFY.NS
```

### Example 2: Find Value Stocks
```
1. Go to Screener
2. Set: P/E < 20, ROE > 20%, D/E < 0.8
3. Add: "RELIANCE.NS,HDFCBANK.NS,INFY.NS"
4. Click Run Screener
5. View filtered results
```

### Example 3: Build Watchlist
```
1. Go to Watchlist
2. Add: "RELIANCE.NS"
3. Add: "TCS.NS"
4. Add: "INFY.NS"
5. Monitor prices in sidebar
```

---

## 📱 Mobile Support

While optimized for desktop, Nexus works on tablets:
- Responsive layouts adapt to screen size
- Touch-friendly buttons and controls
- Readable fonts at all sizes
- Charts scroll horizontally on small screens

---

## ⚠️ Disclaimer

**For Educational & Research Purpose Only**

This dashboard is designed for educational analysis and research. It should NOT be considered:
- Financial advice
- Investment recommendation
- Professional analysis
- Trading signal

Always consult with licensed financial advisors before making investment decisions.

---

## 🔄 Future Enhancements

Planned features for next versions:
- Portfolio backtesting engine
- Options analysis tools
- Dividend tracking
- Technical pattern recognition
- Multi-currency support
- Mobile app version
- Real-time alerts
- Export to PDF reports

---

## 🆘 Troubleshooting

### Issue: Dashboard won't load
**Solution**: Check if all requirements are installed
```bash
pip install -r requirements.txt
```

### Issue: No news displayed
**Solution**: Check internet connection and RSS feed URLs

### Issue: AI reports not generating
**Solution**: Verify GEMINI_API_KEY in .env file

### Issue: Data loading slowly
**Solution**: Use shorter time periods or check internet speed

---

## 📞 Support

For issues or suggestions:
1. Check existing tickets/documentation
2. Verify all dependencies installed
3. Clear Streamlit cache: `streamlit cache clear`
4. Restart the application

---

**Version**: 2.0  
**Last Updated**: May 2026  
**Author**: Nexus Research Team  
**License**: Educational Use Only
