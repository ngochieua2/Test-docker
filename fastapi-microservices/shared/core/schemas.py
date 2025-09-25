"""
Common response models and schemas that can be used across services
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, Dict


class BaseResponse(BaseModel):
    """
    Base response model for consistent API responses
    """
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "timestamp": "2023-12-01T10:00:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standardized error response model
    """
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"field": "title", "issue": "cannot be empty"},
                "timestamp": "2023-12-01T10:00:00Z"
            }
        }


class SuccessResponse(BaseResponse):
    """
    Success response with optional data payload
    """
    data: Optional[Any] = Field(None, description="Response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "timestamp": "2023-12-01T10:00:00Z",
                "data": {"id": 1, "status": "created"}
            }
        }


class PaginatedResponse(BaseModel):
    """
    Paginated response model for list endpoints
    """
    items: list = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    pages: int = Field(..., description="Total number of pages")
    per_page: int = Field(..., description="Items per page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [{"id": 1, "name": "Item 1"}],
                "total": 100,
                "page": 1,
                "pages": 10,
                "per_page": 10
            }
        }