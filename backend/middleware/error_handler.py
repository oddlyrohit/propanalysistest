"""
Error Handler Middleware
Provides unified error handling for API routes
"""
import logging
from functools import wraps
from flask import jsonify
from typing import Callable, Tuple, Any

logger = logging.getLogger(__name__)


class ApiError(Exception):
    """Custom API exception with status code and message"""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        """
        Initialize API error

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict:
        """Convert error to dictionary for JSON response"""
        error_dict = {
            'error': self.message,
            'status_code': self.status_code
        }
        if self.details:
            error_dict['details'] = self.details
        return error_dict


def handle_errors(endpoint_name: str = None) -> Callable:
    """
    Decorator for unified error handling in route handlers

    Args:
        endpoint_name: Name of the endpoint for logging (optional)

    Returns:
        Decorated function with error handling

    Usage:
        @app.route('/api/example')
        @handle_errors('example_endpoint')
        def example_route():
            # Your route logic
            return data
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[Any, int]:
            name = endpoint_name or func.__name__

            try:
                result = func(*args, **kwargs)

                # If function returns tuple with status code
                if isinstance(result, tuple):
                    return result

                # Default success response
                return result, 200

            except ApiError as e:
                # Custom API errors
                logger.warning(f"API Error in {name}: {e.message}", extra={
                    'status_code': e.status_code,
                    'details': e.details
                })
                return jsonify(e.to_dict()), e.status_code

            except ValueError as e:
                # Validation errors
                logger.warning(f"Validation error in {name}: {str(e)}")
                return jsonify({
                    'error': 'Invalid request parameters',
                    'message': str(e),
                    'status_code': 400
                }), 400

            except Exception as e:
                # Unexpected errors
                logger.error(f"Unexpected error in {name}: {str(e)}", exc_info=True)
                return jsonify({
                    'error': 'Internal server error',
                    'message': 'An unexpected error occurred',
                    'status_code': 500
                }), 500

        return wrapper
    return decorator


def register_error_handlers(app):
    """
    Register global error handlers for Flask app

    Args:
        app: Flask application instance
    """

    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        """Handle custom API errors"""
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Resource not found',
            'status_code': 404
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 errors"""
        return jsonify({
            'error': 'Method not allowed',
            'status_code': 405
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'status_code': 500
        }), 500
