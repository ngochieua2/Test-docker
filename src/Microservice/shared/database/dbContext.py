from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for models
Base = declarative_base()

# Global variables that will be set by initialize_database() or use legacy defaults
engine = None
SessionLocal = None

def initialize_database(database_url: str = None, echo: bool = True):
    """
    Initialize the database with a specific DATABASE_URL
    This should be called by each service with their specific settings
    """
    global engine, SessionLocal
    
    if database_url is None:
        raise ValueError("database_url is required and cannot be None")
    
    engine = create_engine(database_url, echo=echo)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return engine, SessionLocal

def get_db():
    """
    Database dependency for FastAPI
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call initialize_database() first.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()