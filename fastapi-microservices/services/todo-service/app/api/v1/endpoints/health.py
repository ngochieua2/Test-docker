from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check(
    db: Session = Depends(get_db),
    health_service: HealthService = Depends(HealthService)
):
    """
    Health check endpoint with database connectivity check
    """
    return await health_service.get_health_status(db)