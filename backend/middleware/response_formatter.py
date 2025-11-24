"""
Response Formatter
Provides utilities for standardizing API responses
"""
from flask import jsonify
from typing import Any, Dict, Tuple


def success_response(
    data: Any,
    status_code: int = 200,
    meta: Dict[str, Any] = None
) -> Tuple[Any, int]:
    """
    Create standardized success response

    Args:
        data: Response data
        status_code: HTTP status code (default: 200)
        meta: Optional metadata (pagination, etc.)

    Returns:
        Tuple of (JSON response, status code)

    Usage:
        return success_response({'suburb': suburb_data})
        return success_response(suburbs, meta={'total': 100, 'page': 1})
    """
    response = {
        'success': True,
        'data': data
    }

    if meta:
        response['meta'] = meta

    return jsonify(response), status_code


def error_response(
    message: str,
    status_code: int = 500,
    details: Dict[str, Any] = None
) -> Tuple[Any, int]:
    """
    Create standardized error response

    Args:
        message: Error message
        status_code: HTTP status code (default: 500)
        details: Optional error details

    Returns:
        Tuple of (JSON response, status code)

    Usage:
        return error_response('Suburb not found', 404)
        return error_response('Validation failed', 400, {'field': 'suburb_id'})
    """
    response = {
        'success': False,
        'error': message,
        'status_code': status_code
    }

    if details:
        response['details'] = details

    return jsonify(response), status_code


def paginated_response(
    items: list,
    page: int = 1,
    per_page: int = 10,
    total: int = None
) -> Tuple[Any, int]:
    """
    Create paginated response with metadata

    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items (optional)

    Returns:
        Tuple of (JSON response, status code)

    Usage:
        return paginated_response(
            items=suburbs,
            page=1,
            per_page=10,
            total=len(all_suburbs)
        )
    """
    meta = {
        'page': page,
        'per_page': per_page,
        'count': len(items)
    }

    if total is not None:
        meta['total'] = total
        meta['total_pages'] = (total + per_page - 1) // per_page  # Ceiling division
        meta['has_next'] = page < meta['total_pages']
        meta['has_prev'] = page > 1

    return success_response(items, meta=meta)
