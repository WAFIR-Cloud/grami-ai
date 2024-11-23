from collections import OrderedDict
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..core.base import BaseMemoryProvider

class LRUMemory(BaseMemoryProvider):
    """
    LRU (Least Recently Used) Memory implementation.
    Provides a generic memory storage that can be used with any LLM provider.
    
    The memory store is provider-agnostic and stores raw data without making
    assumptions about the format needed by specific LLM providers.
    """
    
    def __init__(self, capacity: int = 100, provider_id: Optional[str] = None):
        """Initialize LRU memory with a fixed capacity.
        
        Args:
            capacity: Maximum number of items to store (default: 100)
            provider_id: Optional provider identifier
        """
        super().__init__(provider_id)
        self.capacity = capacity
        self.cache = OrderedDict()
    
    async def store(self, key: str, value: Any) -> None:
        """Store a value in memory.
        
        Args:
            key: Storage key
            value: Value to store
        """
        # Update cache
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        
        self.cache[key] = {
            'value': value,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value from memory.
        
        Args:
            key: Storage key
        
        Returns:
            The stored value or None if not found
        """
        if key not in self.cache:
            return None
            
        entry = self.cache[key]
        self.cache.move_to_end(key)
        return entry['value']
    
    async def delete(self, key: str) -> None:
        """Delete a key from memory.
        
        Args:
            key: Storage key to delete
        """
        if key in self.cache:
            del self.cache[key]
    
    async def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """List all keys in memory.
        
        Args:
            pattern: Optional pattern to filter keys (not implemented)
            
        Returns:
            List of all keys
        """
        return list(self.cache.keys())
    
    async def clear(self) -> None:
        """Clear all items from memory."""
        self.cache.clear()
    
    async def get_size(self) -> int:
        """Get current number of items in memory.
        
        Returns:
            Number of stored items
        """
        return len(self.cache)
    
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate the configuration for the provider.
        
        Args:
            config: Configuration dictionary containing capacity
            
        Returns:
            True if configuration is valid, False otherwise
        """
        return isinstance(config.get('capacity', 100), int) and config.get('capacity', 100) > 0
