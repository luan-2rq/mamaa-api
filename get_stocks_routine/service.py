import json
import logging
import redis
import yfinance as yf
import pandas as pd

from datetime import datetime
from ..config import config

faang = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']

redis_configs: dict = config.get('redis')

redis_client = redis.Redis(
    redis_configs.get('host'),
    redis_configs.get('port')
)


def fetch_stock_data():
    stocks_data = {"count": 5}
    stocks_list = []
    totalVolume = 0
    totalMarketCap = 0

    graphData = yf.download(faang, period='1d', interval='1m')
    formattedGraphData = []
    for index, row in graphData.iterrows():
        formatted_row = {
            #transforme o tempo em horario de brasilia
            "x": (index - pd.Timedelta(hours=-1)).strftime("%H:%M:%S"),
            "AAPL": row["Adj Close"]["AAPL"],
            "AMZN": row["Adj Close"]["AMZN"],
            "GOOGL": row["Adj Close"]["GOOGL"],
            "META": row["Adj Close"]["META"],
            "NFLX": row["Adj Close"]["NFLX"]
        }
        formattedGraphData.append(formatted_row)
    
    for symbol in faang:
        stock_data = yf.Ticker(symbol)
        cur_stock_info = {}
        #save dividend data to a variable
        cur_stock_info["assetName"] = stock_data.info["longName"]
        cur_stock_info["marketCap"] = stock_data.info["marketCap"]	
        cur_stock_info["volume"] = stock_data.info["volume"]
        cur_stock_info["currentPrice"] = stock_data.info.get("regularMarketPrice") if stock_data.info.get("regularMarketPrice") else stock_data.info.get("previousClose")
        cur_stock_info["openPrice"] = stock_data.info["open"]
        cur_stock_info["closePrice"] = stock_data.info["previousClose"]
        totalVolume += stock_data.info["volume"]
        totalMarketCap += stock_data.info["marketCap"]
        stocks_list.append(cur_stock_info)
    stocks_data["results"] = stocks_list
    #adicione o tempo ao graphData
    stocks_data["graphData"] = json.dumps(formattedGraphData)
    stocks_data["totalVolume"] = totalVolume
    stocks_data["totalMarketCap"] = totalMarketCap
    redis_client.set("faang", json.dumps(stocks_data))