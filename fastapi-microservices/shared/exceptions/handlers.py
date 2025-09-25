"""
Global exception handlers that can be registered with FastAPI applications
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from shared.exceptions.custom import (
    BaseServiceException,
    ValidationException,
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    DatabaseException,
    AuthenticationException,
    AuthorizationException,
    RateLimitException
)
from shared.core.schemas import ErrorResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def base_service_exception_handler(request: Request, exc: BaseServiceException) -> JSONResponse:
    """
    Handle custom service exceptions
    """
    logger.error(f"Service exception: {exc.error_code} - {exc.message}", extra={"details": exc.details})
    
    status_map = {
        ValidationException.__name__: 422,
        ResourceNotFoundException.__name__: 404,
        ResourceAlreadyExistsException.__name__: 409,
        DatabaseException.__name__: 500,
        AuthenticationException.__name__: 401,
        AuthorizationException.__name__: 403,
        RateLimitException.__name__: 429,
    }
    
    status_code = status_map.get(exc.error_code, 500)
    
    error_response = ErrorResponse(
        error=exc.error_code,
        message=exc.message,
        details=exc.details,
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle Pydantic validation errors
    """
    logger.error(f"Validation error: {str(exc)}")
    
    error_response = ErrorResponse(
        error="ValidationError",
        message="Invalid input data",
        details={"validation_errors": str(exc)},
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions
    """
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    error_response = ErrorResponse(
        error="HTTPException",
        message=exc.detail,
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        timestamp=datetime.utcnow()
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with a FastAPI application
    """
    app.add_exception_handler(BaseServiceException, base_service_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)