import json
import redis.asyncio as aioredis
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..memory.base import BaseMemoryProvider

class RedisMemory(BaseMemoryProvider):
    """
    Async Redis-based Memory implementation.
    Provides a distributed memory storage that can be used with any LLM provider.
    
    The memory store is provider-agnostic and stores raw data without making
    assumptions about the format needed by specific LLM providers.
    """
    
    def __init__(
        self, 
        host: str = 'localhost', 
        port: int = 6379, 
        db: int = 0, 
        capacity: int = 100, 
        provider_id: Optional[str] = None
    ):
        """Initialize Redis memory with connection parameters.
        
        Args:
            host: Redis server host (default: localhost)
            port: Redis server port (default: 6379)
            db: Redis database number (default: 0)
            capacity: Maximum number of items to store (default: 100)
            provider_id: Optional provider identifier
        """
        self.capacity = capacity
        self.memory_key_prefix = f"grami_memory:{provider_id or 'default'}:"
        self._host = host
        self._port = port
        self._db = db
        self._redis_client = None
    
    async def _get_redis_client(self):
        """Lazily initialize and return Redis client."""
        if self._redis_client is None:
            self._redis_client = await aioredis.from_url(
                f"redis://{self._host}:{self._port}/{self._db}",
                encoding="utf-8",
                decode_responses=True
            )
        return self._redis_client
    
    async def add(self, key: str, value: Any) -> None:
        """Store a value in Redis memory.
        
        Args:
            key: Storage key
            value: Value to store
        """
        redis = await self._get_redis_client()
        
        # Serialize the value with timestamp
        serialized_value = json.dumps({
            'value': value,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        # Use a sorted set to maintain order and limit capacity
        await redis.zadd(
            f"{self.memory_key_prefix}memory_index", 
            {key: datetime.now(timezone.utc).timestamp()}
        )
        
        # Store the actual value
        await redis.hset(
            f"{self.memory_key_prefix}memory", 
            key, 
            serialized_value
        )
        
        # Trim to capacity
        await self._trim_to_capacity()
    
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from Redis memory.
        
        Args:
            key: Storage key
        
        Returns:
            The stored value or None if not found
        """
        redis = await self._get_redis_client()
        
        # Retrieve the serialized value
        serialized_value = await redis.hget(
            f"{self.memory_key_prefix}memory", 
            key
        )
        
        if serialized_value:
            # Deserialize and return the value
            memory_item = json.loads(serialized_value)
            return memory_item['value']
        
        return None
    
    async def remove(self, key: str) -> bool:
        """Remove an item from Redis memory.
        
        Args:
            key: Key of the item to remove
            
        Returns:
            True if item was removed, False if not found
        """
        redis = await self._get_redis_client()
        
        # Remove from memory hash
        removed_count = await redis.hdel(
            f"{self.memory_key_prefix}memory", 
            key
        )
        
        # Remove from sorted set
        await redis.zrem(
            f"{self.memory_key_prefix}memory_index", 
            key
        )
        
        return bool(removed_count)
    
    async def clear(self) -> None:
        """Clear all items from Redis memory."""
        redis = await self._get_redis_client()
        await redis.delete(
            f"{self.memory_key_prefix}memory", 
            f"{self.memory_key_prefix}memory_index"
        )
    
    async def get_recent_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recently used items from Redis memory.
        
        Args:
            limit: Maximum number of items to return
        
        Returns:
            List of recent memory items
        """
        redis = await self._get_redis_client()
        
        # Get recent keys from sorted set
        recent_keys = await redis.zrevrange(
            f"{self.memory_key_prefix}memory_index", 
            0, 
            limit - 1
        )
        
        # Retrieve full details for these keys
        recent_items = []
        for key in recent_keys:
            serialized_value = await redis.hget(
                f"{self.memory_key_prefix}memory", 
                key
            )
            
            if serialized_value:
                memory_item = json.loads(serialized_value)
                recent_items.append({
                    'key': key,
                    **memory_item
                })
        
        return recent_items
    
    async def list_contents(self) -> List[Dict[str, Any]]:
        """List all contents in memory.
        
        Returns:
            List of memory contents with key, value, and timestamp
        """
        redis = await self._get_redis_client()
        
        # Get all keys from memory hash
        keys = await redis.hkeys(f"{self.memory_key_prefix}memory")
        
        # Retrieve details for each key
        contents = []
        for key in keys:
            serialized_value = await redis.hget(
                f"{self.memory_key_prefix}memory", 
                key
            )
            
            if serialized_value:
                memory_item = json.loads(serialized_value)
                contents.append({
                    'key': key,
                    **memory_item
                })
        
        return contents
    
    async def _trim_to_capacity(self) -> None:
        """Trim memory to the specified capacity."""
        redis = await self._get_redis_client()
        
        # Get total number of items
        total_items = await redis.zcard(
            f"{self.memory_key_prefix}memory_index"
        )
        
        # If over capacity, remove oldest items
        if total_items > self.capacity:
            # Get keys to remove
            keys_to_remove = await redis.zrange(
                f"{self.memory_key_prefix}memory_index", 
                0, 
                total_items - self.capacity - 1
            )
            
            # Remove from memory hash
            if keys_to_remove:
                await redis.hdel(
                    f"{self.memory_key_prefix}memory", 
                    *keys_to_remove
                )
                
                # Remove from sorted set
                await redis.zrem(
                    f"{self.memory_key_prefix}memory_index", 
                    *keys_to_remove
                )
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._get_redis_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None
    
    async def store(self, key: str, value: Any) -> None:
        """Store a value in Redis memory.
        
        Args:
            key: Storage key
            value: Value to store
        """
        await self.add(key, value)
    
    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value from Redis memory.
        
        Args:
            key: Storage key
        
        Returns:
            The stored value or None if not found
        """
        return await self.get(key)
    
    async def delete(self, key: str) -> None:
        """Delete a key from Redis memory.
        
        Args:
            key: Storage key to delete
        """
        await self.remove(key)
    
    async def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """List all keys in memory.
        
        Args:
            pattern: Optional pattern to filter keys (not implemented)
            
        Returns:
            List of all keys
        """
        redis = await self._get_redis_client()
        return await redis.hkeys(f"{self.memory_key_prefix}memory")
    
    async def get_size(self) -> int:
        """Get current number of items in memory.
        
        Returns:
            Number of stored items
        """
        redis = await self._get_redis_client()
        return await redis.hlen(f"{self.memory_key_prefix}memory")
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate the configuration for the provider.
        
        Args:
            config: Configuration dictionary containing connection details
            
        Returns:
            True if configuration is valid, False otherwise
        """
        return (
            isinstance(config.get('host', 'localhost'), str) and
            isinstance(config.get('port', 6379), int) and
            isinstance(config.get('db', 0), int) and
            isinstance(config.get('capacity', 100), int) and
            config.get('capacity', 100) > 0
        )
