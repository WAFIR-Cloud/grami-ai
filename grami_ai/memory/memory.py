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

Example:
    ```python
    memory = InMemoryAbstractMemory()
    await memory.add_item("conv1", {"role": "user", "content": "Hello"})
    items = await memory.get_items("conv1")
    ```
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio


class AbstractMemory(ABC):
    """
    Abstract base class for memory management in AI agents.
    
    Defines the core interface for storing and retrieving conversation history
    and other persistent data in the Grami AI framework. This class ensures
    consistent memory management across different implementations.
    
    All memory implementations must provide:
    - Async operations
    - Conversation-based storage
    - Clear memory management
    
    Example:
        ```python
        class CustomMemory(AbstractMemory):
            async def add_item(self, conversation_id, item):
                # Custom implementation
                pass
        ```
    """

    @abstractmethod
    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to the memory for a specific conversation.
        
        This method should be implemented to store conversation items
        in a way that maintains order and allows for efficient retrieval.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
                Should be consistent across related operations.
            item (Dict[str, Any]): Item to be stored in memory.
                Typically contains 'role' and 'content' keys.
                
        Raises:
            ValueError: If the item format is invalid.
            RuntimeError: If storage operation fails.
        """
        pass

    @abstractmethod
    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items for a specific conversation.
        
        Returns items in chronological order (oldest first).
        If no items exist for the conversation, returns an empty list.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
        
        Returns:
            List[Dict[str, Any]]: List of conversation items.
                Each item is a dictionary containing at least:
                - role: str (e.g., "user", "assistant")
                - content: str
                
        Raises:
            RuntimeError: If retrieval operation fails.
        """
        pass

    @abstractmethod
    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear all items for a specific conversation.
        
        This operation is irreversible. Use with caution.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
                
        Raises:
            RuntimeError: If clear operation fails.
        """
        pass


class InMemoryAbstractMemory(AbstractMemory):
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
        _memory (Dict[str, List[Dict[str, Any]]]): Internal storage dictionary.
            Keys are conversation IDs, values are lists of conversation items.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        
        Creates an empty dictionary to store conversation histories.
        Thread-safe for async operations.
        """
        self._memory: Dict[str, List[Dict[str, Any]]] = {}

    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to the memory for a specific conversation.
        
        Creates a new conversation list if the ID doesn't exist.
        Thread-safe for concurrent access.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
            item (Dict[str, Any]): Item to be stored in memory.
                Must contain 'role' and 'content' keys.
                
        Raises:
            ValueError: If item lacks required keys.
        """
        if not isinstance(item, dict) or not all(k in item for k in ['role', 'content']):
            raise ValueError("Item must be a dict with 'role' and 'content' keys")
            
        if conversation_id not in self._memory:
            self._memory[conversation_id] = []
        
        self._memory[conversation_id].append(item)

    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items for a specific conversation.
        
        Returns a shallow copy of the items list to prevent
        external modifications to internal storage.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
        
        Returns:
            List[Dict[str, Any]]: List of conversation items in chronological order.
        """
        return self._memory.get(conversation_id, [])[:]

    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear all items for a specific conversation.
        
        Silently ignores non-existent conversation IDs.
        
        Args:
            conversation_id (str): Unique identifier for the conversation.
        """
        if conversation_id in self._memory:
            del self._memory[conversation_id]

    def __len__(self) -> int:
        """
        Get the total number of conversations stored.
        
        Returns:
            int: Number of unique conversations in memory.
        """
        return len(self._memory)

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
            f"conversations={len(self)}, "
            f"total_items={total_items})"
        )
