"""
Request Tracker Middleware
Adds request ID tracking and performance monitoring
"""
import uuid
import logging
from flask import g, request, Flask
from utils.performance import PerformanceMonitor

logger = logging.getLogger(__name__)


def track_request():
    """Generate and attach request ID to current request"""
    # Generate unique request ID
    request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    g.request_id = request_id

    # Start performance timer
    PerformanceMonitor.start_timer()

    logger.info(
        f"Request started - "
        f"method: {request.method}, "
        f"path: {request.path}, "
        f"request_id: {request_id}, "
        f"remote_addr: {request.remote_addr}"
    )


def add_response_headers(response):
    """
    Add custom headers to response

    Args:
        response: Flask response object

    Returns:
        Modified response with custom headers
    """
    # Add request ID to response headers
    if hasattr(g, 'request_id'):
        response.headers['X-Request-ID'] = g.request_id

    # Add request duration to response headers
    if hasattr(g, 'request_duration_ms'):
        response.headers['X-Response-Time'] = f"{g.request_duration_ms}ms"

    return response


def register_request_tracker(app: Flask):
    """
    Register request tracking middleware with Flask app

    Args:
        app: Flask application instance

    Usage:
        from middleware.request_tracker import register_request_tracker
        register_request_tracker(app)
    """
    @app.before_request
    def before_request():
        """Execute before each request"""
        track_request()

    @app.after_request
    def after_request(response):
        """Execute after each request"""
        # End performance timer
        if hasattr(g, 'start_time'):
            endpoint_name = request.endpoint or 'unknown'
            PerformanceMonitor.end_timer(endpoint_name)

        # Add response headers
        return add_response_headers(response)

    @app.teardown_request
    def teardown_request(exception=None):
        """Execute during request teardown"""
        if exception:
            logger.error(
                f"Request failed - "
                f"exception: {str(exception)}, "
                f"request_id: {getattr(g, 'request_id', 'N/A')}"
            )
