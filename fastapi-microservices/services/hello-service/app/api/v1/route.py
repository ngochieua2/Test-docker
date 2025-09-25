from fastapi import APIRouter
from app.api.v1.endpoints import hello, health

api_router = APIRouter()

# Include route modules from endpoints
api_router.include_router(hello.router, prefix="/hello", tags=["hello"])
api_router.include_router(health.router, prefix="/health", tags=["health"])