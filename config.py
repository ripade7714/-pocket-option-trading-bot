"""
Configuration settings for Pocket Option Trading Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Pocket Option Credentials
POCKET_OPTION_EMAIL = os.getenv('POCKET_OPTION_EMAIL', '')
POCKET_OPTION_PASSWORD = os.getenv('POCKET_OPTION_PASSWORD', '')

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Trading Configuration
TRADE_MODE = os.getenv('TRADE_MODE', 'demo')  # 'demo' or 'live'
MIN_CONFIDENCE = int(os.getenv('MIN_CONFIDENCE', 80))  # Minimum indicator agreement %
EXPIRY_TIME = int(os.getenv('EXPIRY_TIME', 60))  # 1 minute expiry

# Assets to Trade
TRADING_ASSETS = os.getenv('TRADING_ASSETS', 'AUDCAD,EURUSD,GBPUSD').split(',')

# Chart Settings
CHART_INTERVAL = int(os.getenv('CHART_INTERVAL', 1))  # 1 minute
LOOKBACK_PERIODS = int(os.getenv('LOOKBACK_PERIODS', 100))

# Indicator Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

BB_PERIOD = 20
BB_STD_DEV = 2

STOCH_K = 14
STOCH_D = 3

CCI_PERIOD = 20
WILLIAMS_R_PERIOD = 14

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'trading_bot.log'
