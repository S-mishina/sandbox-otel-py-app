# flask sample app

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
import json
import logging
from joblib import Parallel, delayed
if os.getenv("OTEL_TRACES_EXPORTER"):
  from opentelemetry import trace
  from opentelemetry.instrumentation.flask import FlaskInstrumentor
  from opentelemetry.propagate import set_global_textmap
  from opentelemetry.propagators.b3 import B3MultiFormat
  from opentelemetry.sdk.trace import TracerProvider
else:
  logging.info("OTEL_TRACES_EXPORTER is not set. Tracing will not be enabled.")

app = Flask(__name__)
# FlaskInstrumentor().instrument_app(app)

@app.route('/')
def index():
    logging.info("Request headers")
    logging.info(request.headers)
    if os.getenv("HTTP_FLG") == "true":
        logging.info("HTTP_FLG is true")
        request_count = int(os.getenv("REQUESTCOUNT", 1))
        logging.info(f"Request count is {request_count}")
        try:
            results = Parallel(n_jobs=request_count)(delayed(request_api)() for _ in range(request_count))
            logging.info(f"Parallel results: {results}")
        except Exception as e:
            logging.error(f"Error during parallel requests: {e}")
            pass
    else:
        logging.info("HTTP_FLG is not true")
    return jsonify({'message': 'Hello, World!'})

@app.route('/health')
def health():
    return jsonify({'status': 'UP'})

def request_api():
    url = os.getenv("API_URL","localhost:80")
    logging.info(f"API_URL is set to {url}")
    if "localhost" in url or "127.0.0.1" in url:
        logging.error("API_URL points to the local server itself. Aborting to avoid infinite loop.")
        return {"error": "API_URL is invalid and points to itself"}
    logging.info(f"Making a request to {url}")
    response = requests.get(url)
    logging.info(response)
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0",port=8080, debug=True, use_reloader=False)

