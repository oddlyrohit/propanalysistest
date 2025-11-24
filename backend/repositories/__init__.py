"""
Repositories Package
Data access layer with multiple implementations
"""
from .base import SuburbRepository
from .api_repository import ApiSuburbRepository
from .file_repository import FileSuburbRepository
from .composite_repository import CompositeSuburbRepository

__all__ = [
    'SuburbRepository',
    'ApiSuburbRepository',
    'FileSuburbRepository',
    'CompositeSuburbRepository',
]
