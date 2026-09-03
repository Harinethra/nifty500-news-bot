import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "mixtral-8x7b-32768"

# News API Configuration
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Update Frequency
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY", 30))

# Language Settings
PRIMARY_LANGUAGE = os.getenv("PRIMARY_LANGUAGE", "english")
SECONDARY_LANGUAGE = os.getenv("SECONDARY_LANGUAGE", "tamil")

# Impact Levels to Track
IMPACT_LEVELS = ["HIGH", "MEDIUM"]

# Nifty 500 Top Stocks
MAJOR_STOCKS = [
    "TCS", "INFY", "WIPRO", "HDFC", "ICICIBANK", "HDFC BANK",
    "RELIANCE", "BAJAJ-AUTO", "MARUTI", "SBIN", "AXISBANK",
    "LT", "ITC", "HINDUSTAN UNILEVER", "NESTLEIND", "BRITANNIA"
]

# Nifty 500 Stocks List
NIFTY_500_STOCKS = MAJOR_STOCKS
