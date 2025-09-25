from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    health_service = HealthService()
    return await health_service.get_health_status()