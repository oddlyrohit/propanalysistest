"""
Request Validators
Provides input validation utilities for API requests
"""
import re
from functools import wraps
from flask import request
from typing import Callable, List, Dict, Any
from .error_handler import ApiError


def validate_suburb_id(suburb_id: str) -> None:
    """
    Validate suburb ID format

    Args:
        suburb_id: Suburb identifier (e.g., "melbourne-3000")

    Raises:
        ValueError: If suburb_id is invalid
    """
    if not suburb_id:
        raise ValueError("Suburb ID is required")

    # Check basic format: lowercase words separated by hyphens, ending with optional postcode
    # Examples: "melbourne", "melbourne-3000", "belmont-north-2280"
    pattern = r'^[a-z]+(-[a-z]+)*(-\d{4})?$'

    if not re.match(pattern, suburb_id):
        raise ValueError(
            f"Invalid suburb ID format: '{suburb_id}'. "
            "Expected format: 'suburb-name' or 'suburb-name-postcode' (e.g., 'melbourne-3000')"
        )


def validate_query_params(
    required: List[str] = None,
    optional: List[str] = None,
    allowed_values: Dict[str, List[str]] = None
) -> Callable:
    """
    Decorator to validate query parameters

    Args:
        required: List of required parameter names
        optional: List of optional parameter names
        allowed_values: Dict mapping parameter names to allowed values

    Returns:
        Decorator function

    Usage:
        @validate_query_params(
            required=['suburb_id'],
            optional=['geojson', 'property_type'],
            allowed_values={
                'geojson': ['true', 'false'],
                'property_type': ['house', 'unit', 'apartment']
            }
        )
        def my_route():
            # Your route logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check required parameters
            if required:
                for param in required:
                    if param not in request.args:
                        raise ApiError(
                            f"Missing required parameter: '{param}'",
                            status_code=400
                        )

            # Check allowed values
            if allowed_values:
                for param, allowed in allowed_values.items():
                    value = request.args.get(param)
                    if value and value not in allowed:
                        raise ApiError(
                            f"Invalid value for '{param}': '{value}'. "
                            f"Allowed values: {', '.join(allowed)}",
                            status_code=400
                        )

            # Check for unexpected parameters
            if required or optional:
                all_allowed = set(required or []) | set(optional or [])
                unexpected = set(request.args.keys()) - all_allowed

                if unexpected:
                    raise ApiError(
                        f"Unexpected parameters: {', '.join(unexpected)}",
                        status_code=400
                    )

            return func(*args, **kwargs)

        return wrapper
    return decorator


def validate_search_query(min_length: int = 1, max_length: int = 100) -> Callable:
    """
    Decorator to validate search query parameter

    Args:
        min_length: Minimum query length
        max_length: Maximum query length

    Returns:
        Decorator function

    Usage:
        @validate_search_query(min_length=2, max_length=50)
        def search_route():
            query = request.args.get('q', '')
            # Your route logic
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            query = request.args.get('q', '')

            if not query:
                raise ApiError(
                    "Search query parameter 'q' is required",
                    status_code=400
                )

            if len(query) < min_length:
                raise ApiError(
                    f"Search query must be at least {min_length} character(s)",
                    status_code=400
                )

            if len(query) > max_length:
                raise ApiError(
                    f"Search query must not exceed {max_length} characters",
                    status_code=400
                )

            return func(*args, **kwargs)

        return wrapper
    return decorator


def validate_boolean_param(param_name: str, default: bool = True) -> bool:
    """
    Validate and parse boolean query parameter

    Args:
        param_name: Name of the parameter
        default: Default value if parameter is missing

    Returns:
        Boolean value

    Raises:
        ValueError: If parameter value is not a valid boolean
    """
    value = request.args.get(param_name)

    if value is None:
        return default

    value_lower = value.lower()

    if value_lower in ['true', '1', 'yes']:
        return True
    elif value_lower in ['false', '0', 'no']:
        return False
    else:
        raise ValueError(
            f"Invalid boolean value for '{param_name}': '{value}'. "
            "Expected: 'true', 'false', '1', '0', 'yes', or 'no'"
        )
