import uvicorn
from app.core.app import create_application
from app.core.config import settings
from app.utils.logger import setup_logging, get_logger
from app.core.database import engine
from app.models.todo import Todo

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI application
app = create_application()

@app.on_event("startup")
async def startup_event():
    """
    Application startup event
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info(f"Docs available at: http://{settings.HOST}:{settings.PORT}/docs")
    
    # Create database tables (in production, use Alembic migrations)
    Todo.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event
    """
    logger.info(f"Shutting down {settings.APP_NAME}")

if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )