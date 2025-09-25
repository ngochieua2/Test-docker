import pytest
from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.todo import Todo
from datetime import datetime

@pytest.mark.asyncio
async def test_todo_repository_create_todo(db_session: Session):
    """
    Test TodoRepository create_todo method
    """
    repository = TodoRepository()
    todo_data = TodoCreate(
        title="Test Todo",
        description="Test Description",
        completed=False
    )
    
    # Create todo using repository
    created_todo = repository.create_todo(db_session, todo_data)
    
    # Verify todo was created
    assert created_todo.id is not None
    assert created_todo.title == "Test Todo"
    assert created_todo.description == "Test Description"
    assert created_todo.completed == False
    assert created_todo.created_at is not None
    assert created_todo.updated_at is not None

@pytest.mark.asyncio
async def test_todo_repository_get_by_id(db_session: Session):
    """
    Test TodoRepository get_by_id method
    """
    repository = TodoRepository()
    
    # Create a todo first
    todo_data = TodoCreate(title="Test Todo", description="Test", completed=False)
    created_todo = repository.create_todo(db_session, todo_data)
    
    # Get todo by ID
    retrieved_todo = repository.get_by_id(db_session, created_todo.id)
    
    # Verify todo was retrieved correctly
    assert retrieved_todo is not None
    assert retrieved_todo.id == created_todo.id
    assert retrieved_todo.title == created_todo.title

@pytest.mark.asyncio
async def test_todo_repository_get_todos_with_filters(db_session: Session):
    """
    Test TodoRepository get_todos_with_filters method
    """
    repository = TodoRepository()
    
    # Create multiple todos
    todo1_data = TodoCreate(title="Completed Todo", description="Done", completed=True)
    todo2_data = TodoCreate(title="Pending Todo", description="Not done", completed=False)
    todo3_data = TodoCreate(title="Search Todo", description="Find me", completed=False)
    
    repository.create_todo(db_session, todo1_data)
    repository.create_todo(db_session, todo2_data)
    repository.create_todo(db_session, todo3_data)
    
    # Test filter by completed status
    completed_todos = repository.get_todos_with_filters(db_session, completed=True)
    assert len(completed_todos) == 1
    assert completed_todos[0].completed == True
    
    # Test filter by pending status
    pending_todos = repository.get_todos_with_filters(db_session, completed=False)
    assert len(pending_todos) == 2
    assert all(not todo.completed for todo in pending_todos)
    
    # Test search filter
    search_todos = repository.get_todos_with_filters(db_session, search="Search")
    assert len(search_todos) == 1
    assert "Search" in search_todos[0].title

@pytest.mark.asyncio
async def test_todo_repository_update_todo(db_session: Session):
    """
    Test TodoRepository update_todo method
    """
    repository = TodoRepository()
    
    # Create a todo first
    todo_data = TodoCreate(title="Original Title", description="Original", completed=False)
    created_todo = repository.create_todo(db_session, todo_data)
    
    # Update the todo
    update_data = TodoUpdate(title="Updated Title", completed=True)
    updated_todo = repository.update_todo(db_session, created_todo.id, update_data)
    
    # Verify todo was updated
    assert updated_todo is not None
    assert updated_todo.id == created_todo.id
    assert updated_todo.title == "Updated Title"
    assert updated_todo.completed == True
    assert updated_todo.description == "Original"  # Should remain unchanged

@pytest.mark.asyncio
async def test_todo_repository_toggle_completion(db_session: Session):
    """
    Test TodoRepository toggle_todo_completion method
    """
    repository = TodoRepository()
    
    # Create a todo
    todo_data = TodoCreate(title="Toggle Test", completed=False)
    created_todo = repository.create_todo(db_session, todo_data)
    original_status = created_todo.completed
    
    # Toggle completion status
    toggled_todo = repository.toggle_todo_completion(db_session, created_todo.id)
    
    # Verify status was toggled
    assert toggled_todo is not None
    assert toggled_todo.completed == (not original_status)
    assert toggled_todo.id == created_todo.id

@pytest.mark.asyncio
async def test_todo_repository_delete_todo(db_session: Session):
    """
    Test TodoRepository delete method
    """
    repository = TodoRepository()
    
    # Create a todo
    todo_data = TodoCreate(title="Delete Test", completed=False)
    created_todo = repository.create_todo(db_session, todo_data)
    
    # Delete the todo
    success = repository.delete(db_session, created_todo.id)
    assert success == True
    
    # Verify todo was deleted
    deleted_todo = repository.get_by_id(db_session, created_todo.id)
    assert deleted_todo is None

@pytest.mark.asyncio
async def test_todo_repository_delete_completed_todos(db_session: Session):
    """
    Test TodoRepository delete_completed_todos method
    """
    repository = TodoRepository()
    
    # Create mix of completed and pending todos
    completed_todo1 = TodoCreate(title="Completed 1", completed=True)
    completed_todo2 = TodoCreate(title="Completed 2", completed=True)
    pending_todo = TodoCreate(title="Pending", completed=False)
    
    repository.create_todo(db_session, completed_todo1)
    repository.create_todo(db_session, completed_todo2)
    repository.create_todo(db_session, pending_todo)
    
    # Delete completed todos
    deleted_count = repository.delete_completed_todos(db_session)
    assert deleted_count == 2
    
    # Verify only pending todos remain
    remaining_todos = repository.get_todos_with_filters(db_session)
    assert len(remaining_todos) == 1
    assert remaining_todos[0].completed == False

@pytest.mark.asyncio
async def test_todo_repository_get_statistics(db_session: Session):
    """
    Test TodoRepository get_todo_statistics method
    """
    repository = TodoRepository()
    
    # Create todos with different statuses
    todos_data = [
        TodoCreate(title="Todo 1", completed=True),
        TodoCreate(title="Todo 2", completed=True),
        TodoCreate(title="Todo 3", completed=False),
        TodoCreate(title="Todo 4", completed=False),
        TodoCreate(title="Todo 5", completed=False),
    ]
    
    for todo_data in todos_data:
        repository.create_todo(db_session, todo_data)
    
    # Get statistics
    stats = repository.get_todo_statistics(db_session)
    
    # Verify statistics
    assert stats.total == 5
    assert stats.completed == 2
    assert stats.pending == 3
    assert stats.completion_rate == 40.0
    assert stats.recent_todos == 5  # All created today

@pytest.mark.asyncio
async def test_todo_repository_search_todos(db_session: Session):
    """
    Test TodoRepository search_todos method
    """
    repository = TodoRepository()
    
    # Create todos with different content
    todos_data = [
        TodoCreate(title="Learn Python Programming", description="Study basics"),
        TodoCreate(title="Buy groceries", description="Milk and bread"),
        TodoCreate(title="Python web development", description="Learn FastAPI"),
    ]
    
    for todo_data in todos_data:
        repository.create_todo(db_session, todo_data)
    
    # Search for Python-related todos
    python_todos = repository.search_todos(db_session, "Python")
    assert len(python_todos) == 2
    
    # Search in description
    fastapi_todos = repository.search_todos(db_session, "FastAPI")
    assert len(fastapi_todos) == 1
    assert "FastAPI" in fastapi_todos[0].description

@pytest.mark.asyncio
async def test_todo_repository_get_by_completion_status(db_session: Session):
    """
    Test TodoRepository get_todos_by_completion_status method
    """
    repository = TodoRepository()
    
    # Create mix of completed and pending todos
    completed_todo = TodoCreate(title="Completed Task", completed=True)
    pending_todo1 = TodoCreate(title="Pending Task 1", completed=False)
    pending_todo2 = TodoCreate(title="Pending Task 2", completed=False)
    
    repository.create_todo(db_session, completed_todo)
    repository.create_todo(db_session, pending_todo1)
    repository.create_todo(db_session, pending_todo2)
    
    # Get completed todos
    completed_todos = repository.get_todos_by_completion_status(db_session, True)
    assert len(completed_todos) == 1
    assert completed_todos[0].completed == True
    
    # Get pending todos
    pending_todos = repository.get_todos_by_completion_status(db_session, False)
    assert len(pending_todos) == 2
    assert all(not todo.completed for todo in pending_todos)

@pytest.mark.asyncio
async def test_todo_repository_error_handling(db_session: Session):
    """
    Test TodoRepository error handling
    """
    repository = TodoRepository()
    
    # Test getting non-existent todo
    non_existent = repository.get_by_id(db_session, 99999)
    assert non_existent is None
    
    # Test updating non-existent todo
    update_data = TodoUpdate(title="Updated")
    updated = repository.update_todo(db_session, 99999, update_data)
    assert updated is None
    
    # Test toggling non-existent todo
    toggled = repository.toggle_todo_completion(db_session, 99999)
    assert toggled is None
    
    # Test deleting non-existent todo
    deleted = repository.delete(db_session, 99999)
    assert deleted == False