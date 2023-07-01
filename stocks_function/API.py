import json
import redis
import yfinance as yf

from datetime import datetime
from .config import config

# mamaa stocks
# stock_symbols = 'AAPL AMZN META GOOG MSFT NFLX TSLA'
stock_symbols = 'AAPL'
tickers = yf.Tickers(stock_symbols)
redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'),
    redis_configs.get('port'),
    redis_configs.get('name'),
    redis_configs.get('password')
)

def get_stock_data():
    stock_data = []
    for symbol in tickers:
        stock_data = stock_data.append(redis_client.get(symbol))

    if stock_data is None:
        return {'message': 'Error'}, 404

    return {'data': stock_data}


def fetch_stock_data():
    current_prices_of_stocks = dict()

    for symbol in stock_symbols.split(' '):
        response = tickers.tickers.get(symbol).info

        current_price = response.get('currentPrice')
        current_prices_of_stocks[symbol] = current_price

        redis_client.set(symbol, {
            'price': current_price,
            'datetime': datetime.now()
        })
    return current_prices_of_stocks