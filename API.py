import json
import redis
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os
import yfinance as yf

from rq import Queue
from rq.job import Job

from dotenv import load_dotenv
from threading import Thread
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from postgres_repository import PostgresRepository

load_dotenv()

##mamaa stocks
mamaa = ['AAPL','AMZN','FB','GOOG','MSFT','NFLX','TSLA']

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))
q = Queue(connection=redis_client)

app = Flask(__name__)

@app.route('/stock_data/<stock>', methods=['GET'])
def get_stock_data(stock):
    if stock is None:
        return jsonify({'message': 'stock not supplied'}), 404
    
    stock_data_cached = redis_client.get("stock_data:" + stock.upper())

    if stock_data_cached is not None:
        return jsonify(json.loads(stock_data_cached)), 200
    
    stock_data = fetch_stock_data(stock=stock.upper())
    if stock_data is None:
        return jsonify({'message': 'stock not found'}), 404
    
    return jsonify(stock_data), 200

@app.route('/all_stock_data', methods=['GET'])
def get_all_stock_data():
    try:
        keys = redis_client.keys("stock_data:*")
        stock_data = []
        for key in keys:
            stock_data.append(json.loads(redis_client.get(key)))

        return jsonify(stock_data), 200
    except:
        return jsonify({'message': 'error fetching stock data'}), 500

@app.route('/refresh_stock_data', methods=['GET'])
def refresh_stock_data():
    fetch_stock_list()
    return jsonify({'message': 'stock data refreshed'}), 200


def fetch_stock_data(stock = 'AMZN'):
    try:
        stock_ticker = yf.Ticker(stock)
        stock_data = stock_ticker.info
        redis_client.set("stock_data:" + stock, json.dumps(stock_data), ex=int(os.getenv('REDIS_EXPIRY', 60)))
        data = {
            'name': stock_data['symbol'],
            'price': stock_data['currentPrice'],
            'timestamp': datetime.utcnow()
        }
        job = q.enqueue_call(func=PostgresRepository.save_stock, args=(data,), result_ttl=500)
    except Exception as e:
        print(e)
        return None
    
    return stock_data

def fetch_stock_list():
    for item in mamaa:
        fetch_stock_data(item)


scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_stock_list, trigger="interval", seconds=int(os.getenv('REFRESH_INTERVAL', 60)))
scheduler.start()