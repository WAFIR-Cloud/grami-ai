from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class BaseMemoryProvider(ABC):
    """Base class for memory providers in GRAMI-AI."""
    
    @abstractmethod
    async def add(self, key: str, value: Any) -> None:
        """Add an item to memory.
        
        Args:
            key: Unique identifier for the memory item
            value: The value to store
        """
        pass
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve an item from memory.
        
        Args:
            key: Key of the item to retrieve
            
        Returns:
            The stored value or None if not found
        """
        pass
    
    @abstractmethod
    async def remove(self, key: str) -> bool:
        """Remove an item from memory.
        
        Args:
            key: Key of the item to remove
            
        Returns:
            True if item was removed, False if not found
        """
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all items from memory."""
        pass
    
    @abstractmethod
    async def get_recent_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recently used items.
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of recent items with their metadata
        """
        pass
