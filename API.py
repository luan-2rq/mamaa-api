import json
import redis
import requests
import matplotlib.pyplot as plt
import time
import os
import yfinance as yf

from dotenv import load_dotenv
from threading import Thread
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

##mamaa stocks
mamaa = ['AAPL','AMZN','FB','GOOG','MSFT','NFLX','TSLA']

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))

app = Flask(__name__)

@app.route('/stock_data/<stock>', methods=['GET'])
def get_stock_data(stock):
    if stock is None:
        return jsonify({'message': 'stock not supplied'}), 404
    
    stock_data_cached = redis_client.get(stock.upper())

    if stock_data_cached is not None:
        return jsonify(json.loads(stock_data_cached)), 200
    
    stock_data = fetch_stock_data(stock=stock.upper())
    if stock_data is None:
        return jsonify({'message': 'stock not found'}), 404
    
    return jsonify(stock_data), 200



@app.route('/refresh_stock_data', methods=['GET'])
def refresh_stock_data():
    fetch_stock_list()
    return jsonify({'message': 'stock data refreshed'}), 200

def fetch_stock_data(stock = 'AMZN'):
    try:
        stock_ticker = yf.Ticker(stock)
        stock_data = stock_ticker.info
        redis_client.set(stock, json.dumps(stock_data), ex=int(os.getenv('REDIS_EXPIRY', 60)))
    except:
        return None
    
    return stock_data

def fetch_stock_list():
    for item in mamaa:
        fetch_stock_data(item)


scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_stock_list, trigger="interval", seconds=int(os.getenv('REFRESH_INTERVAL', 60)))
scheduler.start()