import psutil
import time
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.health import HealthResponse
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class HealthService:
    """
    Business logic for health check operations
    """
    
    async def get_health_status(self, db: Session) -> HealthResponse:
        """
        Get comprehensive health status including database connectivity
        """
        logger.info("Performing health check")
        
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check database connectivity
        db_status = "healthy"
        db_response_time = 0
        try:
            start_time = time.time()
            db.execute(text("SELECT 1"))
            db_response_time = round((time.time() - start_time) * 1000, 2)  # Convert to ms
            logger.info(f"Database connectivity check passed in {db_response_time}ms")
        except Exception as e:
            db_status = "unhealthy"
            logger.error(f"Database connectivity check failed: {str(e)}")
        
        # Determine overall status
        overall_status = "healthy" if db_status == "healthy" else "unhealthy"
        
        return HealthResponse(
            status=overall_status,
            service="todo-service",
            version=settings.VERSION,
            timestamp=datetime.utcnow(),
            uptime=self._get_uptime(),
            system_metrics={
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available // 1024 // 1024,
                "disk_usage_percent": disk.percent,
                "disk_free_gb": disk.free // 1024 // 1024 // 1024
            },
            database_status=db_status,
            database_response_time_ms=db_response_time
        )
    
    def _get_uptime(self) -> float:
        """
        Calculate service uptime in seconds
        """
        # In a real application, you'd track start time
        # For now, return process uptime
        return time.time() - psutil.Process().create_time()