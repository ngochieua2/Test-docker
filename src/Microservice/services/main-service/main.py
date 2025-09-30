import uvicorn
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Add the parent Microservice directory to Python path so we can import shared modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.app import create_application
from app.core.config import settings
from shared.utils import setup_logging, get_logger
from shared.database.dbContext import initialize_database

# Setup logging
setup_logging(settings.LOG_LEVEL, settings.LOG_FORMAT)
logger = get_logger(__name__, settings.LOG_LEVEL, settings.LOG_FORMAT)

# Initialize database with service-specific settings
if settings.DATABASE_URL is None:
    logger.error("DATABASE_URL is not set in the configuration.")
    raise ValueError("DATABASE_URL is not set in the configuration.")
engine, SessionLocal = initialize_database(settings.DATABASE_URL)

@asynccontextmanager
async def lifespan(app):
    """
    Application lifespan context manager
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Docs available at: http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")

# Create FastAPI application with lifespan
app = create_application(lifespan=lifespan)

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )