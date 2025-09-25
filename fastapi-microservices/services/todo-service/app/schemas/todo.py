from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class TodoBase(BaseModel):
    """
    Base todo schema with shared attributes
    """
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: bool = Field(False, description="Completion status")

class TodoCreate(TodoBase):
    """
    Schema for creating a new todo
    """
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('description')
    def description_validator(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial and build a todo app",
                "completed": False
            }
        }

class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    completed: Optional[bool] = Field(None, description="Completion status")
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v
    
    @validator('description')
    def description_validator(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Learn Advanced FastAPI",
                "description": "Study advanced FastAPI concepts like dependency injection",
                "completed": True
            }
        }

class TodoResponse(TodoBase):
    """
    Schema for todo responses
    """
    id: int = Field(..., description="Todo ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Learn FastAPI",
                "description": "Complete the FastAPI tutorial and build a todo app",
                "completed": False,
                "created_at": "2023-12-01T10:00:00Z",
                "updated_at": "2023-12-01T10:00:00Z"
            }
        }

class TodoStats(BaseModel):
    """
    Schema for todo statistics
    """
    total: int = Field(..., description="Total number of todos")
    completed: int = Field(..., description="Number of completed todos")
    pending: int = Field(..., description="Number of pending todos")
    completion_rate: float = Field(..., description="Completion rate as percentage")
    recent_todos: int = Field(..., description="Number of todos created today")
    
    class Config:
        schema_extra = {
            "example": {
                "total": 25,
                "completed": 15,
                "pending": 10,
                "completion_rate": 60.0,
                "recent_todos": 3
            }
        }