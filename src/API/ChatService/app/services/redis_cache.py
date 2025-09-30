# services/redis_cache.py

from redis.asyncio import Redis
import json
import hashlib
from typing import Any, Optional
from app.config import settings


class RedisCacheService:
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0):
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def make_key(self, prefix: str, *args, **kwargs) -> str:
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        hashed = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{hashed}"

    async def get(self, key: str) -> Optional[Any]:
        cached = await self.redis.get(key)
        if cached is None:
            return None
        return json.loads(cached)

    async def set(self, key: str, value: Any, expire: int) -> None:
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def set(self, key: str, value: Any) -> None:
        await self.redis.set(key, json.dumps(value))

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
