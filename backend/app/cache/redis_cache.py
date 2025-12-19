import json
import logging
from typing import Any, Optional

from redis.asyncio import Redis
from redis.exceptions import ConnectionError, RedisError, TimeoutError

from .base import Cache
from .in_memory import InMemoryCache

logger = logging.getLogger(__name__)


class RedisCache(Cache):
 
    def __init__(self, url: str):
        self.client = Redis.from_url(url, encoding="utf-8", decode_responses=True)
        self._fallback = InMemoryCache()
        self._use_fallback = False

    async def get(self, key: str) -> Optional[Any]:
        if self._use_fallback:
            return await self._fallback.get(key)
        try:
            data = await self.client.get(key)
            if data is None:
                return None
            return json.loads(data)
        except (ConnectionError, TimeoutError, RedisError) as exc:
            await self._enable_fallback(exc)
            return await self._fallback.get(key)

    async def set(self, key: str, value: Any) -> None:
        if self._use_fallback:
            await self._fallback.set(key, value)
            return
        try:
            await self.client.set(key, json.dumps(value))
        except (ConnectionError, TimeoutError, RedisError) as exc:
            await self._enable_fallback(exc)
            await self._fallback.set(key, value)

    async def _enable_fallback(self, exc: Exception) -> None:
    
        if not self._use_fallback:
            logger.warning("Redis unavailable, switching to in-memory cache: %s", exc)
        self._use_fallback = True
