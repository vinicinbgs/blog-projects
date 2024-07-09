import json
import sys
import requests
from flask import Flask, request
from flask_cors import CORS
from prometheus_client import start_http_server, Counter
from loggingz import Logger
from loggingz.trace_id import TraceId

app = Flask(__name__)
CORS(app)
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
MS_NAME = 'ms-one'

@app.route('/')
@app.route('/health')
def healthcheck():
    REQUEST_COUNT.inc()
    do_something()
    
    res = {
        "message": f"Hello from {MS_NAME}!"
    }
    
    Logger().info('app.py', {
        "response": res, 
        "status": "200", 
        "method": "GET", 
        "path": request.path, 
        "app": MS_NAME
    })
    
    return res

def do_something():
    numbers = (1, 2, 3, 4, 5)
    total = sum(numbers, 20)
    
    Logger().info('app.py', {"total": total, "numbers": numbers})

@app.route('/call-ms-two')
def call_ms_two():
    ms_two_endpoint = 'http://ms-two:9999/'
    
    Logger().info('app.py', {"method": "GET", "path": "/call-ms-two", "app": MS_NAME})
    
    response = requests.get(ms_two_endpoint, headers={'trace_id': TraceId().get_id()})
    
    Logger().info('app.py', {"response": response.text, "status": 200, "method": "GET", "path": ms_two_endpoint, "app": MS_NAME})
    
    return response.text

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=9999)
