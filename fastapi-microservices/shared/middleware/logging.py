"""
Request logging middleware that can be used across all services
"""
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests and their responses
    """
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        # Generate request ID
        request_id = str(uuid.uuid4())
        
        # Start timing
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Incoming request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )
        
        # Add request ID to headers for downstream services
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


class CORSMiddleware(BaseHTTPMiddleware):
    """
    Custom CORS middleware with detailed logging
    """
    
    def __init__(self, app, allow_origins=None, allow_methods=None, allow_headers=None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
    
    async def dispatch(self, request: Request, call_next) -> StarletteResponse:
        origin = request.headers.get("origin")
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            response.headers["Access-Control-Allow-Origin"] = origin or "*"
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            response.headers["Access-Control-Max-Age"] = "86400"
            return response
        
        # Process regular request
        response = await call_next(request)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = origin or "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response