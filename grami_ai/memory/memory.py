"""
Grami AI Memory Management Module

This module provides the core memory management functionality for the Grami AI framework.
It includes abstract interfaces and concrete implementations for storing and managing
conversation histories, agent states, and other persistent data.

Key Features:
- Abstract memory interface
- In-memory implementation
- Async operations
- Conversation management
- Type-safe storage
- Filtering and querying
- Unique ID generation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
import asyncio
import uuid
import time

T = TypeVar('T')

class AbstractMemory(ABC, Generic[T]):
    """
    Abstract base class for memory management in AI agents.
    
    Defines the core interface for storing and retrieving data in the Grami AI framework.
    This class ensures consistent memory management across different implementations.
    
    Type Parameters:
        T: The type of values stored in memory
    """

    @abstractmethod
    async def add_item(self, key: str, value: T) -> str:
        """
        Add an item to memory and return its unique ID.
        
        Args:
            key (str): Collection or namespace for the item
            value (T): Value to store
            
        Returns:
            str: Unique ID for the stored item
            
        Raises:
            ValueError: If value format is invalid
            RuntimeError: If storage operation fails
        """
        pass

    @abstractmethod
    async def get_items(
        self,
        key: str,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """
        Retrieve items from memory with optional filtering.
        
        Args:
            key (str): Collection or namespace to query
            filter_params: Optional filtering parameters
            
        Returns:
            List[T]: List of matching items
            
        Raises:
            RuntimeError: If retrieval operation fails
        """
        pass

    @abstractmethod
    async def update_item(self, key: str, item_id: str, value: T) -> None:
        """
        Update an existing item in memory.
        
        Args:
            key (str): Collection or namespace
            item_id (str): Unique ID of the item
            value (T): New value
            
        Raises:
            KeyError: If item_id doesn't exist
            RuntimeError: If update operation fails
        """
        pass

    @abstractmethod
    async def delete_item(self, key: str, item_id: str) -> None:
        """
        Delete an item from memory.
        
        Args:
            key (str): Collection or namespace
            item_id (str): Unique ID of the item to delete
            
        Raises:
            KeyError: If item_id doesn't exist
            RuntimeError: If deletion operation fails
        """
        pass

    def generate_id(self) -> str:
        """Generate a unique ID for a new item."""
        return f"{int(time.time())}_{uuid.uuid4().hex[:8]}"


class InMemoryAbstractMemory(AbstractMemory[Dict[str, Any]]):
    """
    In-memory implementation of AbstractMemory.
    
    Provides a lightweight, dictionary-based storage solution suitable for:
    - Development and testing
    - Short-lived applications
    - Prototype deployments
    
    Note:
        This implementation stores all data in memory and is not persistent
        across application restarts. For production use with persistence
        requirements, consider using a database-backed implementation.
    
    Attributes:
        _memory (Dict[str, Dict[str, Dict[str, Any]]]): Internal storage dictionary.
            Keys are conversation IDs, values are dictionaries of conversation items.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        
        Creates an empty dictionary to store conversation histories.
        Thread-safe for async operations.
        """
        self._memory: Dict[str, Dict[str, Dict[str, Any]]] = {}

    async def add_item(self, key: str, value: Dict[str, Any]) -> str:
        """
        Add an item to the memory for a specific conversation.
        
        Creates a new conversation list if the ID doesn't exist.
        Thread-safe for concurrent access.
        
        Args:
            key (str): Collection or namespace for the item
            value (Dict[str, Any]): Value to store
            
        Returns:
            str: Unique ID for the stored item
            
        Raises:
            ValueError: If value format is invalid
        """
        if not isinstance(value, dict):
            raise ValueError("Value must be a dictionary")
            
        item_id = self.generate_id()
        if key not in self._memory:
            self._memory[key] = {}
        
        self._memory[key][item_id] = value
        return item_id

    async def get_items(
        self,
        key: str,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve items from memory with optional filtering.
        
        Args:
            key (str): Collection or namespace to query
            filter_params: Optional filtering parameters
            
        Returns:
            List[Dict[str, Any]]: List of matching items
        """
        if key not in self._memory:
            return []
        
        items = list(self._memory[key].values())
        if filter_params:
            items = [item for item in items if all(item.get(k) == v for k, v in filter_params.items())]
        
        return items

    async def update_item(self, key: str, item_id: str, value: Dict[str, Any]) -> None:
        """
        Update an existing item in memory.
        
        Args:
            key (str): Collection or namespace
            item_id (str): Unique ID of the item
            value (Dict[str, Any]): New value
            
        Raises:
            KeyError: If item_id doesn't exist
        """
        if key not in self._memory or item_id not in self._memory[key]:
            raise KeyError(f"Item {item_id} not found in {key}")
        
        self._memory[key][item_id] = value

    async def delete_item(self, key: str, item_id: str) -> None:
        """
        Delete an item from memory.
        
        Args:
            key (str): Collection or namespace
            item_id (str): Unique ID of the item to delete
            
        Raises:
            KeyError: If item_id doesn't exist
        """
        if key not in self._memory or item_id not in self._memory[key]:
            raise KeyError(f"Item {item_id} not found in {key}")
        
        del self._memory[key][item_id]

    def __len__(self) -> int:
        """
        Get the total number of conversations stored.
        
        Returns:
            int: Number of unique conversations in memory.
        """
        return sum(len(items) for items in self._memory.values())

    def __repr__(self) -> str:
        """
        String representation of the memory object.
        
        Provides a detailed view of the memory state, including:
        - Total number of conversations
        - Number of items per conversation
        - Memory usage statistics
        
        Returns:
            str: Detailed description of memory state.
        """
        total_items = sum(len(items) for items in self._memory.values())
        return (
            f"InMemoryAbstractMemory("
            f"conversations={len(self._memory)}, "
            f"total_items={total_items})"
        )
