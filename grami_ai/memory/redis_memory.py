import json
import redis.asyncio as aioredis
from typing import Any, Dict, List, Optional

from grami_ai.memory.memory import AbstractMemory


class RedisMemory(AbstractMemory):
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self):
        if not self._redis:
            self._redis = await aioredis.from_url(self.redis_url)

    async def close(self):
        if self._redis:
            await self._redis.aclose()
            self._redis = None

    async def add_item(self, chat_id: str, item: Dict[str, Any]) -> None:
        await self.connect()
        serialized_item = json.dumps(item)
        await self._redis.lpush(chat_id, serialized_item)

    async def get_items(self, chat_id: str) -> List[Dict[str, Any]]:
        await self.connect()
        items = await self._redis.lrange(chat_id, 0, -1)
        return [json.loads(item) for item in items]

    async def clear_items(self, chat_id: str) -> None:
        await self.connect()
        await self._redis.delete(chat_id)
