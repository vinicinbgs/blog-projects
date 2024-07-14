import os
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
    
    Logger().info('Response',  {
        "response": res, 
        "status": "200", 
        "method": "GET", 
        "path": request.path, 
        "app": MS_NAME,
        "file": "app.py"
    })
    
    return res

def do_something():
    numbers = (1, 2, 3, 4, 5)
    total = sum(numbers, 20)
    
    Logger().info('do_something', {
        "total": total, 
        "numbers": numbers,
        "app": MS_NAME,
        "file": "app.py"
    })
    
    filename = 'example.txt'
    content = 'Hello, this is a sample content to be written to the file.'
    
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Content written to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

@app.route('/call-ms-two')
def call_ms_two():
    ms_two_endpoint = os.getenv('MS_TWO_ENDPOINT', 'http://ms-two:9999')
    
    Logger().info('Request', {
        "method": "GET", 
        "path": "/call-ms-two", 
        "app": MS_NAME, 
        "file": "app.py"
    })
    
    response = requests.get(ms_two_endpoint, headers={'trace_id': TraceId().get_id()})
    
    Logger().info('Response', {
        "response": response.text, 
        "status": 200, 
        "method": "GET", 
        "path": ms_two_endpoint, 
        "app": MS_NAME, 
        "file": "app.py"
    })
    
    return response.text

if __name__ == '__main__':
    start_http_server(8000) # Start Prometheus metrics server
    app.run(host='0.0.0.0', port=9999) # Start Flask app
