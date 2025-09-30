import psutil
import time
from sqlalchemy import text
from shared.utils import utc_now
from app.schemas.health import HealthResponse, DatabaseStatus
from app.core.config import settings
from shared.utils import get_logger
from shared.database.dbContext import get_db

logger = get_logger(__name__, settings.LOG_LEVEL, settings.LOG_FORMAT)

class HealthService:
    """
    Business logic for health check operations
    """
    
    async def get_health_status(self) -> HealthResponse:
        """
        Get comprehensive health status including database connectivity
        """
        logger.info("Performing health check")
        
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check database connectivity
        database_status = await self._check_database_connectivity()
        
        return HealthResponse(
            version=settings.VERSION,
            timestamp=utc_now(),
            uptime=self._get_uptime(),
            system_metrics={
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available // 1024 // 1024,
                "disk_usage_percent": disk.percent,
                "disk_free_gb": disk.free // 1024 // 1024 // 1024
            },
            database=database_status
        )
    
    async def _check_database_connectivity(self) -> DatabaseStatus:
        """
        Check database connectivity and response time
        """
        try:
            start_time = time.time()
            
            # Get database session
            db_gen = get_db()
            db = next(db_gen)
            
            try:
                # Execute a simple query to test connectivity
                result = db.execute(text("SELECT 1 as test"))
                result.fetchone()
                
                end_time = time.time()
                response_time_ms = (end_time - start_time) * 1000
                
                logger.info(f"Database connectivity check successful - Response time: {response_time_ms:.2f}ms")
                
                return DatabaseStatus(
                    connected=True,
                    response_time_ms=round(response_time_ms, 2),
                    error=None
                )
                
            finally:
                db.close()
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Database connectivity check failed: {error_msg}")
            
            return DatabaseStatus(
                connected=False,
                response_time_ms=None,
                error=error_msg
            )
    
    def _get_uptime(self) -> float:
        """
        Calculate service uptime in seconds
        """
        # In a real application, you'd track start time
        # For now, return process uptime
        return time.time() - psutil.Process().create_time()