# Pocket Option Trading Bot

Advanced automated trading bot for Pocket Option with technical analysis, chart pattern recognition, and Telegram alerts.

## Features

✨ **Core Features:**
- Live 1-minute chart data analysis
- Multiple technical indicators (RSI, MACD, Bollinger Bands, Stochastic, CCI, Williams %R)
- Chart pattern recognition (Head & Shoulders, Double Top/Bottom, Triangles, Flags, Wedges)
- Majority signal confirmation (80%+ confidence required)
- Automated Telegram alerts with live charts
- Support/Resistance level detection
- Demo and Live trading modes

## Indicators Used

📊 **Technical Indicators:**
1. **RSI (14)** - Overbought/Oversold detection
2. **MACD** - Trend and momentum
3. **Bollinger Bands** - Volatility and price extremes
4. **Stochastic** - Momentum and reversals
5. **CCI** - Cyclic price movements
6. **Williams %R** - Oversold/Overbought levels
7. **ATR** - Volatility measurement

## Chart Patterns

📈 **Patterns Detected:**
- Head and Shoulders (Reversal)
- Double Top (Reversal)
- Double Bottom (Reversal)
- Ascending Triangle (Bullish)
- Descending Triangle (Bearish)
- Flag Pattern (Continuation)
- Rising Wedge (Bearish)
- Falling Wedge (Bullish)

## Installation

### Requirements
- Python 3.8+
- Chrome/Chromium browser

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/ripade7714/-pocket-option-trading-bot.git
cd pocket-option-trading-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
```

4. **Edit `.env` file with your settings:**
```
POCKET_OPTION_EMAIL=your_email@example.com
POCKET_OPTION_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
TRADE_MODE=demo  # or 'live'
MIN_CONFIDENCE=80
TRADING_ASSETS=AUDCAD,EURUSD,GBPUSD,USDCAD,GOLD,BITCOIN
```

## Getting Telegram Credentials

### Create Telegram Bot:
1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow instructions and copy the **Bot Token**
4. Paste it in `.env` as `TELEGRAM_BOT_TOKEN`

### Get Your Chat ID:
1. Message your bot
2. Go to: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Copy the `chat.id` value
4. Paste it in `.env` as `TELEGRAM_CHAT_ID`

## Usage

### Run Bot (Continuous Mode)
```bash
python trading_bot_engine.py
```

### Run Single Analysis Cycle
```bash
python -c "from trading_bot_engine import TradingBotEngine; bot = TradingBotEngine(); bot.run_single_cycle()"
```

### Test Single Asset
```bash
python -c "from trading_bot_engine import TradingBotEngine; bot = TradingBotEngine(); bot.analyze_asset('AUDCAD')"
```

## Signal System

### How Signals Are Generated:

1. **Data Collection** → Fetch 1-minute OHLC data
2. **Indicator Analysis** → Calculate 7 technical indicators
3. **Pattern Recognition** → Detect chart patterns
4. **Majority Voting** → All indicators must agree (80%+ confidence)
5. **Signal Generation** → Send BUY/SELL only when conditions met
6. **Telegram Alert** → Send signal with chart to Telegram

### Confidence Levels:
- ✅ **80-100%**: High confidence - Trade signal sent
- ⚠️ **60-79%**: Medium confidence - No signal (wait for higher)
- ❌ **Below 60%**: Low confidence - No trade

## Configuration

Edit `config.py` to customize:

```python
# Trading Assets
TRADING_ASSETS = ['AUDCAD', 'EURUSD', 'GBPUSD', 'USDCAD']

# Minimum confidence required (default: 80%)
MIN_CONFIDENCE = 80

# 1-minute expiry
EXPIRY_TIME = 60

# Look back periods for analysis
LOOKBACK_PERIODS = 100

# Indicator periods
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
BB_PERIOD = 20
STOCH_K = 14
```

## File Structure

```
pocket-option-trading-bot/
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── config.py                     # Configuration settings
├── logger.py                     # Logging setup
├── data_scraper.py               # Data fetching
├── indicators.py                 # Technical indicators
├── chart_patterns.py             # Pattern recognition
├── chart_visualizer.py           # Chart generation
├── signal_analyzer.py            # Signal analysis engine
├── telegram_bot.py               # Telegram integration
├── trading_bot_engine.py         # Main bot engine
├── charts/                       # Generated chart images
├── logs/                         # Bot logs
└── README.md                     # This file
```

## Logs

Bot logs are saved to `logs/trading_bot.log` and also printed to console.

Check logs with:
```bash
tail -f logs/trading_bot.log
```

## Risk Disclaimer

⚠️ **IMPORTANT:**
- This bot is for educational purposes only
- Binary options trading is high-risk
- Past performance does NOT guarantee future results
- Always use DEMO mode first
- Only trade with money you can afford to lose
- Bot signals are NOT guaranteed to be profitable
- Use at your own risk - author assumes no responsibility

## Trading Tips

1. ✅ **Test in Demo First** - Always test signals before live trading
2. ✅ **Start Small** - Begin with minimum position sizes
3. ✅ **Monitor Regularly** - Check bot logs and signals
4. ✅ **Use Stop Loss** - Always set a maximum loss limit
5. ✅ **Don't Overtrade** - Wait for high-confidence signals only
6. ✅ **Track Performance** - Maintain a trading journal

## Troubleshooting

### Bot not sending signals?
- Check confidence is ≥80%
- Verify Telegram token and chat ID
- Check logs: `tail -f logs/trading_bot.log`

### Chrome driver issues?
- Install latest Chrome browser
- Bot auto-downloads correct driver

### No data for asset?
- Verify asset name is correct (e.g., AUDCAD, not AUD/CAD)
- Check internet connection
- Try again in next cycle

## Support & Issues

For bugs or questions:
1. Check the logs first
2. Review configuration in `.env`
3. Ensure all dependencies installed: `pip install -r requirements.txt`

## License

MIT License - See LICENSE file

---

**Remember: Trade responsibly and always use proper risk management!** 🚀
