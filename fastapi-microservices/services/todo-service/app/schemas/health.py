from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    """
    Response schema for health check endpoint
    """
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")
    system_metrics: Optional[Dict[str, Any]] = Field(None, description="System performance metrics")
    database_status: Optional[str] = Field(None, description="Database connectivity status")
    database_response_time_ms: Optional[float] = Field(None, description="Database response time in milliseconds")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "todo-service",
                "version": "1.0.0",
                "timestamp": "2023-12-01T10:00:00Z",
                "uptime": 3600.0,
                "system_metrics": {
                    "cpu_usage_percent": 15.2,
                    "memory_usage_percent": 45.8,
                    "memory_available_mb": 2048,
                    "disk_usage_percent": 65.4,
                    "disk_free_gb": 50
                },
                "database_status": "healthy",
                "database_response_time_ms": 12.5
            }
        }