"""
Data access layer for the application.

This module provides repositories for database operations
and a connection manager for database access.
"""
from __future__ import annotations

from src.data_access.repository_factory import RepositoryFactory
from src.data_access.utils.db_connection_manager import db_manager


__all__ = [
    'RepositoryFactory',
    'db_manager',
]