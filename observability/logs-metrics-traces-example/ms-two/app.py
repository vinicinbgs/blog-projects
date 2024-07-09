import json
import sys
from flask import Flask, request
from flask_cors import CORS
from prometheus_client import start_http_server, Counter
from loggingz import Logger
from loggingz.trace_id import TraceId

app = Flask(__name__)
CORS(app)
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
MS_NAME = 'ms-two'

@app.route('/')
def hello():
    REQUEST_COUNT.inc()
    
    if request.headers.get('trace_id'):
        TraceId.set_id(request.headers.get('trace_id'))
        
    message = f"Hello from {MS_NAME}!"
    Logger().info('app.py', {"status": "200", "method": "GET", "path": "/", "app": MS_NAME})
    
    return message

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=9999)
