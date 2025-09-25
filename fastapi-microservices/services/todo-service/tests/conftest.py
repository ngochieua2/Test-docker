import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.app import create_application
from app.core.database import get_db, Base
from app.models.todo import Todo

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Override database dependency for testing
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    """
    Create test client with test database
    """
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    
    # Create app and override database dependency
    app = create_application()
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_todo_create():
    """
    Sample todo creation data
    """
    return {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    }

@pytest.fixture
def sample_todo_update():
    """
    Sample todo update data
    """
    return {
        "title": "Updated Test Todo",
        "description": "This is an updated test todo",
        "completed": True
    }

@pytest.fixture
def db_session():
    """
    Create database session for direct database operations in tests
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)