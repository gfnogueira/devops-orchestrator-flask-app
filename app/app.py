from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter("flask_http_request_total", "Total HTTP Requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("flask_http_request_duration_seconds", "HTTP Request Duration", ["method", "endpoint"])

@app.before_request
def before_request():
    app.start_time = time.time()

@app.after_request
def after_request(response):
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    if hasattr(app, 'start_time'):
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).observe(time.time() - app.start_time)
    
    return response

@app.route("/")
def hello():
    logger.info("Hello endpoint accessed")
    return jsonify({
        "message": "Hello from Flask DevOps App!",
        "version": "1.0.0",
        "environment": os.getenv("FLASK_ENV", "production")
    })

@app.route("/health")
def health():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {
            "application": "ok",
            "dependencies": "ok"
        }
    }), 200

@app.route("/ready")
def ready():
    """Readiness check endpoint"""
    return jsonify({
        "status": "ready",
        "timestamp": time.time()
    }), 200

@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/api/data")
def get_data():
    """Sample API endpoint with some processing time"""
    time.sleep(0.1)  # Simulate some processing
    return jsonify({
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ],
        "count": 3
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    app.run(host="0.0.0.0", port=port, debug=debug)
