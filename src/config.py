import os
from dotenv import load_dotenv

load_dotenv()

# Полониекс API
POLONIEX_API_KEY = os.getenv("POLONIEX_API_KEY")
POLONIEX_API_SECRET = os.getenv("POLONIEX_API_SECRET")
POLONIEX_API_URL = "https://poloniex.com/public"

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")