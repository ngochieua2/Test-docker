import psutil
import time
from datetime import datetime
from app.schemas.health import HealthResponse
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class HealthService:
    """
    Business logic for health check operations
    """
    
    async def get_health_status(self) -> HealthResponse:
        """
        Get comprehensive health status
        """
        logger.info("Performing health check")
        
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return HealthResponse(
            status="healthy",
            service="hello-service",
            version=settings.VERSION,
            timestamp=datetime.utcnow(),
            uptime=self._get_uptime(),
            system_metrics={
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available // 1024 // 1024,
                "disk_usage_percent": disk.percent,
                "disk_free_gb": disk.free // 1024 // 1024 // 1024
            }
        )
    
    def _get_uptime(self) -> float:
        """
        Calculate service uptime in seconds
        """
        # In a real application, you'd track start time
        # For now, return process uptime
        return time.time() - psutil.Process().create_time()