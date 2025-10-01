import os

API_KEY = os.getenv("API_KEY", "secret_api_key")
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./quotes.db")
REQUEST_HEADERS = {
    "User-Agent": "QuotesScraperBot/1.0 (+https://example.com/bot)"
}
REQUEST_TIMEOUT = 10
