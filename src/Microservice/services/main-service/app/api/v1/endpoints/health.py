from fastapi import APIRouter, Depends
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check(health_service: HealthService = Depends(HealthService)):
    """
    Health check endpoint
    """
    return await health_service.get_health_status()