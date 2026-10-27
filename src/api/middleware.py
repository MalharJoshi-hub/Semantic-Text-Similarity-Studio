"""API middleware, security headers, and global exception handlers."""

import time
import logging
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)


def setup_middleware(app: Flask):
    """Register request timing and response header middleware."""
    @app.before_request
    def record_start_time():
        request._start_time = time.perf_counter()

    @app.after_request
    def attach_headers(response):
        if hasattr(request, "_start_time"):
            duration = (time.perf_counter() - request._start_time) * 1000.0
            response.headers["X-Response-Time-Ms"] = f"{duration:.2f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error("Internal Server Error: %s", error, exc_info=True)
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500
