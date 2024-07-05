import json
import sys
from flask import Flask
from flask_cors import CORS
from prometheus_client import start_http_server, Counter
from loggingz import Logger

app = Flask(__name__)
CORS(app)
REQUEST_COUNT = Counter('request_count', 'Total number of requests')

# Configure logging
@app.route('/')
def hello():
    REQUEST_COUNT.inc()
    something()
    Logger().info('app.py', {"response": "Hello World!", "status": "200", "method": "GET", "path": "/"})
    return "Hello World!"


def something():
    numbers = (1, 2, 3, 4, 5)
    total = sum(numbers, 20)
    
    Logger().info('app.py', {"total": total, "numbers": numbers})

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=9999)
