from typing import List, Dict, Any, Optional, AsyncGenerator, Union, Callable
from .core.base import BaseLLMProvider, BaseMemoryProvider, BaseCommunicationProvider, BaseTool
import logging
import asyncio
from datetime import datetime

class Agent:
    """
    Core Agent class representing an AI agent in the Grami framework.
    
    This class provides a flexible and extensible implementation for creating 
    AI agents with customizable capabilities.
    """
    
    def __init__(
        self, 
        name: str,
        role: str,
        llm_provider: BaseLLMProvider,
        memory_provider: Optional[BaseMemoryProvider] = None,
        communication_provider: Optional[BaseCommunicationProvider] = None,
        tools: Optional[List[BaseTool]] = None,
        initial_context: Optional[List[Dict[str, str]]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an AI Agent with specified providers and configurations.
        
        :param name: Unique name for the agent
        :param role: Role or purpose of the agent
        :param llm_provider: Language Model Provider for generating responses
        :param memory_provider: Optional memory management provider
        :param communication_provider: Optional communication interface provider
        :param tools: Optional list of tools/functions the agent can use
        :param initial_context: Initial conversation context with role-based messages
        :param config: Additional configuration parameters
        """
        self.name = name
        self.role = role
        self.llm_provider = llm_provider
        self.memory_provider = memory_provider
        self.communication_provider = communication_provider
        self.tools = tools or []
        self.config = config or {}
        
        # Set up logging
        self.logger = logging.getLogger(f"Agent_{name}")
        
        # Store initial context for potential reinitiation
        self._initial_context = initial_context or [
            {"role": "system", "content": f"You are {name}, an AI assistant with the role: {role}"}
        ]
    
    async def initialize_conversation(self, additional_context: Optional[List[Dict[str, str]]] = None) -> None:
        """
        Asynchronously initialize the agent's conversation context.
        
        :param additional_context: Optional additional context messages to append
        """
        try:
            # Merge initial context with any additional context
            context = self._initial_context.copy()
            if additional_context:
                context.extend(additional_context)
            
            await self.llm_provider.initialize_conversation(context)
            self.logger.info(f"Agent {self.name} conversation initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize agent conversation: {e}")
            raise
    
    async def add_tool(self, tool: BaseTool) -> None:
        """
        Asynchronously add a new tool to the agent's toolset.
        
        :param tool: Tool to add
        """
        self.tools.append(tool)
    
    async def send_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Asynchronously send a message and get a response.
        
        :param message: Message to send
        :param context: Optional additional context
        :return: LLM's response
        """
        try:
            # Ensure conversation is initialized
            if not hasattr(self.llm_provider, '_conversation'):
                await self.initialize_conversation()
            
            # Prepare message with role
            message_payload = {"role": "user", "content": message}
            
            response = await self.llm_provider.send_message(message_payload, context)
            
            # Optionally store conversation in memory
            if self.memory_provider:
                await self.memory_provider.store(f"{self.name}_last_message", message)
                await self.memory_provider.store(f"{self.name}_last_response", response)
            
            return response
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise
    
    async def stream_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronously stream a message response.
        
        :param message: Message to send
        :param context: Optional additional context
        :yield: Streamed response tokens
        """
        try:
            # Ensure conversation is initialized
            if not hasattr(self.llm_provider, '_conversation'):
                await self.initialize_conversation()
            
            # Prepare message with role
            message_payload = {"role": "user", "content": message}
            
            async for token in self.llm_provider.stream_message(message_payload, context):
                yield token
        except Exception as e:
            self.logger.error(f"Error streaming message: {e}")
            raise
    
    async def broadcast(self, topic: str, message: Any) -> None:
        """
        Asynchronously broadcast a message via the communication provider.
        
        :param topic: Communication topic
        :param message: Message to broadcast
        """
        if not self.communication_provider:
            self.logger.warning("No communication provider configured")
            return
        
        await self.communication_provider.send(topic, message)

class AgentCrew:
    """
    Manages a group of agents working together towards a common goal.
    """
    
    def __init__(
        self, 
        agents: List[Agent],
        global_memory_provider: Optional[BaseMemoryProvider] = None,
        communication_broker: Optional[BaseCommunicationProvider] = None
    ):
        """
        Initialize an agent crew.
        
        :param agents: List of agents in the crew
        :param global_memory_provider: Shared memory provider for the crew
        :param communication_broker: Communication broker for inter-agent communication
        """
        self.agents = {agent.name: agent for agent in agents}
        self.global_memory_provider = global_memory_provider
        self.communication_broker = communication_broker
        
        self.logger = logging.getLogger("AgentCrew")
    
    async def get_agent(self, name: str) -> Optional[Agent]:
        """
        Asynchronously retrieve an agent by name.
        
        :param name: Name of the agent
        :return: Agent instance or None
        """
        return self.agents.get(name)
    
    async def dispatch_task(self, task: Dict[str, Any]) -> None:
        """
        Asynchronously dispatch a task to the appropriate agent(s).
        
        :param task: Task details
        """
        # Placeholder for task routing logic
        pass
    
    async def synchronize_state(self) -> None:
        """
        Asynchronously synchronize global state across all agents.
        """
        # Placeholder for state synchronization
        pass

class AsyncAgent:
    """
    Asynchronous agent that can interact with different LLM providers.
    """
    def __init__(
        self,
        name: str,
        role: str,
        llm_provider: BaseLLMProvider,
        memory_provider: Optional[BaseMemoryProvider] = None,
        tools: Optional[List[BaseTool]] = None
    ):
        """Initialize async agent.
        
        Args:
            name: Agent name
            role: Agent role description
            llm_provider: LLM provider to use
            memory_provider: Optional memory provider for conversation history
            tools: Optional list of tools for the agent to use
        """
        self.name = name
        self.role = role
        self.llm_provider = llm_provider
        self.tools = tools or []
        
        # Set memory provider on LLM if provided
        if memory_provider:
            self.llm_provider.set_memory_provider(memory_provider)
        
        # Register tools with LLM provider if supported
        if hasattr(self.llm_provider, 'register_tools'):
            self.llm_provider.register_tools(self.tools)
    
    async def send_message(self, message: Union[str, Dict[str, str]], chat_id: Optional[str] = None) -> str:
        """Send a message to the agent and get a response.
        
        Args:
            message: Message to send (can be a string or a dictionary)
            chat_id: Optional chat ID for conversation tracking
            
        Returns:
            Agent's response
        """
        # Convert string message to dictionary if needed
        if isinstance(message, str):
            message = {"role": "user", "content": message}
        
        return await self.llm_provider.send_message(message, chat_id)
    
    async def stream_message(self, message: Dict[str, str], chat_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Stream a message response from the agent.
        
        Args:
            message: Message to send
            chat_id: Optional chat ID for conversation tracking
            
        Yields:
            Chunks of the agent's response
        """
        async for chunk in self.llm_provider.stream_message(message, chat_id):
            yield chunk
