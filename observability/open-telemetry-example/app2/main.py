from flask import Flask
from flask_cors import CORS
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Configure tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Configure Flask
app = Flask(__name__)
CORS(app)
FlaskInstrumentor().instrument_app(app)

@app.route('/customers')
def index():
    tracer = trace.get_tracer("list-customers-tracer")
    
    with tracer.start_as_current_span("list-customers-return-span"):
        return {"customers": [{"name": "Alice"}, {"name": "Bob"}]}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
