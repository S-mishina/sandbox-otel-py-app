# flask sample app

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
import json
import logging

app = Flask(__name__)

@app.route('/')
def index():
    if os.getenv("HTTP_FLG") == "true":
        logging.info("HTTP_FLG is true")
        response = request_api()
        logging.info(response)
    else:
        logging.info("HTTP_FLG is not true")
    return jsonify({'message': 'Hello, World!'})

def request_api():
    url = os.getenv("API_URL","localhost:80")
    logging.info(f"API_URL is set to {url}")
    if "localhost" in url or "127.0.0.1" in url:
        logging.error("API_URL points to the local server itself. Aborting to avoid infinite loop.")
        return {"error": "API_URL is invalid and points to itself"}
    logging.info(f"Making a request to {url}")
    response = requests.get(url)
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8080)
    debug=True


