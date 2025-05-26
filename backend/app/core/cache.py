import redis.asyncio as redis
import json
from typing import Optional, Any
from app.config import settings
import structlog

logger = structlog.get_logger()

class RedisCache:
    def __init__(self, url: str):
        self.redis = redis.from_url(url, decode_responses=True)
    
    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Cache get error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        try:
            ttl = ttl or settings.CACHE_TTL
            serialized = json.dumps(value, ensure_ascii=False)
            await self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error("Cache set error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error("Cache delete error", key=key, error=str(e))
            return False
    
    async def ping(self) -> bool:
        try:
            await self.redis.ping()
            return True
        except Exception:
            return False
    
    async def close(self):
        await self.redis.close()

redis_client = RedisCache(settings.REDIS_URL)
