import os
import logging
from flask import Flask
from flask_cors import CORS
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configure tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Initialize logging
logger = logging.getLogger(__name__)

# Instrument logging
LoggingInstrumentor(logging_format='%(msg)s [span_id=%(span_id)s]', log_level=logging.DEBUG, set_logging_format=True).instrument()

# Configure Flask
app = Flask(__name__)
CORS(app)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

MS_TWO_URL = os.getenv("MS_TWO_URL", "http://app2:9999")

@app.route('/')
def index():
    tracer = trace.get_tracer("index-tracer")
    
    with tracer.start_as_current_span("access-ms-two-span"):
        current_span = trace.get_current_span()
        current_span.add_event("access-ms-two-span-1", {"url": MS_TWO_URL})
        current_span.add_event("access-ms-two-span-2", {"url": MS_TWO_URL})
        logger.error("This is a log message")
        
        response = requests.get(MS_TWO_URL + "/customers")
        return f"Hello from app1! Response from app2: {response.text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
