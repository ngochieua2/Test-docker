from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class HelloRequest(BaseModel):
    """
    Request schema for personalized hello
    """
    name: str = Field(..., min_length=1, max_length=100, description="Name to greet")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "World"
            }
        }

class HelloResponse(BaseModel):
    """
    Response schema for hello endpoints
    """
    message: str = Field(..., description="Hello message")
    timestamp: Optional[datetime] = Field(None, description="Response timestamp")
    service: str = Field(..., description="Service name")
    language: Optional[str] = Field(None, description="Language used for greeting")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Hello, World!",
                "timestamp": "2023-12-01T10:00:00Z",
                "service": "hello-service",
                "language": "english"
            }
        }