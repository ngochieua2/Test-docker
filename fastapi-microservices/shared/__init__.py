# Shared modules for FastAPI microservices

"""
Shared components for FastAPI microservices

This package provides reusable components that can be shared across all services:
- Core configuration and response schemas
- Exception handling and custom exceptions  
- Middleware for logging, security, and rate limiting
- Utility functions for common operations
- Authentication and authorization utilities (placeholder)

Usage:
    from shared.core.config import BaseAppSettings
    from shared.exceptions.handlers import register_exception_handlers
    from shared.middleware.logging import RequestLoggingMiddleware
    from shared.utils.datetime_utils import utc_now
"""

# Common imports for easy access
from shared.core.config import BaseAppSettings, BaseHealthResponse
from shared.core.schemas import BaseResponse, ErrorResponse, SuccessResponse, PaginatedResponse
from shared.exceptions.custom import (
    BaseServiceException,
    ValidationException, 
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    DatabaseException,
    AuthenticationException,
    AuthorizationException
)
from shared.exceptions.handlers import register_exception_handlers

__version__ = "1.0.0"
__all__ = [
    # Core
    "BaseAppSettings",
    "BaseHealthResponse", 
    "BaseResponse",
    "ErrorResponse",
    "SuccessResponse", 
    "PaginatedResponse",
    
    # Exceptions
    "BaseServiceException",
    "ValidationException",
    "ResourceNotFoundException", 
    "ResourceAlreadyExistsException",
    "DatabaseException",
    "AuthenticationException",
    "AuthorizationException",
    "register_exception_handlers",
]