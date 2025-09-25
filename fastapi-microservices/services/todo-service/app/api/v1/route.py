from fastapi import APIRouter
from app.api.v1.endpoints import todos, health

api_router = APIRouter()

# Include route modules from endpoints
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
api_router.include_router(health.router, prefix="/health", tags=["health"])