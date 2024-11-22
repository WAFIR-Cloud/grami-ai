import abc
import asyncio
from typing import (
    Any, 
    Dict, 
    List, 
    Optional, 
    TypeVar, 
    Generic, 
    Union
)
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from grami_ai.core.logger import AsyncLogger

class MemoryItemType(Enum):
    """
    Categorization of memory items for better organization
    """
    MESSAGE = auto()
    SYSTEM_INSTRUCTION = auto()
    TOOL_RESULT = auto()
    USER_CONTEXT = auto()
    EXTERNAL_DATA = auto()
    ERROR_LOG = auto()
    CUSTOM = auto()

@dataclass
class MemoryItem:
    """
    Comprehensive memory item representation
    """
    content: Any
    type: MemoryItemType
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memory item to a dictionary for serialization
        
        Returns:
            Serializable dictionary representation
        """
        return {
            "content": str(self.content),  # Ensure string representation
            "type": self.type.name,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

T = TypeVar('T')

class AsyncMemory(Generic[T], abc.ABC):
    """
    Abstract base class for async memory management
    
    Supports generic type T for flexible memory item handling
    """
    def __init__(
        self, 
        max_items: Optional[int] = 100,
        max_age: Optional[timedelta] = timedelta(hours=24),
        logger: Optional[AsyncLogger] = None
    ):
        """
        Initialize memory with configurable constraints
        
        Args:
            max_items: Maximum number of items to store
            max_age: Maximum age of stored items
            logger: Optional custom logger
        """
        self._max_items = max_items
        self._max_age = max_age
        self._logger = logger or AsyncLogger()
        self._memory: List[MemoryItem] = []
    
    async def add_item(
        self, 
        content: T, 
        item_type: MemoryItemType = MemoryItemType.MESSAGE,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add an item to memory with type and optional metadata
        
        Args:
            content: Memory item content
            item_type: Categorization of memory item
            metadata: Additional contextual information
        """
        # Prune old items before adding new one
        await self._prune_memory()
        
        # Create memory item
        memory_item = MemoryItem(
            content=content, 
            type=item_type, 
            metadata=metadata or {}
        )
        
        # Add item to memory
        self._memory.append(memory_item)
        
        # Log memory addition
        await self._logger.debug(
            "Memory item added", 
            {"type": item_type.name, "metadata": metadata}
        )
    
    async def _prune_memory(self) -> None:
        """
        Remove items exceeding max_items or max_age constraints
        """
        current_time = datetime.now()
        
        # Remove items older than max_age
        if self._max_age:
            self._memory = [
                item for item in self._memory 
                if current_time - item.timestamp <= self._max_age
            ]
        
        # Truncate to max_items if specified
        if self._max_items:
            self._memory = self._memory[-self._max_items:]
    
    async def get_memory_items(
        self, 
        item_type: Optional[MemoryItemType] = None,
        limit: Optional[int] = None
    ) -> List[MemoryItem]:
        """
        Retrieve memory items, optionally filtered
        
        Args:
            item_type: Optional filter by memory item type
            limit: Optional limit on number of items returned
        
        Returns:
            List of memory items
        """
        filtered_items = self._memory
        
        # Filter by type if specified
        if item_type:
            filtered_items = [
                item for item in filtered_items 
                if item.type == item_type
            ]
        
        # Apply limit if specified
        if limit:
            filtered_items = filtered_items[-limit:]
        
        return filtered_items
    
    async def clear_memory(self) -> None:
        """
        Clear all memory items
        """
        self._memory.clear()
        await self._logger.info("Memory cleared")
    
    @abc.abstractmethod
    async def prepare_context_for_llm(self) -> Union[List[Dict[str, Any]], str]:
        """
        Prepare memory context for specific LLM
        
        Abstract method to be implemented by subclasses
        
        Returns:
            Formatted context ready for LLM input
        """
        pass
    
    def __len__(self) -> int:
        """
        Get current number of memory items
        
        Returns:
            Number of memory items
        """
        return len(self._memory)

class AsyncInMemoryMemory(AsyncMemory[Any]):
    """
    In-memory implementation of AsyncMemory
    """
    async def prepare_context_for_llm(self) -> List[Dict[str, Any]]:
        """
        Prepare memory items as a list of chat messages
        
        Returns:
            List of message dictionaries
        """
        context = []
        memory_items = await self.get_memory_items()
        
        for item in memory_items:
            if item.type == MemoryItemType.MESSAGE:
                context.append({
                    "role": item.metadata.get("role", "user"),
                    "content": str(item.content)
                })
            elif item.type == MemoryItemType.SYSTEM_INSTRUCTION:
                context.append({
                    "role": "system",
                    "content": str(item.content)
                })
        
        return context

class AsyncRedisMemory(AsyncMemory[Any]):
    """
    Redis-backed implementation of AsyncMemory
    """
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        namespace: str = "grami_memory",
        **kwargs
    ):
        """
        Initialize Redis memory
        
        Args:
            redis_url: Redis connection URL
            namespace: Namespace for Redis keys
            **kwargs: Additional arguments passed to AsyncMemory
        """
        super().__init__(**kwargs)
        import redis.asyncio as redis
        self._redis = redis.from_url(redis_url)
        self._namespace = namespace
    
    async def add_item(
        self,
        content: Any,
        item_type: MemoryItemType = MemoryItemType.MESSAGE,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add item to Redis memory
        """
        memory_item = MemoryItem(
            content=content,
            type=item_type,
            metadata=metadata or {}
        )
        
        # Store in Redis
        key = f"{self._namespace}:{memory_item.timestamp.isoformat()}"
        await self._redis.set(key, str(memory_item.to_dict()))
        
        # Set expiry if max_age is specified
        if self._max_age:
            await self._redis.expire(key, int(self._max_age.total_seconds()))
    
    async def get_memory_items(
        self,
        item_type: Optional[MemoryItemType] = None,
        limit: Optional[int] = None
    ) -> List[MemoryItem]:
        """
        Retrieve items from Redis memory
        """
        import json
        from datetime import datetime
        
        # Get all keys in namespace
        keys = await self._redis.keys(f"{self._namespace}:*")
        items = []
        
        for key in keys:
            value = await self._redis.get(key)
            if value:
                try:
                    data = json.loads(value)
                    item = MemoryItem(
                        content=data["content"],
                        type=MemoryItemType[data["type"]],
                        timestamp=datetime.fromisoformat(data["timestamp"]),
                        metadata=data["metadata"]
                    )
                    items.append(item)
                except (json.JSONDecodeError, KeyError) as e:
                    await self._logger.error(f"Error decoding memory item: {e}")
        
        # Sort by timestamp
        items.sort(key=lambda x: x.timestamp)
        
        # Filter by type if specified
        if item_type:
            items = [item for item in items if item.type == item_type]
        
        # Apply limit if specified
        if limit:
            items = items[-limit:]
        
        return items
    
    async def prepare_context_for_llm(self) -> List[Dict[str, Any]]:
        """
        Prepare Redis memory items as chat messages
        """
        context = []
        memory_items = await self.get_memory_items()
        
        for item in memory_items:
            if item.type == MemoryItemType.MESSAGE:
                context.append({
                    "role": item.metadata.get("role", "user"),
                    "content": str(item.content)
                })
            elif item.type == MemoryItemType.SYSTEM_INSTRUCTION:
                context.append({
                    "role": "system",
                    "content": str(item.content)
                })
        
        return context
    
    async def clear_memory(self) -> None:
        """
        Clear all Redis memory items in namespace
        """
        keys = await self._redis.keys(f"{self._namespace}:*")
        if keys:
            await self._redis.delete(*keys)
        await self._logger.info("Redis memory cleared")
