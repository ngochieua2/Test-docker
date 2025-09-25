import logging
import sys
from typing import Optional
from app.core.config import settings

def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configure logger
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        
        # Create formatter
        formatter = logging.Formatter(settings.LOG_FORMAT)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Prevent duplicate logs
        logger.propagate = False
    
    return logger

def setup_logging():
    """
    Setup application-wide logging configuration
    """
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )