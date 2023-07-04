import logging
import json
import redis
import yfinance as yf

from datetime import datetime
from ..config import config

stock_symbols = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'),
    redis_configs.get('port')
)

def get_top_10_stocks_data():
    stocks_data = redis_client.get("faang")
    return stocks_data
