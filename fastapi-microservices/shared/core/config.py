"""
Base configuration settings that can be shared across services
"""
from typing import List
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """
    Base settings class that can be inherited by individual services
    """
    
    # Basic app configuration
    DEBUG: bool = False
    
    # Server configuration
    HOST: str = "0.0.0.0"
    
    # API configuration
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
    ]
    
    # Documentation settings
    ENABLE_DOCS: bool = True
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class BaseHealthResponse:
    """
    Base health response structure for consistency across services
    """
    
    @staticmethod
    def create_health_response(
        service_name: str,
        version: str,
        status: str = "healthy",
        **kwargs
    ) -> dict:
        """
        Create a standardized health response
        """
        from datetime import datetime
        
        response = {
            "status": status,
            "service": service_name,
            "version": version,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Add any additional fields
        response.update(kwargs)
        
        return response