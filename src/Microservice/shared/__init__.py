# Shared modules for FastAPI microservices

"""
Shared components for FastAPI microservices

This package provides reusable components that can be shared across all services:
- Database configuration and session management
- Base configuration class for service settings
- Legacy database and todo models (for compatibility)
- Utility functions for logging and datetime operations

Usage:
    from shared.utils import get_logger, setup_logging, utc_now
    from shared.database_legacy import get_db, TodoService
"""

__version__ = "1.0.0"

# Legacy imports for backward compatibility
try:
    from shared.database_legacy import get_db, TodoService
except ImportError:
    # Database legacy components not available
    pass