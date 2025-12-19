import logging

from .base import Cache
from .redis_cache import RedisCache
from .in_memory import InMemoryCache
from ..shared.config import settings

logger = logging.getLogger(__name__)


def get_cache() -> Cache:
    if settings.redis_url:
        try:
            return RedisCache(settings.redis_url)
        except Exception:
            logger.warning("Redis unavailable, falling back to in-memory cache")
            return InMemoryCache()
    return InMemoryCache()
