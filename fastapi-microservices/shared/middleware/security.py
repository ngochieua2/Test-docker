"""
Security middleware components
"""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiting middleware
    """
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Number of calls allowed
        self.period = period  # Time period in seconds
        self.clients: Dict[str, List[float]] = defaultdict(list)
    
    def _clean_old_requests(self, client_id: str, current_time: float):
        """Remove old requests outside the time window"""
        cutoff_time = current_time - self.period
        self.clients[client_id] = [
            timestamp for timestamp in self.clients[client_id]
            if timestamp > cutoff_time
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old requests
        self._clean_old_requests(client_id, current_time)
        
        # Check rate limit
        if len(self.clients[client_id]) >= self.calls:
            logger.warning(f"Rate limit exceeded for client {client_id}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Add current request
        self.clients[client_id].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = max(0, self.calls - len(self.clients[client_id]))
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.period))
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response