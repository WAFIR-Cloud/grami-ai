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

T = TypeVar('T')

class AsyncTool(Protocol):
    """Protocol for async tools usable by agents"""
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the tool asynchronously"""
        ...

class AsyncMemoryProvider(Protocol, Generic[T]):
    """Async memory management protocol"""
    async def store(self, key: str, value: T) -> None:
        """Store a value in memory"""
        ...
    
    async def retrieve(self, key: str) -> Optional[T]:
        """Retrieve a value from memory"""
        ...
    
    async def delete(self, key: str) -> None:
        """Delete a value from memory"""
        ...
    
    async def list_keys(self) -> List[str]:
        """List all keys in memory"""
        ...

class AsyncKafkaIntegration(Protocol):
    """Async Kafka message handling protocol"""
    async def produce(self, topic: str, message: Any) -> None:
        """Produce a message to a Kafka topic"""
        ...
    
    async def consume(self, topic: str) -> AsyncIterator[Any]:
        """Consume messages from a Kafka topic"""
        ...

class PromptTemplate:
    """Customizable prompt engineering"""
    def __init__(self, template: str):
        self.template = template
    
    async def format(self, **kwargs) -> str:
        """Format the prompt template with given context"""
        return self.template.format(**kwargs)

class BaseLLMProvider(ABC, Generic[T]):
    """Enhanced LLM provider with comprehensive async features"""
    
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
        Comprehensive generation method with:
        - Customizable prompts
        - Tool integration
        - Memory management
        - Kafka messaging support
        """
        pass

class BaseAgent(ABC, Generic[T]):
    """Advanced async agent with comprehensive capabilities"""
    
    def __init__(
        self, 
        llm: BaseLLMProvider[T],
        memory: AsyncMemoryProvider,
        tools: Optional[List[AsyncTool]] = None,
        kafka_integration: Optional[AsyncKafkaIntegration] = None
    ):
        self.llm = llm
        self.memory = memory
        self.tools = tools or []
        self.kafka = kafka_integration

    @abstractmethod
    async def process(
        self, 
        prompt_template: PromptTemplate, 
        additional_context: Optional[Dict[str, Any]] = None
    ) -> T:
        """
        Comprehensive async processing with:
        - Prompt customization
        - Tool execution
        - Memory interaction
        - Kafka messaging
        """
        pass

class ContextualPromptTemplate(PromptTemplate):
    """Advanced prompt template with context awareness"""
    async def format(
        self, 
        context: Optional[Dict[str, Any]] = None, 
        **kwargs
    ) -> str:
        """
        Format prompt with intelligent context handling
        
        Args:
            context: Additional context for prompt formatting
            **kwargs: Additional formatting parameters
        
        Returns:
            Formatted prompt string
        """
        context = context or {}
        formatted = self.template.format(
            context=context, 
            **kwargs
        )
        return formatted

# Utility type for async function
AsyncFunction = Callable[..., Coroutine[Any, Any, T]]
