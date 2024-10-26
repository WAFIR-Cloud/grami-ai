import asyncio
import json
from typing import Any, List

from grami_ai.state import RedisState, state


class RedisMemory:
    """
    A higher-level wrapper for managing conversation history or other
    memory-like data in Redis, using the RedisState class.
    """

    def __init__(
            self,
            redis_url: str = None,  # Optional: Override the default Redis URL
            history_limit: int = 100,
            key_prefix: str = "memory",  # Optional: Customize the key prefix
    ):
        """
        Initializes RedisMemory.

        Args:
            redis_url: Optional Redis URL to override the default from RedisState.
            history_limit: Maximum number of items to store.
            key_prefix: Prefix for Redis keys.
        """
        self.history_limit = history_limit
        self.key_prefix = key_prefix
        self.state = RedisState(redis_url=redis_url) if redis_url else state  # Use provided URL or global state

    async def add_item(self, chat_id: str, item: Any):
        """
        Adds an item to the memory.

        Args:
            chat_id: Unique identifier for the conversation or context.
            item: The item to add to the memory.
        """
        key = f"{self.key_prefix}:{chat_id}"
        await self.state.lpush(key, json.dumps(item).encode())  # Encode to bytes before lpush
        await self.state.ltrim(key, 0, self.history_limit - 1)  # Trim the list

    async def get_items(self, chat_id: str, limit: int = 10) -> List[Any]:
        """
        Retrieves items from the memory.

        Args:
            chat_id: Unique identifier for the conversation or context.
            limit: Maximum number of items to retrieve.

        Returns:
            A list of items from the memory.
        """
        key = f"{self.key_prefix}:{chat_id}"
        items = await self.state.lrange(key, 0, limit - 1)
        return [json.loads(item.decode()) for item in items]  # Decode from bytes after lrange
