from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class CrudExampleBase(BaseModel):
    """
    Base Crud Example schema with shared attributes
    """
    name: str = Field(..., min_length=1, max_length=200, description="Crud Example title")
    description: Optional[str] = Field(None, max_length=1000, description="Crud Example description")
    isActive: bool = Field(False, description="Crud Example Is Active")
    status: int = Field(0, description="Crud Example status")

class CrudExampleCreate(CrudExampleBase):
    """
    Schema for creating a new crud example
    """
    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @field_validator('description')
    def description_validator(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "ex name",
                "description": "ex description",
                "isActive": False,
                "status": 0
            }
        }

class CrudExampleUpdate(CrudExampleBase):
    """
    Schema for updating an existing crud example
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Crud Example title")
    description: Optional[str] = Field(None, max_length=1000, description="Crud Example description")
    isActive: Optional[bool] = Field(None, description="Crud Example Is Active")
    status: Optional[int] = Field(None, description="Crud Example status")

    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('name cannot be empty')
        return v.strip() if v else v
    
    @field_validator('description')
    def description_validator(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    class Config:
        json_schema_extra = {
           "example": {
                "name": "ex title",
                "description": "ex description",
                "isActive": False,
                "status": 0
            }
        }

class CrudExampleResponse(CrudExampleBase):
    """
    Schema for crud example responses
    """
    id: int = Field(..., description="Crud Example ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "ex name",
                "description": "ex description",
                "isActive": False,
                "status": 0,
                "created_at": "2023-12-01T10:00:00Z",
                "updated_at": "2023-12-01T10:00:00Z"
            }
        }
