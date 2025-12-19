import asyncio
from typing import Any, Optional

from .base import Cache


class InMemoryCache(Cache):
    def __init__(self):
        self._store: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            return self._store.get(key)

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._store[key] = value
