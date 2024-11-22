"""
Grami AI Core Agent Module

This module provides the core agent implementation for the Grami AI framework.
It enables easy creation of AI agents with different capabilities and interfaces.
"""

import asyncio
from typing import List, Optional, Any, Dict, Callable, Union, Type
from enum import Enum

from grami_ai.core.memory import AsyncMemory, AsyncInMemoryMemory, AsyncRedisMemory
from grami_ai.core.config import settings, Settings
from grami_ai.core.logger import logger, LoggingContext
from grami_ai.llms.base import BaseLLMProvider
from grami_ai.tools.base import AsyncBaseTool
from grami_ai.core.interfaces import AgentInterface, WebSocketInterface, KafkaConsumerInterface

class MemoryType(str, Enum):
    """Supported memory backends"""
    REDIS = "redis"
    IN_MEMORY = "in_memory"
    IN_MEMORY_TYPE = "in_memory_type"

class InterfaceType(str, Enum):
    """Supported agent interfaces"""
    WEBSOCKET = "websocket"
    KAFKA_CONSUMER = "kafka_consumer"

class LLMType(str, Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    OPENAI = "openai"

class AsyncAgent:
    """
    Enhanced Async AI Agent Framework
    
    Features:
    - Factory-style creation
    - Multiple interface support
    - Pluggable memory backends
    - Automatic tool selection
    - LLM-driven decision making
    """
    def __init__(
        self,
        name: str,
        llm: BaseLLMProvider,
        memory: AsyncMemory,
        interface: AgentInterface,
        tools: Optional[List[AsyncBaseTool]] = None,
        system_instruction: Optional[str] = None,
        config: Optional[Settings] = None
    ):
        self.name = name
        self.llm = llm
        self.memory = memory
        self.interface = interface
        self.tools = tools or []
        self.system_instruction = system_instruction or settings.default_system_instruction
        self.config = config or settings
        
        # Initialize interface
        # self.interface.initialize(self)
    
    @classmethod
    async def create(
        cls,
        name: str,
        llm: Union[str, BaseLLMProvider],
        memory: Union[str, AsyncMemory] = MemoryType.IN_MEMORY,
        interface: Union[str, AgentInterface] = InterfaceType.WEBSOCKET,
        tools: Optional[List[Union[str, AsyncBaseTool]]] = None,
        system_instruction: Optional[str] = None,
        config: Optional[Settings] = None,
        **kwargs
    ) -> "AsyncAgent":
        """
        Create an agent with the specified configuration.
        
        Args:
            name: Agent name
            llm: LLM provider name or instance
            memory: Memory backend name or instance
            interface: Interface type or instance
            tools: List of tool names or instances
            system_instruction: Custom system instruction
            config: Custom settings
            **kwargs: Additional configuration
            
        Returns:
            Configured AsyncAgent instance
        """
        # Resolve LLM provider
        if isinstance(llm, str):
            llm = await cls._get_llm_provider(llm, **kwargs)
            
        # Resolve memory backend
        if isinstance(memory, str):
            memory = await cls._get_memory_backend(memory, **kwargs)
            
        # Resolve interface
        if isinstance(interface, str):
            interface = await cls._get_interface(interface, **kwargs)
            
        # Resolve tools
        if tools:
            resolved_tools = await cls._get_tools(tools, **kwargs)
        else:
            resolved_tools = await cls._get_default_tools()
            
        return cls(
            name=name,
            llm=llm,
            memory=memory,
            interface=interface,
            tools=resolved_tools,
            system_instruction=system_instruction,
            config=config
        )
    
    @staticmethod
    async def _get_llm_provider(name: str, **kwargs) -> BaseLLMProvider:
        """Get LLM provider by name"""
        if name == LLMType.GEMINI:
            from grami_ai.llms.gemini_llm import GeminiLLMProvider
            return GeminiLLMProvider(**kwargs)
        elif name == LLMType.OPENAI:
            from grami_ai.llms.openai_llm import OpenAILLMProvider
            return OpenAILLMProvider(**kwargs)
        raise ValueError(f"Unsupported LLM provider: {name}")

    @staticmethod
    async def _get_memory_backend(name: str, **kwargs) -> AsyncMemory:
        """Get memory backend by name"""
        if name == MemoryType.REDIS:
            return AsyncRedisMemory(**kwargs)
        elif name == MemoryType.IN_MEMORY:
            return AsyncInMemoryMemory()
        elif name == MemoryType.IN_MEMORY_TYPE:
            return AsyncInMemoryMemory()
        raise ValueError(f"Unsupported memory type: {name}")
    
    @staticmethod
    async def _get_interface(name: str, **kwargs) -> AgentInterface:
        """Get interface by name"""
        if name == InterfaceType.WEBSOCKET:
            return WebSocketInterface(**kwargs)
        elif name == InterfaceType.KAFKA_CONSUMER:
            return KafkaConsumerInterface(**kwargs)
        raise ValueError(f"Unsupported interface type: {name}")
    
    @staticmethod
    async def _get_tools(
        tools: List[Union[str, AsyncBaseTool]], 
        **kwargs
    ) -> List[AsyncBaseTool]:
        """Get tools by name or use provided instances"""
        resolved_tools = []
        for tool in tools:
            if isinstance(tool, str):
                # Resolve tool by name
                tool_instance = await AsyncAgent._resolve_tool(tool, **kwargs)
                resolved_tools.append(tool_instance)
            else:
                resolved_tools.append(tool)
        return resolved_tools
    
    @staticmethod
    async def _get_default_tools() -> List[AsyncBaseTool]:
        """Get default tools (communication, etc.)"""
        # Implementation for default tools
        pass
    
    @staticmethod
    async def _resolve_tool(name: str, **kwargs) -> AsyncBaseTool:
        """Resolve tool by name"""
        # Implementation for tool resolution
        pass
    
    async def process(self, message: Any) -> Any:
        """
        Process incoming message using LLM and tools
        
        The LLM decides:
        1. Which tools to use
        2. How to respond
        3. When to use memory
        4. How to format response
        """
        # Implementation for LLM-driven message processing
        pass
    
    async def start(self) -> None:
        """Start the agent's interface."""
        if self.interface:
            await self.interface.initialize(self)
            await self.interface.start()

    async def stop(self) -> None:
        """Stop the agent's interface."""
        if self.interface:
            await self.interface.stop()
