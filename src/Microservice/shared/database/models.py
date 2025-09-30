from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from shared.database.dbContext import Base

class CrudExample(Base):
    """
    CrudExample database model
    """
    __tablename__ = "crudExamples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    isActive = Column(Boolean, default=False, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<CrudExample(id={self.id}, name='{self.name}')>"