import abc
import asyncio
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum, auto

from grami_ai.core.logger import AsyncLogger
from grami_ai.core.exceptions import ToolConfigurationError, ToolExecutionError

class ToolCategory(Enum):
    """
    Comprehensive categorization of tools
    """
    SEARCH = auto()
    COMPUTATION = auto()
    COMMUNICATION = auto()
    DATA_PROCESSING = auto()
    SYSTEM_INTERACTION = auto()
    EXTERNAL_API = auto()
    MACHINE_LEARNING = auto()
    VISUALIZATION = auto()
    CUSTOM = auto()

@dataclass
class ToolMetadata:
    """
    Comprehensive metadata for tools
    """
    name: str
    description: str
    category: ToolCategory
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    performance_score: float = 0.5
    reliability_score: float = 0.5
    required_env_vars: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class AsyncBaseTool(abc.ABC):
    """
    Abstract base class for async tools in the Grami AI framework
    """
    def __init__(
        self, 
        metadata: Optional[ToolMetadata] = None,
        logger: Optional[AsyncLogger] = None
    ):
        """
        Initialize a base tool
        
        Args:
            metadata: Tool metadata
            logger: Optional custom logger
        """
        self.metadata = metadata or self._generate_default_metadata()
        self.logger = logger or AsyncLogger()
    
    def _generate_default_metadata(self) -> ToolMetadata:
        """
        Generate default metadata based on class information
        
        Returns:
            Generated ToolMetadata instance
        """
        return ToolMetadata(
            name=self.__class__.__name__,
            description=self._generate_default_description(),
            category=ToolCategory.CUSTOM
        )
    
    def _generate_default_description(self) -> str:
        """
        Generate a default description based on class name
        
        Returns:
            Generated description string
        """
        return f"A tool for performing {self.__class__.__name__.replace('Tool', '').lower()} operations"
    
    @abc.abstractmethod
    async def execute(
        self, 
        task: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute the tool asynchronously
        
        Args:
            task: Primary task or query
            context: Additional contextual information
        
        Returns:
            Result of tool execution
        
        Raises:
            ToolExecutionError: If tool execution fails
        """
        pass
    
    @abc.abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """
        Define tool-specific parameters
        
        Returns:
            A dictionary of parameter definitions
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tool metadata to a dictionary
        
        Returns:
            Dictionary representation of tool metadata
        """
        return {
            "name": self.metadata.name,
            "description": self.metadata.description,
            "category": self.metadata.category.name,
            "version": self.metadata.version,
            "performance_score": self.metadata.performance_score,
            "reliability_score": self.metadata.reliability_score
        }

class ToolRegistry:
    """
    Centralized tool management system
    """
    def __init__(self):
        """Initialize tool registry"""
        self._tools: Dict[str, AsyncBaseTool] = {}
        self._category_map: Dict[ToolCategory, List[str]] = {}
    
    def register_tool(self, tool: AsyncBaseTool):
        """
        Register a tool in the registry
        
        Args:
            tool: Tool instance to register
        
        Raises:
            ValueError: If tool with same name already exists
        """
        name = tool.metadata.name
        category = tool.metadata.category
        
        if name in self._tools:
            raise ValueError(f"Tool {name} already registered")
        
        self._tools[name] = tool
        
        # Update category map
        if category not in self._category_map:
            self._category_map[category] = []
        self._category_map[category].append(name)
    
    def get_tool(self, name: str) -> AsyncBaseTool:
        """
        Retrieve a tool by name
        
        Args:
            name: Tool name
        
        Returns:
            Registered tool instance
        
        Raises:
            KeyError: If tool not found
        """
        return self._tools[name]
    
    def list_tools(
        self, 
        category: Optional[ToolCategory] = None
    ) -> List[Dict[str, Any]]:
        """
        List available tools, optionally filtered by category
        
        Args:
            category: Optional tool category to filter
        
        Returns:
            List of tool metadata dictionaries
        """
        if category:
            tool_names = self._category_map.get(category, [])
            return [self._tools[name].to_dict() for name in tool_names]
        
        return [tool.to_dict() for tool in self._tools.values()]

# Global tool registry instance
tool_registry = ToolRegistry()
