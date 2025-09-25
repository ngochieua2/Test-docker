import pytest
from fastapi.testclient import TestClient

def test_get_todos_empty(client: TestClient):
    """
    Test getting todos when none exist
    """
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_todo(client: TestClient, sample_todo_create):
    """
    Test creating a new todo
    """
    response = client.post("/api/v1/todos/", json=sample_todo_create)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == sample_todo_create["title"]
    assert data["description"] == sample_todo_create["description"]
    assert data["completed"] == sample_todo_create["completed"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_todo_validation_error(client: TestClient):
    """
    Test creating todo with invalid data
    """
    # Test empty title
    response = client.post("/api/v1/todos/", json={"title": "", "description": "Test"})
    assert response.status_code == 422
    
    # Test missing title
    response = client.post("/api/v1/todos/", json={"description": "Test"})
    assert response.status_code == 422

def test_get_todos_with_data(client: TestClient, sample_todo_create):
    """
    Test getting todos when data exists
    """
    # Create a todo first
    client.post("/api/v1/todos/", json=sample_todo_create)
    
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_todo_create["title"]

def test_get_todo_by_id(client: TestClient, sample_todo_create):
    """
    Test getting a specific todo by ID
    """
    # Create a todo first
    create_response = client.post("/api/v1/todos/", json=sample_todo_create)
    created_todo = create_response.json()
    todo_id = created_todo["id"]
    
    # Get the todo by ID
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == sample_todo_create["title"]

def test_get_todo_not_found(client: TestClient):
    """
    Test getting a non-existent todo
    """
    response = client.get("/api/v1/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_update_todo(client: TestClient, sample_todo_create, sample_todo_update):
    """
    Test updating an existing todo
    """
    # Create a todo first
    create_response = client.post("/api/v1/todos/", json=sample_todo_create)
    created_todo = create_response.json()
    todo_id = created_todo["id"]
    
    # Update the todo
    response = client.put(f"/api/v1/todos/{todo_id}", json=sample_todo_update)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == sample_todo_update["title"]
    assert data["description"] == sample_todo_update["description"]
    assert data["completed"] == sample_todo_update["completed"]

def test_update_todo_not_found(client: TestClient, sample_todo_update):
    """
    Test updating a non-existent todo
    """
    response = client.put("/api/v1/todos/999", json=sample_todo_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_toggle_todo_completion(client: TestClient, sample_todo_create):
    """
    Test toggling todo completion status
    """
    # Create a todo first
    create_response = client.post("/api/v1/todos/", json=sample_todo_create)
    created_todo = create_response.json()
    todo_id = created_todo["id"]
    original_status = created_todo["completed"]
    
    # Toggle completion status
    response = client.patch(f"/api/v1/todos/{todo_id}/toggle")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] == (not original_status)

def test_delete_todo(client: TestClient, sample_todo_create):
    """
    Test deleting a todo
    """
    # Create a todo first
    create_response = client.post("/api/v1/todos/", json=sample_todo_create)
    created_todo = create_response.json()
    todo_id = created_todo["id"]
    
    # Delete the todo
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404

def test_delete_todo_not_found(client: TestClient):
    """
    Test deleting a non-existent todo
    """
    response = client.delete("/api/v1/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_get_todos_with_filters(client: TestClient):
    """
    Test getting todos with filters
    """
    # Create multiple todos
    todo1 = {"title": "Completed Task", "description": "Done", "completed": True}
    todo2 = {"title": "Pending Task", "description": "Not done", "completed": False}
    
    client.post("/api/v1/todos/", json=todo1)
    client.post("/api/v1/todos/", json=todo2)
    
    # Test completed filter
    response = client.get("/api/v1/todos/?completed=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["completed"] == True
    
    # Test pending filter
    response = client.get("/api/v1/todos/?completed=false")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["completed"] == False

def test_get_todos_with_search(client: TestClient):
    """
    Test getting todos with search filter
    """
    # Create todos with different content
    todo1 = {"title": "Learn Python", "description": "Study programming"}
    todo2 = {"title": "Buy groceries", "description": "Milk and bread"}
    
    client.post("/api/v1/todos/", json=todo1)
    client.post("/api/v1/todos/", json=todo2)
    
    # Search in title
    response = client.get("/api/v1/todos/?search=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Python" in data[0]["title"]
    
    # Search in description
    response = client.get("/api/v1/todos/?search=programming")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "programming" in data[0]["description"]

def test_get_todo_stats(client: TestClient):
    """
    Test getting todo statistics
    """
    # Create some todos
    todos = [
        {"title": "Task 1", "completed": True},
        {"title": "Task 2", "completed": False},
        {"title": "Task 3", "completed": True},
    ]
    
    for todo in todos:
        client.post("/api/v1/todos/", json=todo)
    
    # Get stats
    response = client.get("/api/v1/todos/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 3
    assert data["completed"] == 2
    assert data["pending"] == 1
    assert data["completion_rate"] == 66.67

def test_delete_completed_todos(client: TestClient):
    """
    Test deleting all completed todos
    """
    # Create mix of completed and pending todos
    todos = [
        {"title": "Task 1", "completed": True},
        {"title": "Task 2", "completed": False},
        {"title": "Task 3", "completed": True},
    ]
    
    for todo in todos:
        client.post("/api/v1/todos/", json=todo)
    
    # Delete completed todos
    response = client.delete("/api/v1/todos/")
    assert response.status_code == 200
    assert response.json()["message"] == "Deleted 2 completed todos"
    
    # Verify only pending todos remain
    get_response = client.get("/api/v1/todos/")
    remaining_todos = get_response.json()
    assert len(remaining_todos) == 1
    assert remaining_todos[0]["completed"] == False