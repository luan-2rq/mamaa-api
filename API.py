import json
import redis
import time
import yfinance as yf

from datetime import datetime
from config import config
from flask import Flask, jsonify
from flask_caching import Cache

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

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = redis_configs.get('host')
app.config['CACHE_REDIS_PORT'] = redis_configs.get('port')
app.config['CACHE_DEFAULT_TIMEOUT'] = 120

cache = Cache()
cache.init_app(app)

@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    stock_data = []
    for symbol in tickers:
        stock_data = stock_data.append(redis_client.get(symbol))

    if stock_data is None:
        return jsonify({'message': 'Error'}), 404

    return jsonify(json.loads(stock_data))


@app.route('/get_stocks', methods=['GET'])
@cache.cached()
def fetch_stock_data():
    current_prices_of_stocks = dict()

    for symbol in stock_symbols.split(' '):
        response = tickers.tickers.get(symbol).info

        current_price = response.get('currentPrice')
        current_prices_of_stocks[symbol] = current_price

        # redis_client.set(symbol, {
        #     'price': current_price,
        #     'datetime': datetime.now()
        # })
    return current_prices_of_stocks


def update_stock_data():
    sleep_interval: int = 60

    while True:
        fetch_stock_data()
        time.sleep(sleep_interval)


if __name__ == '__main__':
    # update_thread = Thread(target=update_stock_data)
    # update_thread.start()
    app.run(config.get('host'), port=config.get('port'), debug=True)
