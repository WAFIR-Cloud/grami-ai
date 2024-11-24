"""
Base agent implementation for the GRAMI framework.

This module provides the foundation for all agent implementations in GRAMI.
"""

from typing import List, Dict, Any, Optional, Union, Callable
from ..core.base import BaseLLMProvider, BaseMemoryProvider, BaseCommunicationProvider, BaseTool
import logging
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all GRAMI agents.
    
    This class defines the core interface that all agent implementations must follow.
    It provides basic functionality for agent initialization, message handling,
    and tool management.
    """
    
    def __init__(
        self,
        name: str,
        llm: BaseLLMProvider,
        memory: Optional[BaseMemoryProvider] = None,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Callable]] = None,
        communication_interface: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a base agent with core capabilities.
        
        Args:
            name: Unique identifier for the agent
            llm: Language model provider for generating responses
            memory: Optional memory provider for conversation history
            system_instructions: Optional system-level instructions
            tools: Optional list of tool functions
            communication_interface: Optional communication interface
            config: Additional configuration parameters
        """
        self.name = name
        self.llm = llm
        self.memory = memory
        self.system_instructions = system_instructions
        self.communication_interface = communication_interface
        self.config = config or {}
        
        # Set up logging with proper naming
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{name}")
        
        # Initialize tools if provided
        if tools:
            self._register_tools(tools)
            
        # Set system instructions if supported
        if system_instructions and hasattr(self.llm, '_system_prompt'):
            self.llm._system_prompt = system_instructions
    
    def _register_tools(self, tools: List[Callable]) -> None:
        """
        Register tools with the LLM provider.
        
        Args:
            tools: List of callable tools to register
        """
        if hasattr(self.llm, 'tools'):
            self.llm.tools = tools
        else:
            self.logger.warning(f"LLM provider {type(self.llm).__name__} does not support tools")
    
    @abstractmethod
    async def send_message(
        self,
        message: Union[str, Dict[str, str]],
        context: Optional[Dict] = None
    ) -> str:
        """
        Send a message and get a response.
        
        Args:
            message: Message content (string or role-content dictionary)
            context: Optional context information
            
        Returns:
            Response from the agent
        """
        pass
    
    def _normalize_message(self, message: Union[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Normalize message format to standard dictionary format.
        
        Args:
            message: Raw message (string or dictionary)
            
        Returns:
            Normalized message dictionary
        """
        if isinstance(message, str):
            return {"role": "user", "content": message}
        return message
    
    async def add_tool(self, tool: Callable) -> None:
        """
        Add a new tool to the agent's capabilities.
        
        Args:
            tool: Callable tool function to add
        """
        if hasattr(self.llm, 'tools'):
            current_tools = getattr(self.llm, 'tools', [])
            current_tools.append(tool)
            self.llm.tools = current_tools
        else:
            self.logger.warning(f"LLM provider {type(self.llm).__name__} does not support tools")
