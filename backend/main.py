from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Docker Swarm Demo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configurations
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@postgresql:5432/postgres")
SQLSERVER_URL = os.getenv("SQLSERVER_URL", "mssql+pyodbc://sa:YourStrong@Passw0rd@sqlserver:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")

# Database engines for connection testing
postgres_engine = create_engine(POSTGRES_URL)
try:
   sqlserver_engine = create_engine(SQLSERVER_URL)
except Exception as e:
   logger.warning(f"SQL Server connection failed: {e}")
   sqlserver_engine = None

# For now, set engines to None since database configs are commented
# postgres_engine = None
# sqlserver_engine = None

# Health check endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/postgres")
async def postgres_health():
    try:
        with postgres_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "postgresql"}
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")
        raise HTTPException(status_code=503, detail="PostgreSQL not available")

@app.get("/health/sqlserver")
async def sqlserver_health():
    try:
        if sqlserver_engine is None:
            raise Exception("SQL Server engine not initialized")
        with sqlserver_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "sqlserver"}
    except Exception as e:
        logger.error(f"SQL Server health check failed: {e}")
        raise HTTPException(status_code=503, detail="SQL Server not available")

# API endpoints
@app.get("/")
async def root():
    return {
        "message": "Docker Swarm Demo API",
        "version": "1.0.0",
        "status": "success",
        "endpoints": {
            "health": "/health",
            "sample": "/sample"
        }
    }

# Sample API endpoint
@app.get("/sample")
async def sample_endpoint():
    return {
        "status": "success",
        "message": "API is working successfully!",
        "timestamp": datetime.utcnow(),
        "data": {
            "postgres_connected": "available" if postgres_engine else "unavailable",
            "sqlserver_connected": "available" if sqlserver_engine else "unavailable"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)