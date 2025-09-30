import logging
import sys
from typing import Optional


def get_logger(name: str, log_level: str = "INFO", log_format: Optional[str] = None) -> logging.Logger:
    """
    Get configured logger instance
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Configure logger
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatter
        default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format or default_format)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Prevent duplicate logs
        logger.propagate = False
    
    return logger


def setup_logging(log_level: str = "INFO", log_format: Optional[str] = None):
    """
    Setup application-wide logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
    """
    default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format or default_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )