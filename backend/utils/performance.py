"""
Performance Monitor
Tracks and logs request performance metrics
"""
import time
import logging
from functools import wraps
from typing import Callable
from flask import g, has_request_context

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and log performance metrics"""

    @staticmethod
    def start_timer():
        """Start performance timer for current request"""
        if has_request_context():
            g.start_time = time.time()

    @staticmethod
    def end_timer(endpoint_name: str = None):
        """
        End performance timer and log duration

        Args:
            endpoint_name: Name of the endpoint being monitored
        """
        if has_request_context() and hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            duration_ms = round(duration * 1000, 2)

            # Log performance
            logger.info(
                f"Request completed - "
                f"endpoint: {endpoint_name or 'unknown'}, "
                f"duration: {duration_ms}ms, "
                f"request_id: {getattr(g, 'request_id', 'N/A')}"
            )

            # Store for response headers
            g.request_duration_ms = duration_ms

    @staticmethod
    def get_duration() -> float:
        """Get current request duration in milliseconds"""
        if has_request_context() and hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            return round(duration * 1000, 2)
        return 0.0


def performance_monitor(endpoint_name: str = None) -> Callable:
    """
    Decorator to monitor function performance

    Args:
        endpoint_name: Name of the endpoint for logging

    Returns:
        Decorated function with performance monitoring

    Usage:
        @performance_monitor('get_suburb_data')
        def get_suburb(suburb_id):
            # Your function logic
            return data
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = endpoint_name or func.__name__
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                duration_ms = round(duration * 1000, 2)

                logger.debug(
                    f"Function '{name}' executed in {duration_ms}ms"
                )

        return wrapper
    return decorator
