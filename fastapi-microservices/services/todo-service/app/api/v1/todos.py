from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.todo_service import TodoService
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoResponse, TodoCreate, TodoUpdate, TodoStats
from app.core.database import get_db
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Dependency injection for repository and service
def get_todo_repository() -> TodoRepository:
    """Get TodoRepository instance"""
    return TodoRepository()

def get_todo_service(todo_repository: TodoRepository = Depends(get_todo_repository)) -> TodoService:
    """Get TodoService instance with injected repository"""
    return TodoService(todo_repository)

@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = Query(0, ge=0, description="Number of todos to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of todos to return"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Get all todos with optional filtering and pagination
    """
    logger.info(f"Fetching todos: skip={skip}, limit={limit}, completed={completed}, search={search}")
    return await todo_service.get_todos(
        db=db,
        skip=skip,
        limit=limit,
        completed=completed,
        search=search
    )

@router.get("/stats", response_model=TodoStats)
async def get_todo_stats(
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Get todo statistics
    """
    logger.info("Fetching todo statistics")
    return await todo_service.get_todo_stats(db)

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Get a specific todo by ID
    """
    logger.info(f"Fetching todo with ID: {todo_id}")
    todo = await todo_service.get_todo(db, todo_id)
    if not todo:
        logger.warning(f"Todo not found: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Create a new todo
    """
    logger.info(f"Creating new todo: {todo.title}")
    try:
        return await todo_service.create_todo(db, todo)
    except ValueError as e:
        logger.warning(f"Validation error creating todo: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Update an existing todo
    """
    logger.info(f"Updating todo {todo_id}")
    try:
        updated_todo = await todo_service.update_todo(db, todo_id, todo_update)
        if not updated_todo:
            logger.warning(f"Todo not found for update: {todo_id}")
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo
    except ValueError as e:
        logger.warning(f"Validation error updating todo: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))

@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
async def toggle_todo_completion(
    todo_id: int,
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Toggle todo completion status
    """
    logger.info(f"Toggling completion status for todo {todo_id}")
    updated_todo = await todo_service.toggle_todo_completion(db, todo_id)
    if not updated_todo:
        logger.warning(f"Todo not found for toggle: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Delete a todo
    """
    logger.info(f"Deleting todo {todo_id}")
    success = await todo_service.delete_todo(db, todo_id)
    if not success:
        logger.warning(f"Todo not found for deletion: {todo_id}")
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@router.delete("/")
async def delete_completed_todos(
    db: Session = Depends(get_db),
    todo_service: TodoService = Depends(get_todo_service)
):
    """
    Delete all completed todos
    """
    logger.info("Deleting all completed todos")
    count = await todo_service.delete_completed_todos(db)
    return {"message": f"Deleted {count} completed todos"}