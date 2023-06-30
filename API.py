import json
import redis
import matplotlib.pyplot as plt
import time
import yfinance as yf

from config import config
from threading import Thread
from flask import Flask, jsonify

##mamaa stocks
stock_symbols = 'AAPL AMZN FB GOOG MSFT NFLX TSLA'
tickers = yf.Tickers(stock_symbols)
redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'), 
    redis_configs.get('port'),
    redis_configs.get('name'),
    redis_configs.get('password')
)

app = Flask(__name__)

@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    stock_data = []
    for symbol in tickers:
        stock_data = stock_data.append(redis_client.get(symbol))

    if stock_data is None:
        return jsonify({'message': 'Error'}), 404

    return jsonify(json.loads(stock_data))

def fetch_stock_data():
    for symbol in stock_symbols.split(' '):
        # url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        response = tickers.tickers.get(symbol).info
        print(response)

        data = response.json()

        stock_data = data["chart"]["result"][0]["indicators"]["quote"][0]
        redis_client.set(symbol, json.dumps(stock_data))

def update_stock_data():
    sleep_interval: int = 60

    while True:
        fetch_stock_data()
        time.sleep(sleep_interval)

if __name__ == '__main__':
    update_thread = Thread(target=update_stock_data)
    update_thread.start()
    app.run(config.get('host'), port=config.get('port'), debug=True)
    