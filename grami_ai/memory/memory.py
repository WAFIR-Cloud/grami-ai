from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import asyncio


class AbstractMemory(ABC):
    """
    Abstract base class for memory management in AI agents.
    Defines the interface for storing and retrieving conversation history.
    """

    @abstractmethod
    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to the memory for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
            item (Dict[str, Any]): Item to be stored in memory
        """
        pass

    @abstractmethod
    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
        
        Returns:
            List[Dict[str, Any]]: List of conversation items
        """
        pass

    @abstractmethod
    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear all items for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
        """
        pass


class InMemoryAbstractMemory(AbstractMemory):
    """
    In-memory implementation of AbstractMemory.
    Stores conversation history in a dictionary, suitable for short-lived or testing scenarios.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        Uses a dictionary to store conversation histories.
        """
        self._memory: Dict[str, List[Dict[str, Any]]] = {}

    async def add_item(self, conversation_id: str, item: Dict[str, Any]) -> None:
        """
        Add an item to the memory for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
            item (Dict[str, Any]): Item to be stored in memory
        """
        if conversation_id not in self._memory:
            self._memory[conversation_id] = []
        
        self._memory[conversation_id].append(item)

    async def get_items(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
        
        Returns:
            List[Dict[str, Any]]: List of conversation items
        """
        return self._memory.get(conversation_id, [])

    async def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear all items for a specific conversation.
        
        Args:
            conversation_id (str): Unique identifier for the conversation
        """
        if conversation_id in self._memory:
            del self._memory[conversation_id]

    def __len__(self) -> int:
        """
        Get the total number of conversations stored.
        
        Returns:
            int: Number of unique conversations in memory
        """
        return len(self._memory)

    def __repr__(self) -> str:
        """
        String representation of the memory.
        
        Returns:
            str: Description of stored conversations
        """
        return f"InMemoryAbstractMemory(conversations={len(self)})"
