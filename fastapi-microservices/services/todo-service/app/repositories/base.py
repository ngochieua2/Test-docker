from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import Base
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType], ABC):
    """
    Base repository class with common database operations
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID
        """
        try:
            result = db.query(self.model).filter(self.model.id == id).first()
            if result:
                logger.debug(f"Found {self.model.__name__} with ID: {id}")
            else:
                logger.debug(f"No {self.model.__name__} found with ID: {id}")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_by_id: {str(e)}")
            raise
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Any] = None
    ) -> List[ModelType]:
        """
        Get multiple records with optional filtering and pagination
        """
        try:
            query = db.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            # Apply ordering
            if order_by is not None:
                query = query.order_by(order_by)
            
            # Apply pagination
            results = query.offset(skip).limit(limit).all()
            logger.debug(f"Retrieved {len(results)} {self.model.__name__} records")
            return results
            
        except SQLAlchemyError as e:
            logger.error(f"Database error in get_multi: {str(e)}")
            raise
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record
        """
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Created {self.model.__name__} with ID: {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Database error in create: {str(e)}")
            db.rollback()
            raise
    
    def update(
        self, 
        db: Session, 
        db_obj: ModelType, 
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """
        Update an existing record
        """
        try:
            for field, value in obj_in.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Updated {self.model.__name__} with ID: {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Database error in update: {str(e)}")
            db.rollback()
            raise
    
    def delete(self, db: Session, id: Any) -> bool:
        """
        Delete a record by ID
        """
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if obj:
                db.delete(obj)
                db.commit()
                logger.info(f"Deleted {self.model.__name__} with ID: {id}")
                return True
            else:
                logger.warning(f"No {self.model.__name__} found with ID: {id} for deletion")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete: {str(e)}")
            db.rollback()
            raise
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filtering
        """
        try:
            query = db.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            count = query.count()
            logger.debug(f"Counted {count} {self.model.__name__} records")
            return count
            
        except SQLAlchemyError as e:
            logger.error(f"Database error in count: {str(e)}")
            raise
    
    def exists(self, db: Session, id: Any) -> bool:
        """
        Check if a record exists by ID
        """
        try:
            exists = db.query(self.model).filter(self.model.id == id).first() is not None
            logger.debug(f"{self.model.__name__} with ID {id} exists: {exists}")
            return exists
        except SQLAlchemyError as e:
            logger.error(f"Database error in exists: {str(e)}")
            raise