from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

class ToolCategory(str, Enum):
    """Enumeration of tool categories."""
    CONTENT = "content"
    SEARCH = "search"
    ANALYSIS = "analysis"
    UTILITY = "utility"
    COMMUNICATION = "communication"

@dataclass
class ToolMetadata:
    """Metadata for tools in the Grami AI framework."""
    name: str
    description: str
    category: ToolCategory
    performance_score: float = 0.5
    reliability_score: float = 0.5
    tags: List[str] = field(default_factory=list)

class AsyncBaseTool(ABC):
    """
    Abstract base class for async tools in the Grami AI framework.
    
    Provides a standardized interface for tool implementation.
    """
    def __init__(self, metadata: Optional[ToolMetadata] = None):
        """
        Initialize the tool with optional metadata.
        
        Args:
            metadata: Metadata describing the tool's characteristics
        """
        self.metadata = metadata or ToolMetadata(
            name="base_tool",
            description="Base async tool",
            category=ToolCategory.UTILITY
        )
    
    @property
    def name(self) -> str:
        """
        Get the tool's name from its metadata.
        
        Returns:
            Name of the tool
        """
        return self.metadata.name
    
    @abstractmethod
    async def generate(self, *args, **kwargs) -> Any:
        """
        Abstract method for tool generation/execution.
        
        To be implemented by subclasses.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Generated or processed result
        """
        raise NotImplementedError("Subclasses must implement generate method")
    
    async def run(self, *args, **kwargs) -> Any:
        """
        Default run method that calls generate.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Result of generate method
        """
        return await self.generate(*args, **kwargs)
