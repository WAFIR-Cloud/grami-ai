from typing import List, Dict, Any, Optional, AsyncGenerator, Union, Callable
from .core.base import BaseLLMProvider, BaseMemoryProvider, BaseCommunicationProvider, BaseTool
import logging
import asyncio
from datetime import datetime
import uuid

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
        message: Union[str, Dict[str, str]], 
        context: Optional[Dict] = None
    ) -> str:
        """
        Send a message using the LLM provider.
        
        :param message: Message to send (string or dictionary)
        :param context: Optional context dictionary for additional parameters
        :return: Response from the LLM
        """
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Send message via LLM provider
        response = await self.llm_provider.send_message(message_payload, context)
        
        # Store conversation turn in memory if memory provider exists
        if self.memory_provider:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Ensure memory_provider is an instance of BaseMemoryProvider
            if hasattr(self.memory_provider, 'store'):
                await self.memory_provider.store(
                    unique_key, 
                    {
                        "type": "conversation_turn",
                        "user_message": {
                            "content": message_payload.get('content', ''),
                            "role": "user"
                        },
                        "model_response": {
                            "content": response,
                            "role": "model"
                        },
                        "timestamp": current_timestamp
                    }
                )
        
        return response
    
    async def stream_message(
        self, 
        message: Union[str, Dict[str, str]], 
        context: Optional[Dict] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream a message response from the LLM.
        
        :param message: Message to send (string or dictionary)
        :param context: Optional context dictionary for additional parameters
        :param kwargs: Additional keyword arguments to pass to the LLM provider
        :return: Async generator of response tokens
        """
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Merge context and kwargs
        context = context or {}
        context.update(kwargs)
        
        # Stream message via LLM provider
        response_stream = self.llm_provider.stream_message(message_payload, context)
        
        # Collect full response for memory storage
        full_response = []
        
        # Stream tokens
        async for token in response_stream:
            full_response.append(token)
            yield token
        
        # Combine tokens into full response
        response = ''.join(full_response)
        
        # Store conversation turn in memory if memory provider exists
        if self.memory_provider:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Ensure memory_provider is an instance of BaseMemoryProvider
            if hasattr(self.memory_provider, 'store'):
                await self.memory_provider.store(
                    unique_key, 
                    {
                        "type": "conversation_turn",
                        "user_message": {
                            "content": message_payload.get('content', ''),
                            "role": "user"
                        },
                        "model_response": {
                            "content": response,
                            "role": "model"
                        },
                        "timestamp": current_timestamp
                    }
                )
    
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
        llm: BaseLLMProvider,
        memory: Optional[BaseMemoryProvider] = None,
        system_instructions: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None
    ):
        """
        Initialize an AsyncAgent.

        :param name: Name of the agent
        :param llm: Language model provider
        :param memory: Memory provider for storing conversation context
        :param system_instructions: System-level instructions to guide the model's behavior
        :param tools: Optional dictionary of tools the agent can use
        """
        self.name = name
        self.llm = llm
        self.memory = memory
        self.system_instructions = system_instructions
        
        # Set system instructions on the provider if supported
        if hasattr(self.llm, '_system_prompt'):
            self.llm._system_prompt = system_instructions
        
        # Register tools if provided
        if tools:
            self.llm.register_tools(tools)
    
    async def send_message(
        self, 
        message: Union[str, Dict[str, str]], 
        context: Optional[Dict] = None
    ) -> str:
        """
        Send a message using the LLM provider.
        
        :param message: Message to send (string or dictionary)
        :param context: Optional context dictionary for additional parameters
        :return: Response from the LLM
        """
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Send message via LLM provider
        response = await self.llm.send_message(message_payload, context)
        
        # Store conversation turn in memory if memory provider exists
        if self.memory:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Ensure memory is an instance of BaseMemoryProvider
            if hasattr(self.memory, 'store'):
                await self.memory.store(
                    unique_key, 
                    {
                        "type": "conversation_turn",
                        "user_message": {
                            "content": message_payload.get('content', ''),
                            "role": "user"
                        },
                        "model_response": {
                            "content": response,
                            "role": "model"
                        },
                        "timestamp": current_timestamp
                    }
                )
        
        return response
    
    async def stream_message(
        self, 
        message: Union[str, Dict[str, str]], 
        context: Optional[Dict] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream a message response from the LLM.
        
        :param message: Message to send (string or dictionary)
        :param context: Optional context dictionary for additional parameters
        :param kwargs: Additional keyword arguments to pass to the LLM provider
        :return: Async generator of response tokens
        """
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Merge context and kwargs
        context = context or {}
        context.update(kwargs)
        
        # Stream message via LLM provider
        response_stream = self.llm.stream_message(message_payload, context)
        
        # Collect full response for memory storage
        full_response = []
        
        # Stream tokens
        async for token in response_stream:
            full_response.append(token)
            yield token
        
        # Combine tokens into full response
        response = ''.join(full_response)
        
        # Store conversation turn in memory if memory provider exists
        if self.memory:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Ensure memory is an instance of BaseMemoryProvider
            if hasattr(self.memory, 'store'):
                await self.memory.store(
                    unique_key, 
                    {
                        "type": "conversation_turn",
                        "user_message": {
                            "content": message_payload.get('content', ''),
                            "role": "user"
                        },
                        "model_response": {
                            "content": response,
                            "role": "model"
                        },
                        "timestamp": current_timestamp
                    }
                )
