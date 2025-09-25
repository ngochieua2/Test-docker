"""
Custom exceptions that can be used across all microservices
"""
from typing import Optional, Dict, Any


class BaseServiceException(Exception):
    """
    Base exception class for all service-specific exceptions
    """
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(BaseServiceException):
    """
    Raised when input validation fails
    """
    pass


class ResourceNotFoundException(BaseServiceException):
    """
    Raised when a requested resource is not found
    """
    pass


class ResourceAlreadyExistsException(BaseServiceException):
    """
    Raised when trying to create a resource that already exists
    """
    pass


class DatabaseException(BaseServiceException):
    """
    Raised when database operations fail
    """
    pass


class ExternalServiceException(BaseServiceException):
    """
    Raised when external service calls fail
    """
    pass


class AuthenticationException(BaseServiceException):
    """
    Raised when authentication fails
    """
    pass


class AuthorizationException(BaseServiceException):
    """
    Raised when authorization fails
    """
    pass


class RateLimitException(BaseServiceException):
    """
    Raised when rate limits are exceeded
    """
    pass