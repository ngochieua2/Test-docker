import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # Basic app configuration
    APP_NAME: str = "Hello Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Database configuration (if needed later)
    DATABASE_URL: Optional[str] = None
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Feature flags
    ENABLE_DOCS: bool = True
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()