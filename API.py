import json
import redis
import requests
import matplotlib.pyplot as plt
import time

from threading import Thread
from flask import Flask, request, jsonify

##mamaa stocks
mamaa = ['AAPL','AMZN','FB','GOOG','MSFT','NFLX','TSLA']

redis_client = redis.Redis()

app = Flask(__name__)

@app.route('/stock_data', methods=['GET'])
def get_stock_data():
    stock_data = []
    for symbol in mamaa:
        stock_data = stock_data.append(redis_client.get(symbol))

    if stock_data is None:
        return jsonify({'message': 'Error'}), 404

    return jsonify(json.loads(stock_data))

def fetch_stock_data():
    stockSymbols = faang
    for symbol in stockSymbols:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        response = requests.get(url)
        data = response.json()

        stock_data = data["chart"]["result"][0]["indicators"]["quote"][0]
        redis_client.set(symbol, json.dumps(stock_data))

def update_stock_data():
    while True:
        fetch_stock_data()
        time.sleep(60)

if __name__ == '__main__':
    update_thread = Thread(target=update_stock_data)
    update_thread.start()
    app.run()
    

