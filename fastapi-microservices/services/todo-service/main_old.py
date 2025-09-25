from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Add parent directory to path to access shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from shared.database import get_db
from shared.schemas import TodoResponse, TodoCreate, TodoUpdate
from shared.services import TodoService

app = FastAPI(title="Todo Service", version="1.0.0")

@app.get("/todos", response_model=List[TodoResponse])
async def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all todos with pagination"""
    todo_service = TodoService(db)
    todos = todo_service.get_todos(skip=skip, limit=limit)
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo_service = TodoService(db)
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    todo_service = TodoService(db)
    return todo_service.create_todo(todo)

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo"""
    todo_service = TodoService(db)
    updated_todo = todo_service.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    todo_service = TodoService(db)
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return JSONResponse(content={"message": "Todo deleted successfully"})

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "todo-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)