from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoStats
from app.utils.logger import get_logger

logger = get_logger(__name__)

class TodoService:
    """
    Business logic for todo operations using repository pattern
    """
    
    def __init__(self, todo_repository: TodoRepository = None):
        self.todo_repository = todo_repository or TodoRepository()

    async def get_todos(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[TodoResponse]:
        """
        Get todos with optional filtering
        """
        logger.info(f"Getting todos with filters: completed={completed}, search={search}")
        
        # Use repository for database operations
        todos = self.todo_repository.get_todos_with_filters(
            db=db,
            skip=skip,
            limit=limit,
            completed=completed,
            search=search
        )
        
        # Convert to response DTOs
        return [TodoResponse.from_orm(todo) for todo in todos]

    async def get_todo(self, db: Session, todo_id: int) -> Optional[TodoResponse]:
        """
        Get a specific todo by ID
        """
        logger.info(f"Getting todo by ID: {todo_id}")
        
        todo = self.todo_repository.get_by_id(db, todo_id)
        if todo:
            return TodoResponse.from_orm(todo)
        return None

    async def create_todo(self, db: Session, todo_data: TodoCreate) -> TodoResponse:
        """
        Create a new todo
        """
        logger.info(f"Creating new todo: {todo_data.title}")
        
        # Validate business rules (if any)
        self._validate_todo_creation(todo_data)
        
        # Use repository to create todo
        todo = self.todo_repository.create_todo(db, todo_data)
        
        logger.info(f"Successfully created todo with ID: {todo.id}")
        return TodoResponse.from_orm(todo)

    async def update_todo(
        self, 
        db: Session, 
        todo_id: int, 
        todo_update: TodoUpdate
    ) -> Optional[TodoResponse]:
        """
        Update an existing todo
        """
        logger.info(f"Updating todo {todo_id}")
        
        # Validate business rules (if any)
        self._validate_todo_update(todo_update)
        
        # Use repository to update todo
        updated_todo = self.todo_repository.update_todo(db, todo_id, todo_update)
        
        if updated_todo:
            logger.info(f"Successfully updated todo {todo_id}")
            return TodoResponse.from_orm(updated_todo)
        
        logger.warning(f"Todo {todo_id} not found for update")
        return None

    async def toggle_todo_completion(
        self, 
        db: Session, 
        todo_id: int
    ) -> Optional[TodoResponse]:
        """
        Toggle the completion status of a todo
        """
        logger.info(f"Toggling completion status for todo {todo_id}")
        
        # Use repository to toggle completion
        updated_todo = self.todo_repository.toggle_todo_completion(db, todo_id)
        
        if updated_todo:
            status = "completed" if updated_todo.completed else "pending"
            logger.info(f"Successfully toggled todo {todo_id} to {status}")
            return TodoResponse.from_orm(updated_todo)
        
        logger.warning(f"Todo {todo_id} not found for toggle")
        return None

    async def delete_todo(self, db: Session, todo_id: int) -> bool:
        """
        Delete a todo
        """
        logger.info(f"Deleting todo {todo_id}")
        
        # Check if todo exists and if user has permission (business logic)
        todo = self.todo_repository.get_by_id(db, todo_id)
        if not todo:
            logger.warning(f"Todo {todo_id} not found for deletion")
            return False
        
        # Perform any pre-deletion business logic here
        self._validate_todo_deletion(todo)
        
        # Use repository to delete
        success = self.todo_repository.delete(db, todo_id)
        
        if success:
            logger.info(f"Successfully deleted todo {todo_id}")
        
        return success

    async def delete_completed_todos(self, db: Session) -> int:
        """
        Delete all completed todos
        """
        logger.info("Deleting all completed todos")
        
        # Use repository to delete completed todos
        count = self.todo_repository.delete_completed_todos(db)
        
        logger.info(f"Successfully deleted {count} completed todos")
        return count

    async def get_todo_stats(self, db: Session) -> TodoStats:
        """
        Get todo statistics
        """
        logger.info("Generating todo statistics")
        
        # Use repository to get statistics
        stats = self.todo_repository.get_todo_statistics(db)
        
        # Apply any business logic to stats (e.g., additional calculations)
        self._enrich_statistics(stats)
        
        logger.info(f"Generated statistics: {stats.dict()}")
        return stats

    # Private methods for business logic validation
    
    def _validate_todo_creation(self, todo_data: TodoCreate) -> None:
        """
        Validate business rules for todo creation
        """
        # Example business rules:
        # - Title cannot be empty (already handled by Pydantic)
        # - Title cannot be too long
        # - Description cannot contain inappropriate content
        
        if len(todo_data.title.strip()) == 0:
            raise ValueError("Todo title cannot be empty")
        
        if len(todo_data.title) > 200:
            raise ValueError("Todo title is too long")
        
        # Add more business validation as needed
        logger.debug("Todo creation validation passed")
    
    def _validate_todo_update(self, todo_update: TodoUpdate) -> None:
        """
        Validate business rules for todo updates
        """
        if todo_update.title is not None:
            if len(todo_update.title.strip()) == 0:
                raise ValueError("Todo title cannot be empty")
            
            if len(todo_update.title) > 200:
                raise ValueError("Todo title is too long")
        
        logger.debug("Todo update validation passed")
    
    def _validate_todo_deletion(self, todo) -> None:
        """
        Validate business rules for todo deletion
        """
        # Example business rules:
        # - Cannot delete todos that are part of a project
        # - Cannot delete todos created by other users (if multi-user)
        
        # Add business validation as needed
        logger.debug("Todo deletion validation passed")
    
    def _enrich_statistics(self, stats: TodoStats) -> None:
        """
        Add additional business logic to statistics
        """
        # Example: Add productivity insights, trends, etc.
        # This is where you'd add business intelligence
        
        logger.debug("Statistics enrichment completed")