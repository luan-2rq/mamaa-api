import json
import redis
import yfinance as yf

from datetime import datetime
from ..config import config

# mamaa stocks
# stock_symbols = 'AAPL AMZN META GOOG MSFT NFLX TSLA'
stock_symbols = ['AAPL']

redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'),
    redis_configs.get('port')
)

def fetch_stock_data():
    for symbol in stock_symbols:
        stock_data = yf.Ticker(symbol)
        current_price = stock_data.info["currentPrice"]
        redis_client.set(symbol, json.dumps({"current_price": current_price}))