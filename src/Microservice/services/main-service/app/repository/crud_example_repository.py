from shared.utils.logger import get_logger
from app.repository.base import BaseRepository
from shared.database.models import CrudExample
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import and_, or_, func, desc
from app.schemas.crudExample import CrudExampleCreate, CrudExampleUpdate
from shared.utils import utc_now

logger = get_logger(__name__)

class CrudExampleRepository(BaseRepository[CrudExample]):

    def __init__(self):
        super().__init__(CrudExample)
    
    def search_crud_example(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        isActive: Optional[bool] = None,
        status: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[CrudExample]:
        """
        Get crud examples with optional filtering and search
        """
        try:
            query = db.query(CrudExample)
            
            # Apply isActive filter
            if isActive is not None:
                query = query.filter(CrudExample.isActive == isActive)
                logger.debug(f"Applied isActive filter: {isActive}")

            # Apply status filter
            if status is not None:
                query = query.filter(CrudExample.status == status)
                logger.debug(f"Applied status filter: {status}")

            # Apply search filter
            if search:
                search_filter = or_(
                    CrudExample.name.ilike(f"%{search}%"),
                    CrudExample.description.ilike(f"%{search}%")
                )
                query = query.filter(search_filter)
                logger.debug(f"Applied search filter: {search}")
            
            # Apply ordering and pagination
            crud_examples = query.order_by(desc(CrudExample.created_at)).offset(skip).limit(limit).all()

            logger.info(f"Retrieved {len(crud_examples)} crud examples with filters")
            return crud_examples

        except Exception as e:
            logger.error(f"Error getting crud examples with filters: {str(e)}")
            raise

    def create_crud_example(
        self, 
        db: Session, 
        crud_example_data: CrudExampleCreate
    ) -> CrudExample:
        """
        Create a new crud example
        """
        try:
            crud_example_dict = {
                "name": crud_example_data.name,
                "description": crud_example_data.description,
                "isActive": crud_example_data.isActive,
                "status": crud_example_data.status
            }
              
            return self.create(db, crud_example_dict)

        except Exception as e:
            logger.error(f"Error creating crud example: {str(e)}")
            raise
    
    def update_crud_example(
        self, 
        db: Session, 
        crud_example_id: int, 
        crud_example_update: CrudExampleUpdate
    ) -> Optional[CrudExample]:
        """
        Update an existing crud example
        """
        try:
            crud_example = self.get_by_id(db, crud_example_id)
            if not crud_example:
                return None
            
            # Get only the fields that were actually provided
            update_data = crud_example_update.model_dump(exclude_unset=True)
            
            # Add updated_at timestamp
            update_data["updated_at"] = utc_now()

            return self.update(db, crud_example, update_data)
            
        except Exception as e:
            logger.error(f"Error updating crud example {crud_example_id}: {str(e)}")
            raise
    
    def delete_crud_example_by_id(
        self, 
        db: Session, 
        crud_example_id: int) -> bool:
        """
        Delete a crud example by ID
        """
        try:
            return self.delete(db, crud_example_id)
        except Exception as e:
            logger.error(f"Error deleting a crud example by ID: {str(e)}")
            db.rollback()
            raise
    
    def get_total_record(self, db: Session) -> int:
        """
        Get total record count
        """
        try:
            # Get total count
            total = db.query(func.count(CrudExample.id)).scalar()
            return total
        except Exception as e:
            logger.error(f"Error getting total record count: {str(e)}")
            raise
    