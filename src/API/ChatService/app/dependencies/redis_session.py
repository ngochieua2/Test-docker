from app.services.redis_cache import RedisCacheService


# Redis cache session
async def get_redis_cache_session():
    try:
        print("redis connected!")
        redis_cache = RedisCacheService()
        yield redis_cache
    finally:
        print("redis disconnected!")
        await redis_cache.close()