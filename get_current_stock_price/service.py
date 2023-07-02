import logging
import json
import redis
import yfinance as yf

from datetime import datetime
from ..config import config

stock_symbols = ['AAPL']
redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'),
    redis_configs.get('port')
)

def get_current_stock_price():
    stocks_data = []
    for stock in stock_symbols :
        stocks_data.append(redis_client.get(stock))
    logging.info(stocks_data)
    return stocks_data
