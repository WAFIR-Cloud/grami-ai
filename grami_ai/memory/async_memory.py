import asyncio
import json
import pickle
from typing import Any, Dict, List, Optional, TypeVar

from grami_ai.memory.memory import AbstractMemory, InMemoryAbstractMemory

T = TypeVar('T')

class AsyncRedisMemory(AbstractMemory):
    """
    Async Redis-based memory implementation
    
    Supports:
    - Async storage and retrieval
    - Conversation history management
    - Connection pooling
    """
    
    def __init__(
        self, 
        redis_url: str = "redis://localhost:6379/0"
    ):
        """
        Initialize Redis memory provider
        
        Args:
            redis_url: Redis connection URL
        """
        import redis.asyncio as aioredis
        
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Establish Redis connection"""
        import redis.asyncio as aioredis
        
        if not self._redis:
            self._redis = await aioredis.from_url(self.redis_url)
    
    async def close(self):
        """Close Redis connection"""
        if self._redis:
            await self._redis.aclose()
            self._redis = None
    
    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to conversation memory
        
        Args:
            conversation_id: Unique conversation identifier
            item: Item to store
        """
        await self.connect()
        serialized_item = json.dumps(item)
        await self._redis.lpush(conversation_id, serialized_item)
    
    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve conversation items
        
        Args:
            conversation_id: Unique conversation identifier
        
        Returns:
            List of conversation items
        """
        await self.connect()
        items = await self._redis.lrange(conversation_id, 0, -1)
        return [json.loads(item) for item in items]
    
    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear conversation items
        
        Args:
            conversation_id: Unique conversation identifier
        """
        await self.connect()
        await self._redis.delete(conversation_id)

class AsyncInMemoryMemory(InMemoryAbstractMemory):
    """
    Enhanced async in-memory memory with additional features
    
    Supports:
    - Async storage and retrieval
    - Thread-safe operations
    - Configurable memory limits
    """
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize in-memory storage
        
        Args:
            max_size: Optional maximum number of items to store
        """
        super().__init__()
        self._max_size = max_size
        self._lock = asyncio.Lock()
    
    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to conversation memory
        
        Args:
            conversation_id: Unique conversation identifier
            item: Item to store
        """
        async with self._lock:
            if not hasattr(self, '_conversations'):
                self._conversations = {}
            
            if conversation_id not in self._conversations:
                self._conversations[conversation_id] = []
            
            if self._max_size and len(self._conversations[conversation_id]) >= self._max_size:
                # Remove oldest item if max size reached
                self._conversations[conversation_id].pop(0)
            
            self._conversations[conversation_id].append(item)
    
    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve conversation items
        
        Args:
            conversation_id: Unique conversation identifier
        
        Returns:
            List of conversation items
        """
        async with self._lock:
            return self._conversations.get(conversation_id, [])
    
    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear conversation items
        
        Args:
            conversation_id: Unique conversation identifier
        """
        async with self._lock:
            if hasattr(self, '_conversations'):
                self._conversations.pop(conversation_id, None)
