import pytest
from fastapi.testclient import TestClient
from app.core.app import create_application

@pytest.fixture
def client():
    """
    Create test client
    """
    app = create_application()
    return TestClient(app)

@pytest.fixture
def sample_hello_request():
    """
    Sample hello request data
    """
    return {"name": "Test User"}