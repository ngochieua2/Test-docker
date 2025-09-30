from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class DatabaseStatus(BaseModel):
    """
    Database connectivity status
    """
    connected: bool = Field(..., description="Whether database connection is successful")
    response_time_ms: Optional[float] = Field(None, description="Database response time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if connection failed")

class HealthResponse(BaseModel):
    """
    Response schema for health check endpoint
    """
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")
    system_metrics: Optional[Dict[str, Any]] = Field(None, description="System performance metrics")
    database: Optional[DatabaseStatus] = Field(None, description="Database connectivity status")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                "database": {
                    "connected": True,
                    "response_time_ms": 15.2,
                    "error": None
                }
            }
        }