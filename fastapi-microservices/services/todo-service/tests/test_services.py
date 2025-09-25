import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from app.services.todo_service import TodoService
from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.todo import Todo

@pytest.mark.asyncio
async def test_todo_service_get_todos_empty():
    """
    Test TodoService get_todos method with empty database
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_query = Mock()
    mock_query.filter.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []
    mock_db.query.return_value = mock_query
    
    service = TodoService()
    result = await service.get_todos(mock_db)
    
    assert isinstance(result, list)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_todo_service_create_todo():
    """
    Test TodoService create_todo method
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_todo = Todo(id=1, title="Test Todo", description="Test", completed=False)
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    # Mock the refresh to set the ID
    def mock_refresh(todo):
        todo.id = 1
        todo.created_at = "2023-12-01T10:00:00Z"
        todo.updated_at = "2023-12-01T10:00:00Z"
    
    mock_db.refresh.side_effect = mock_refresh
    
    service = TodoService()
    todo_data = TodoCreate(title="Test Todo", description="Test", completed=False)
    
    result = await service.create_todo(mock_db, todo_data)
    
    # Verify database operations were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_todo_service_get_todo_by_id():
    """
    Test TodoService get_todo method
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_todo = Todo(id=1, title="Test Todo", description="Test", completed=False)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_todo
    mock_db.query.return_value = mock_query
    
    service = TodoService()
    result = await service.get_todo(mock_db, 1)
    
    assert result is not None

@pytest.mark.asyncio
async def test_todo_service_get_todo_not_found():
    """
    Test TodoService get_todo method when todo doesn't exist
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query
    
    service = TodoService()
    result = await service.get_todo(mock_db, 999)
    
    assert result is None

@pytest.mark.asyncio
async def test_todo_service_delete_todo():
    """
    Test TodoService delete_todo method
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_todo = Todo(id=1, title="Test Todo", description="Test", completed=False)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_todo
    mock_db.query.return_value = mock_query
    mock_db.delete = Mock()
    mock_db.commit = Mock()
    
    service = TodoService()
    result = await service.delete_todo(mock_db, 1)
    
    assert result == True
    mock_db.delete.assert_called_once_with(mock_todo)
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_todo_service_delete_todo_not_found():
    """
    Test TodoService delete_todo method when todo doesn't exist
    """
    # Mock database session
    mock_db = Mock(spec=Session)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db.query.return_value = mock_query
    
    service = TodoService()
    result = await service.delete_todo(mock_db, 999)
    
    assert result == False

@pytest.mark.asyncio
async def test_todo_service_toggle_completion():
    """
    Test TodoService toggle_todo_completion method
    """
    # Mock database session and todo
    mock_db = Mock(spec=Session)
    mock_todo = Todo(id=1, title="Test Todo", completed=False)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_todo
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    service = TodoService()
    result = await service.toggle_todo_completion(mock_db, 1)
    
    # Verify completion status was toggled
    assert mock_todo.completed == True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_todo_service_update_todo():
    """
    Test TodoService update_todo method
    """
    # Mock database session and todo
    mock_db = Mock(spec=Session)
    mock_todo = Todo(id=1, title="Old Title", description="Old Desc", completed=False)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_todo
    mock_db.query.return_value = mock_query
    mock_db.commit = Mock()
    mock_db.refresh = Mock()
    
    service = TodoService()
    update_data = TodoUpdate(title="New Title", completed=True)
    result = await service.update_todo(mock_db, 1, update_data)
    
    # Verify todo was updated
    assert mock_todo.title == "New Title"
    assert mock_todo.completed == True
    assert mock_todo.description == "Old Desc"  # Should remain unchanged
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()