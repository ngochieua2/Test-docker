from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime
from app.repositories.base import BaseRepository
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoStats
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TodoRepository(BaseRepository[Todo]):
    """
    Repository for Todo database operations
    """
    
    def __init__(self):
        super().__init__(Todo)
    
    def get_todos_with_filters(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Todo]:
        """
        Get todos with optional filtering and search
        """
        try:
            query = db.query(Todo)
            
            # Apply completion filter
            if completed is not None:
                query = query.filter(Todo.completed == completed)
                logger.debug(f"Applied completion filter: {completed}")
            
            # Apply search filter
            if search:
                search_filter = or_(
                    Todo.title.ilike(f"%{search}%"),
                    Todo.description.ilike(f"%{search}%")
                )
                query = query.filter(search_filter)
                logger.debug(f"Applied search filter: {search}")
            
            # Apply ordering and pagination
            todos = query.order_by(desc(Todo.created_at)).offset(skip).limit(limit).all()
            
            logger.info(f"Retrieved {len(todos)} todos with filters")
            return todos
            
        except Exception as e:
            logger.error(f"Error getting todos with filters: {str(e)}")
            raise
    
    def create_todo(self, db: Session, todo_data: TodoCreate) -> Todo:
        """
        Create a new todo
        """
        try:
            todo_dict = {
                "title": todo_data.title,
                "description": todo_data.description,
                "completed": todo_data.completed
            }
            
            return self.create(db, todo_dict)
            
        except Exception as e:
            logger.error(f"Error creating todo: {str(e)}")
            raise
    
    def update_todo(
        self, 
        db: Session, 
        todo_id: int, 
        todo_update: TodoUpdate
    ) -> Optional[Todo]:
        """
        Update an existing todo
        """
        try:
            todo = self.get_by_id(db, todo_id)
            if not todo:
                return None
            
            # Get only the fields that were actually provided
            update_data = todo_update.dict(exclude_unset=True)
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            return self.update(db, todo, update_data)
            
        except Exception as e:
            logger.error(f"Error updating todo {todo_id}: {str(e)}")
            raise
    
    def toggle_todo_completion(self, db: Session, todo_id: int) -> Optional[Todo]:
        """
        Toggle the completion status of a todo
        """
        try:
            todo = self.get_by_id(db, todo_id)
            if not todo:
                return None
            
            update_data = {
                "completed": not todo.completed,
                "updated_at": datetime.utcnow()
            }
            
            updated_todo = self.update(db, todo, update_data)
            
            status = "completed" if updated_todo.completed else "pending"
            logger.info(f"Toggled todo {todo_id} to {status}")
            
            return updated_todo
            
        except Exception as e:
            logger.error(f"Error toggling todo {todo_id}: {str(e)}")
            raise
    
    def delete_completed_todos(self, db: Session) -> int:
        """
        Delete all completed todos and return count
        """
        try:
            # Get count first
            completed_count = db.query(func.count(Todo.id)).filter(Todo.completed == True).scalar()
            
            if completed_count > 0:
                # Delete completed todos
                db.query(Todo).filter(Todo.completed == True).delete()
                db.commit()
                logger.info(f"Deleted {completed_count} completed todos")
            
            return completed_count
            
        except Exception as e:
            logger.error(f"Error deleting completed todos: {str(e)}")
            db.rollback()
            raise
    
    def get_todo_statistics(self, db: Session) -> TodoStats:
        """
        Get comprehensive todo statistics
        """
        try:
            # Get total count
            total = db.query(func.count(Todo.id)).scalar()
            
            # Get completed count
            completed = db.query(func.count(Todo.id)).filter(Todo.completed == True).scalar()
            
            # Calculate pending count
            pending = total - completed
            
            # Calculate completion rate
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            # Get recent todos (created today)
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            recent_todos = db.query(func.count(Todo.id)).filter(
                Todo.created_at >= today_start
            ).scalar()
            
            stats = TodoStats(
                total=total,
                completed=completed,
                pending=pending,
                completion_rate=round(completion_rate, 2),
                recent_todos=recent_todos
            )
            
            logger.info(f"Generated todo statistics: {stats.dict()}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting todo statistics: {str(e)}")
            raise
    
    def search_todos(self, db: Session, search_term: str, limit: int = 50) -> List[Todo]:
        """
        Search todos by title and description
        """
        try:
            search_filter = or_(
                Todo.title.ilike(f"%{search_term}%"),
                Todo.description.ilike(f"%{search_term}%")
            )
            
            todos = db.query(Todo).filter(search_filter).order_by(
                desc(Todo.created_at)
            ).limit(limit).all()
            
            logger.info(f"Found {len(todos)} todos matching search: {search_term}")
            return todos
            
        except Exception as e:
            logger.error(f"Error searching todos: {str(e)}")
            raise
    
    def get_todos_by_completion_status(
        self, 
        db: Session, 
        completed: bool, 
        limit: int = 100
    ) -> List[Todo]:
        """
        Get todos filtered by completion status
        """
        try:
            todos = db.query(Todo).filter(
                Todo.completed == completed
            ).order_by(desc(Todo.created_at)).limit(limit).all()
            
            status_text = "completed" if completed else "pending"
            logger.info(f"Retrieved {len(todos)} {status_text} todos")
            
            return todos
            
        except Exception as e:
            logger.error(f"Error getting todos by status: {str(e)}")
            raise
    
    def get_recent_todos(self, db: Session, days: int = 7, limit: int = 50) -> List[Todo]:
        """
        Get todos created in the last N days
        """
        try:
            cutoff_date = datetime.utcnow() - datetime.timedelta(days=days)
            
            todos = db.query(Todo).filter(
                Todo.created_at >= cutoff_date
            ).order_by(desc(Todo.created_at)).limit(limit).all()
            
            logger.info(f"Retrieved {len(todos)} todos from last {days} days")
            return todos
            
        except Exception as e:
            logger.error(f"Error getting recent todos: {str(e)}")
            raise