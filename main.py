import os

import uvicorn

from dotenv import load_dotenv
from flask import Flask, jsonify, Response
from asgiref.wsgi import WsgiToAsgi
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter


# Load .env if present for env vars
load_dotenv()

# Read values from environment with defaults
APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_TITLE = os.getenv("APP_TITLE", "Devops for Cloud Assignment")

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by_endpoint=True)

# Custom metric for counting /get_info requests
get_info_counter = Counter(
    'get_info_requests_total', 
    'Number of requests to /get_info endpoint'
)


@app.route("/", methods=["GET"])
def index():
    """Return basic information about the application and available endpoints."""
    return jsonify({
        "message": "Welcome to the DevOps Application",
        "author": "Aditya Jambhalikar - 2024MT03611",
        "status": "running",
        "available_endpoints": {
            "/": "Get this information",
            "/get_info": "Get application version and title"
        }
    })

@app.route("/get_info", methods=["GET"]) 
def get_info():
    get_info_counter.inc()
    """Return application info read from environment variables."""
    return jsonify({
        "APP_VERSION": APP_VERSION,
        "APP_TITLE": APP_TITLE
    })
    
    
# Expose an ASGI-compatible app so uvicorn can serve it
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    # Run the ASGI app with uvicorn for local development
    uvicorn.run("main:asgi_app", host="127.0.0.1", port=8000, reload=True)
