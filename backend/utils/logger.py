"""
Structured Logger
Provides JSON-formatted structured logging with context
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from flask import has_request_context, request, g


class StructuredLogger:
    """Logger with structured JSON output"""

    def __init__(self, name: str):
        """
        Initialize structured logger

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)

    def _get_context(self) -> Dict[str, Any]:
        """Get current request context"""
        context = {}

        if has_request_context():
            # Add request ID if available
            if hasattr(g, 'request_id'):
                context['request_id'] = g.request_id

            # Add request info
            context['method'] = request.method
            context['path'] = request.path
            context['remote_addr'] = request.remote_addr

            # Add user agent if available
            if request.headers.get('User-Agent'):
                context['user_agent'] = request.headers.get('User-Agent')

        return context

    def _format_message(
        self,
        level: str,
        message: str,
        extra: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format log message as JSON

        Args:
            level: Log level
            message: Log message
            extra: Additional context data

        Returns:
            JSON formatted log string
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level,
            'message': message,
            **self._get_context()
        }

        if extra:
            log_data['extra'] = extra

        return json.dumps(log_data)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(self._format_message('DEBUG', message, kwargs))

    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(self._format_message('INFO', message, kwargs))

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(self._format_message('WARNING', message, kwargs))

    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(self._format_message('ERROR', message, kwargs))

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(self._format_message('CRITICAL', message, kwargs))


# Cache for logger instances
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(name: str) -> StructuredLogger:
    """
    Get or create a structured logger instance

    Args:
        name: Logger name

    Returns:
        StructuredLogger instance

    Usage:
        logger = get_logger(__name__)
        logger.info('Processing request', user_id=123)
    """
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name)
    return _loggers[name]
