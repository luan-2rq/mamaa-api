import os

import redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv

load_dotenv()

listen = ['default']

conn = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()