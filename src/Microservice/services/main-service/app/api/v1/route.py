from fastapi import APIRouter
from app.api.v1.endpoints import crud_example, process_data, health

api_router = APIRouter()

# Include route modules from endpoints
api_router.include_router(crud_example.router, prefix="/crud-example", tags=["Crud Example API"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(process_data.router, prefix="/process-data", tags=["Data Processing"])