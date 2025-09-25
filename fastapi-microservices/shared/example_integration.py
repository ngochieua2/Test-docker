"""
Example of how to integrate shared components into a FastAPI service

This example shows how to use the new organized shared structure
in your service's application factory.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import shared components
from shared import (
    BaseAppSettings, 
    register_exception_handlers,
    BaseResponse
)
from shared.middleware.logging import RequestLoggingMiddleware
from shared.middleware.security import RateLimitMiddleware, SecurityHeadersMiddleware
from shared.utils.datetime_utils import utc_now


class ExampleServiceSettings(BaseAppSettings):
    """
    Service-specific settings extending the base configuration
    """
    APP_NAME: str = "Example Service"
    VERSION: str = "1.0.0"
    PORT: int = 8003


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Service lifespan with startup and shutdown events
    """
    settings = ExampleServiceSettings()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"⏰ Startup time: {utc_now()}")
    
    yield
    
    print(f"🛑 Shutting down {settings.APP_NAME}")


def create_example_service() -> FastAPI:
    """
    Example service factory using shared components
    """
    settings = ExampleServiceSettings()
    
    # Create FastAPI app with lifespan
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        lifespan=lifespan,
    )
    
    # Add shared middleware
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Add CORS middleware using shared configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register shared exception handlers
    register_exception_handlers(app)
    
    # Add example endpoint using shared response schema
    @app.get("/", response_model=BaseResponse)
    async def root():
        return BaseResponse(
            message=f"Welcome to {settings.APP_NAME}!",
            timestamp=utc_now()
        )
    
    @app.get("/health", response_model=BaseResponse)
    async def health_check():
        return BaseResponse(
            message="Service is healthy",
            timestamp=utc_now()
        )
    
    return app


# Example usage
if __name__ == "__main__":
    import uvicorn
    
    settings = ExampleServiceSettings()
    app = create_example_service()
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )