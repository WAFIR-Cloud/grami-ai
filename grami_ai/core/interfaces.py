"""
Grami AI Core Interfaces Module

This module defines the core protocols and abstract base classes for the Grami AI framework.
It provides the foundational interfaces for:
- Async Tools
- Memory Management
- LLM Integration
- Agent Implementation
- Kafka Integration
- Prompt Engineering

These interfaces ensure consistent behavior and interoperability across the framework.
"""

from __future__ import annotations
import asyncio
from abc import ABC, abstractmethod
from typing import (
    Any, 
    Dict, 
    List, 
    Optional, 
    Protocol, 
    TypeVar, 
    Generic, 
    AsyncIterator, 
    Callable, 
    Coroutine
)
import json
import socket

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    import uvicorn
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

T = TypeVar('T')

def find_free_port():
    """Find a free port for WebSocket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

class AsyncTool(Protocol):
    """
    Protocol defining the interface for asynchronous tools usable by agents.
    
    All tools in the framework must implement this protocol to ensure
    consistent behavior and interoperability with agents.
    """
    
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the tool asynchronously.
        
        Args:
            *args: Variable positional arguments for tool execution.
            **kwargs: Variable keyword arguments for tool execution.
            
        Returns:
            Any: Result of tool execution.
        """
        ...

class AsyncMemoryProvider(Protocol, Generic[T]):
    """
    Protocol for asynchronous memory management.
    
    Provides a standardized interface for storing, retrieving, and managing
    data in memory systems. Supports generic type T for flexible data storage.
    
    Type Parameters:
        T: The type of values stored in memory.
    """
    
    async def store(self, key: str, value: T) -> None:
        """
        Store a value in memory asynchronously.
        
        Args:
            key (str): Unique identifier for the stored value.
            value (T): Value to store.
        """
        ...
    
    async def retrieve(self, key: str) -> Optional[T]:
        """
        Retrieve a value from memory asynchronously.
        
        Args:
            key (str): Key of the value to retrieve.
            
        Returns:
            Optional[T]: Retrieved value if found, None otherwise.
        """
        ...
    
    async def delete(self, key: str) -> None:
        """
        Delete a value from memory asynchronously.
        
        Args:
            key (str): Key of the value to delete.
        """
        ...
    
    async def list_keys(self) -> List[str]:
        """
        List all keys in memory asynchronously.
        
        Returns:
            List[str]: List of all keys currently in memory.
        """
        ...
    
    async def add_item(self, key: str, value: T) -> str:
        """
        Add an item to memory and return its unique ID.
        
        Args:
            key (str): Collection or namespace for the item.
            value (T): Value to store.
            
        Returns:
            str: Unique ID for the stored item.
        """
        ...
    
    async def get_items(
        self,
        key: str,
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """
        Retrieve items from memory with optional filtering.
        
        Args:
            key (str): Collection or namespace to query.
            filter_params: Optional filtering parameters.
            
        Returns:
            List[T]: List of matching items.
        """
        ...
    
    async def update_item(self, key: str, item_id: str, value: T) -> None:
        """
        Update an existing item in memory.
        
        Args:
            key (str): Collection or namespace.
            item_id (str): Unique ID of the item.
            value (T): New value.
        """
        ...
    
    async def delete_item(self, key: str, item_id: str) -> None:
        """
        Delete an item from memory.
        
        Args:
            key (str): Collection or namespace.
            item_id (str): Unique ID of the item to delete.
        """
        ...

class AsyncKafkaIntegration(Protocol):
    """
    Protocol for asynchronous Kafka message handling.
    
    Provides a standardized interface for producing and consuming
    messages with Apache Kafka, enabling event-driven architectures.
    """
    
    async def produce(self, topic: str, message: Any) -> None:
        """
        Produce a message to a Kafka topic asynchronously.
        
        Args:
            topic (str): Target Kafka topic.
            message (Any): Message to produce.
        """
        ...
    
    async def consume(self, topic: str) -> AsyncIterator[Any]:
        """
        Consume messages from a Kafka topic asynchronously.
        
        Args:
            topic (str): Source Kafka topic.
            
        Returns:
            AsyncIterator[Any]: Iterator over consumed messages.
        """
        ...
    
    async def publish(self, topic: str, message: Any) -> None:
        """
        Publish a message to a Kafka topic asynchronously.
        
        Args:
            topic (str): Target Kafka topic.
            message (Any): Message to publish.
        """
        ...
    
    async def subscribe(self, topic: str, callback: Callable[[Any], Coroutine[Any, Any, None]]) -> None:
        """
        Subscribe to a Kafka topic with a callback function.
        
        Args:
            topic (str): Topic to subscribe to.
            callback: Async function to handle received messages.
        """
        ...
    
    async def unsubscribe(self, topic: str) -> None:
        """
        Unsubscribe from a Kafka topic.
        
        Args:
            topic (str): Topic to unsubscribe from.
        """
        ...

class PromptTemplate:
    """
    Customizable prompt engineering template.
    
    Provides a flexible system for creating and formatting prompts
    with dynamic content and context-aware formatting.
    
    Attributes:
        template (str): The prompt template string.
    """
    
    def __init__(self, template: str):
        """
        Initialize prompt template.
        
        Args:
            template (str): Template string with format placeholders.
        """
        self.template = template
    
    async def format(self, **kwargs) -> str:
        """
        Format the prompt template with given context.
        
        Args:
            **kwargs: Format parameters for template.
            
        Returns:
            str: Formatted prompt string.
        """
        return self.template.format(**kwargs)

class BaseLLMProvider(ABC, Generic[T]):
    """
    Enhanced abstract base class for LLM providers.
    
    Provides a comprehensive interface for language model integration
    with support for tools, memory, and messaging.
    
    Type Parameters:
        T: The type of generation output.
    """
    
    @abstractmethod
    async def generate(
        self, 
        prompt: PromptTemplate, 
        tools: Optional[List[AsyncTool]] = None,
        memory: Optional[AsyncMemoryProvider] = None,
        kafka_integration: Optional[AsyncKafkaIntegration] = None,
        **kwargs: Any
    ) -> T:
        """
        Generate content using the language model.
        
        Comprehensive generation method supporting:
        - Customizable prompts
        - Tool integration
        - Memory management
        - Kafka messaging
        
        Args:
            prompt (PromptTemplate): Template for generation.
            tools (Optional[List[AsyncTool]]): Available tools.
            memory (Optional[AsyncMemoryProvider]): Memory provider.
            kafka_integration (Optional[AsyncKafkaIntegration]): Kafka integration.
            **kwargs: Additional generation parameters.
            
        Returns:
            T: Generated content.
        """
        pass

class BaseAgent(ABC, Generic[T]):
    """
    Advanced abstract base class for async agents.
    
    Provides a comprehensive framework for building intelligent agents
    with support for LLMs, memory, tools, and messaging.
    
    Type Parameters:
        T: The type of agent processing output.
        
    Attributes:
        llm (BaseLLMProvider[T]): Language model provider.
        memory (AsyncMemoryProvider): Memory management system.
        tools (List[AsyncTool]): Available tools.
        kafka (Optional[AsyncKafkaIntegration]): Kafka integration.
    """
    
    def __init__(
        self, 
        llm: BaseLLMProvider[T],
        memory: AsyncMemoryProvider,
        tools: Optional[List[AsyncTool]] = None,
        kafka_integration: Optional[AsyncKafkaIntegration] = None
    ):
        """
        Initialize agent with required components.
        
        Args:
            llm (BaseLLMProvider[T]): Language model provider.
            memory (AsyncMemoryProvider): Memory provider.
            tools (Optional[List[AsyncTool]]): Available tools.
            kafka_integration (Optional[AsyncKafkaIntegration]): Kafka integration.
        """
        self.llm = llm
        self.memory = memory
        self.tools = tools or []
        self.kafka = kafka_integration

    @abstractmethod
    async def process(
        self, 
        prompt_template: PromptTemplate, 
        **kwargs: Any
    ) -> T:
        """
        Process input using the agent's capabilities.
        
        Args:
            prompt_template (PromptTemplate): Input prompt template.
            **kwargs: Additional processing parameters.
            
        Returns:
            T: Processing result.
        """
        pass

class ContextualPromptTemplate(PromptTemplate):
    """
    Advanced prompt template with context awareness.
    
    Extends PromptTemplate with intelligent context handling
    and dynamic content adaptation.
    """
    
    async def format(
        self, 
        context: Optional[Dict[str, Any]] = None, 
        **kwargs
    ) -> str:
        """
        Format prompt with intelligent context handling.
        
        Args:
            context (Optional[Dict[str, Any]]): Additional context.
            **kwargs: Additional formatting parameters.
            
        Returns:
            str: Formatted prompt string.
        """
        if context:
            kwargs.update(context)
        return await super().format(**kwargs)

class AgentInterface(Protocol):
    """
    Protocol for agent interfaces.
    
    Defines how agents interact with their environment (chat, Kafka, etc.).
    """
    
    async def initialize(self, agent: Any) -> None:
        """
        Initialize the interface with an agent.
        
        Args:
            agent: The agent instance using this interface.
        """
        ...
    
    async def start(self) -> None:
        """Start the interface."""
        ...
    
    async def stop(self) -> None:
        """Stop the interface."""
        ...
    
    async def send(self, message: Any) -> None:
        """
        Send a message through the interface.
        
        Args:
            message: Message to send.
        """
        ...
    
    async def receive(self) -> AsyncIterator[Any]:
        """
        Receive messages through the interface.
        
        Returns:
            AsyncIterator[Any]: Iterator over received messages.
        """
        ...

class WebSocketInterface(AgentInterface):
    """WebSocket-based agent interface."""
    
    def __init__(self, host: str = "0.0.0.0", port: Optional[int] = None):
        if not WEBSOCKET_AVAILABLE:
            raise ImportError("FastAPI and uvicorn are required for WebSocket interface. Install with: pip install fastapi uvicorn")
            
        self.host = host
        self.port = port or find_free_port()
        self.agent = None
        self.app = FastAPI()
        self.server_task = None
        self.server = None
        
        # Explicitly define the WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            print(f"WebSocket connection attempt received")
            try:
                await websocket.accept()
                print(f"WebSocket connection accepted")
                
                while True:
                    try:
                        data = await websocket.receive_json()
                        print(f"Received data: {data}")
                        
                        if not self.agent:
                            print("Agent not initialized")
                            await websocket.send_json({"error": "Agent not initialized"})
                            continue
                        
                        response = await self.agent.process(data)
                        print(f"Sending response: {response}")
                        await websocket.send_json(response)
                    except json.JSONDecodeError:
                        print("Invalid JSON received")
                        await websocket.send_json({"error": "Invalid JSON"})
                    except Exception as e:
                        print(f"Error processing WebSocket message: {e}")
                        await websocket.send_json({"error": str(e)})
            except Exception as e:
                print(f"WebSocket connection error: {e}")
                try:
                    await websocket.close(code=1011)  # Internal server error
                except:
                    pass
    
    async def initialize(self, agent: Any) -> None:
        """Initialize the interface with an agent."""
        self.agent = agent
    
    async def start(self) -> None:
        """Start the WebSocket server."""
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )
        self.server = uvicorn.Server(config)
        
        # Run server in a separate task
        self.server_task = asyncio.create_task(self.server.serve())
        
        # Wait a moment for the server to start
        await asyncio.sleep(1)
        print(f"WebSocket server started on {self.host}:{self.port}")
    
    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.server_task:
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
            
        if self.server:
            await self.server.shutdown()
    
    async def send(self, message: Any) -> None:
        """Not used in WebSocket interface."""
        pass
    
    async def receive(self) -> AsyncIterator[Any]:
        """Not used in WebSocket interface."""
        yield None

class KafkaConsumerInterface(AgentInterface):
    """Kafka consumer-based agent interface."""
    
    def __init__(
        self,
        bootstrap_servers: str,
        input_topic: str,
        output_topic: Optional[str] = None,
        group_id: Optional[str] = None
    ):
        self.bootstrap_servers = bootstrap_servers
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id or "grami_agent"
        self.agent = None
        self.consumer = None
        self.producer = None
        self._running = False
    
    async def initialize(self, agent: Any) -> None:
        """Initialize Kafka consumer and producer."""
        from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
        
        self.agent = agent
        
        # Initialize consumer
        self.consumer = AIOKafkaConsumer(
            self.input_topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        
        # Initialize producer if output topic is specified
        if self.output_topic:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
    
    async def start(self) -> None:
        """Start consuming messages."""
        await self.consumer.start()
        if self.producer:
            await self.producer.start()
        
        self._running = True
        while self._running:
            try:
                async for msg in self.consumer:
                    response = await self.agent.process(msg.value)
                    if response and self.producer:
                        await self.producer.send_and_wait(
                            self.output_topic,
                            response
                        )
            except Exception as e:
                print(f"Kafka interface error: {e}")
    
    async def stop(self) -> None:
        """Stop consuming messages."""
        self._running = False
        await self.consumer.stop()
        if self.producer:
            await self.producer.stop()
    
    async def send(self, message: Any) -> None:
        """Send message to output topic."""
        if self.producer and self.output_topic:
            await self.producer.send_and_wait(self.output_topic, message)
    
    async def receive(self) -> AsyncIterator[Any]:
        """Receive messages from input topic."""
        async for msg in self.consumer:
            yield msg.value

# Utility type for async functions
AsyncFunction = Callable[..., Coroutine[Any, Any, T]]
