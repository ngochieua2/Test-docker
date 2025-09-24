from fastapi import HTTPException
from sqlalchemy.orm import Session
from shared.models import Todo
from shared.schemas import TodoCreate, TodoUpdate
from typing import List, Optional

class TodoService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_todos(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        return self.db.query(Todo).offset(skip).limit(limit).all()
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()
    
    def create_todo(self, todo: TodoCreate) -> Todo:
        db_todo = Todo(**todo.dict())
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        db_todo = self.get_todo(todo_id)
        if not db_todo:
            return None
        
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def delete_todo(self, todo_id: int) -> bool:
        db_todo = self.get_todo(todo_id)
        if not db_todo:
            return False
        
        self.db.delete(db_todo)
        self.db.commit()
        return True