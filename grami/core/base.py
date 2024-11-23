from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncGenerator
import uuid

class BaseProvider(ABC):
    """Base abstract class for all providers in the Grami AI framework."""
    
    def __init__(self, provider_id: Optional[str] = None):
        """
        Initialize a base provider with a unique identifier.
        
        :param provider_id: Optional custom identifier for the provider
        """
        self.id = provider_id or str(uuid.uuid4())
    
    @abstractmethod
    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for the provider.
        
        :param config: Configuration dictionary
        :return: Boolean indicating if configuration is valid
        """
        pass

class BaseLLMProvider(BaseProvider):
    """Abstract base class for Language Model Providers."""
    
    @abstractmethod
    async def initialize_conversation(self, context: Optional[List[Dict[str, str]]] = None):
        """
        Asynchronously initialize a new conversation with context.
        
        :param context: Optional list of context messages with role and content
        """
        pass
    
    @abstractmethod
    async def send_message(self, message: Dict[str, str], context: Optional[Dict] = None) -> str:
        """
        Base method for sending a message.
        
        :param message: Message to send
        :param context: Optional context dictionary for additional parameters
        :return: Response from the provider
        """
        raise NotImplementedError("Subclasses must implement send_message method")
    
    @abstractmethod
    async def stream_message(self, message: Dict[str, str], context: Optional[Dict] = None) -> AsyncGenerator[str, None]:
        """
        Asynchronously stream a message response from the LLM.
        
        :param message: User message to send with role and content
        :param context: Optional additional context for the message
        :yield: Streamed response tokens
        """
        pass

class BaseMemoryProvider(BaseProvider):
    """Abstract base class for Memory Management Providers."""
    
    @abstractmethod
    async def store(self, key: str, value: Any, expiry: Optional[int] = None):
        """
        Asynchronously store a value in memory with optional expiry.
        
        :param key: Storage key
        :param value: Value to store
        :param expiry: Optional expiry time in seconds
        """
        pass
    
    @abstractmethod
    async def retrieve(self, key: str) -> Any:
        """
        Asynchronously retrieve a value from memory.
        
        :param key: Storage key to retrieve
        :return: Retrieved value
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str):
        """
        Asynchronously delete a key from memory.
        
        :param key: Storage key to delete
        """
        pass
    
    @abstractmethod
    async def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """
        Asynchronously list all keys matching an optional pattern.
        
        :param pattern: Optional pattern to filter keys
        :return: List of matching keys
        """
        pass

class BaseCommunicationProvider(BaseProvider):
    """Abstract base class for Communication Interfaces."""
    
    @abstractmethod
    async def connect(self, connection_params: Dict[str, Any]):
        """
        Asynchronously establish a connection using provided parameters.
        
        :param connection_params: Connection configuration
        """
        pass
    
    @abstractmethod
    async def send(self, topic: str, message: Any):
        """
        Asynchronously send a message to a specific topic/channel.
        
        :param topic: Destination topic/channel
        :param message: Message to send
        """
        pass
    
    @abstractmethod
    async def receive(self, topic: str, callback: callable):
        """
        Asynchronously receive messages from a topic with a callback.
        
        :param topic: Source topic/channel
        :param callback: Function to handle received messages
        """
        pass

class BaseTool(ABC):
    """Abstract base class for tools/functions in the Grami AI framework."""
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """
        Asynchronously execute the tool with given arguments.
        
        :return: Result of tool execution
        """
        pass
    
    @abstractmethod
    async def validate_input(self, *args, **kwargs) -> bool:
        """
        Asynchronously validate input parameters for the tool.
        
        :return: Boolean indicating if inputs are valid
        """
        pass
