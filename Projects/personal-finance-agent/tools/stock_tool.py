import os
import requests
from langchain.tools import tool

@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol (e.g. AAPL, TSLA)."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    )
    response = requests.get(url)
    data = response.json()

    quote = data.get("Global Quote", {})
    if not quote:
        return f"Error: Could not fetch price for {symbol}"

    price = quote.get("05. price", "N/A")
    change = quote.get("10. change percent", "N/A")

    return f"{symbol}: ${price} ({change} change today)"
