import json
from typing import Any, Dict, List, Optional
import redis.asyncio as aioredis
import uuid

from grami_ai.memory.memory import AbstractMemory


class RedisMemory(AbstractMemory[Dict[str, Any]]):
    """Redis-based implementation of AbstractMemory.
    
    Provides a persistent, scalable memory solution using Redis as the backend.
    Supports:
    - Persistent storage
    - Concurrent access
    - Filtering and querying
    - Automatic ID generation
    """
    
    def __init__(self, redis_url: str = "redis://localhost"):
        """Initialize Redis memory provider.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self) -> None:
        """Ensure Redis connection is established."""
        if not self._redis:
            self._redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )

    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.aclose()
            self._redis = None

    def generate_id(self) -> str:
        """Generate a unique ID."""
        return str(uuid.uuid4())

    async def add_item(self, key: str, value: Dict[str, Any]) -> str:
        """Add an item to Redis and return its ID.
        
        Args:
            key: Collection or namespace
            value: Value to store
            
        Returns:
            str: Unique ID for the stored item
        """
        await self.connect()
        
        # Generate unique ID
        item_id = self.generate_id()
        
        # Store item in Redis hash
        item_key = f"{key}:{item_id}"
        await self._redis.hset(item_key, mapping=value)
        
        # Add to collection set
        await self._redis.sadd(f"{key}:items", item_id)
        
        return item_id

    async def get_items(
        self,
        key: str,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get items from Redis with optional filtering.
        
        Args:
            key: Collection or namespace
            filter_params: Optional filtering parameters
            
        Returns:
            List[Dict[str, Any]]: List of matching items
        """
        await self.connect()
        
        # Get all item IDs for the collection
        item_ids = await self._redis.smembers(f"{key}:items")
        if not item_ids:
            return []
        
        # Get all items
        items = []
        for item_id in item_ids:
            item_key = f"{key}:{item_id}"
            item = await self._redis.hgetall(item_key)
            if item:  # Only include non-empty items
                if filter_params:
                    # Apply filters
                    if all(item.get(k) == str(v) for k, v in filter_params.items()):
                        items.append(item)
                else:
                    items.append(item)
        
        return items

    async def update_item(self, key: str, item_id: str, value: Dict[str, Any]) -> None:
        """Update an existing item in Redis.
        
        Args:
            key: Collection or namespace
            item_id: Unique ID of the item
            value: New value
            
        Raises:
            KeyError: If item doesn't exist
        """
        await self.connect()
        
        item_key = f"{key}:{item_id}"
        if not await self._redis.exists(item_key):
            raise KeyError(f"Item {item_id} not found in {key}")
        
        # Update the hash
        await self._redis.delete(item_key)  # Clear existing fields
        await self._redis.hset(item_key, mapping=value)

    async def delete_item(self, key: str, item_id: str) -> None:
        """Delete an item from Redis.
        
        Args:
            key: Collection or namespace
            item_id: Unique ID of the item
            
        Raises:
            KeyError: If item doesn't exist
        """
        await self.connect()
        
        item_key = f"{key}:{item_id}"
        if not await self._redis.exists(item_key):
            raise KeyError(f"Item {item_id} not found in {key}")
        
        # Remove from collection set and delete hash
        await self._redis.srem(f"{key}:items", item_id)
        await self._redis.delete(item_key)
