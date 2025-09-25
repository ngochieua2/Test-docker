import pytest
from fastapi.testclient import TestClient

def test_get_hello(client: TestClient):
    """
    Test basic hello endpoint
    """
    response = client.get("/api/v1/hello/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "service" in data
    assert data["service"] == "hello-service"
    assert "Hello World!" in data["message"]

def test_post_hello(client: TestClient, sample_hello_request):
    """
    Test personalized hello endpoint
    """
    response = client.post("/api/v1/hello/", json=sample_hello_request)
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "service" in data
    assert data["service"] == "hello-service"
    assert sample_hello_request["name"] in data["message"]

def test_hello_in_language(client: TestClient):
    """
    Test hello in different languages
    """
    # Test English
    response = client.get("/api/v1/hello/greetings/english")
    assert response.status_code == 200
    
    data = response.json()
    assert "Hello" in data["message"]
    assert data["language"] == "english"
    
    # Test Spanish
    response = client.get("/api/v1/hello/greetings/spanish")
    assert response.status_code == 200
    
    data = response.json()
    assert "Hola" in data["message"]
    assert data["language"] == "spanish"
    
    # Test unknown language (should default to English)
    response = client.get("/api/v1/hello/greetings/unknown")
    assert response.status_code == 200
    
    data = response.json()
    assert "Hello" in data["message"]
    assert data["language"] == "unknown"

def test_post_hello_validation(client: TestClient):
    """
    Test request validation for personalized hello
    """
    # Test empty name
    response = client.post("/api/v1/hello/", json={"name": ""})
    assert response.status_code == 422
    
    # Test missing name
    response = client.post("/api/v1/hello/", json={})
    assert response.status_code == 422