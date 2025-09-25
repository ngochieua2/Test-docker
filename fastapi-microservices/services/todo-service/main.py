import uvicorn
from contextlib import asynccontextmanager
from app.core.app import create_application
from app.core.config import settings
from app.utils.logger import setup_logging, get_logger
from app.core.database import engine
from app.models.todo import Todo

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app):
    """
    Application lifespan context manager
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info(f"Docs available at: http://{settings.HOST}:{settings.PORT}/docs")
    
    # Create database tables (in production, use Alembic migrations)
    Todo.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
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