from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseLLMProvider(ABC):
    """
    Abstract base class for Language Model providers.
    Defines the interface for interacting with different LLM services.
    """

    @abstractmethod
    def __init__(
        self, 
        api_key: str, 
        model_name: str, 
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, str]]] = None
    ):
        """
        Initialize the LLM provider with necessary configuration.
        
        Args:
            api_key (str): Authentication key for the LLM service
            model_name (str): Name or identifier of the specific model to use
            system_instruction (Optional[str]): Initial system-level instruction for the model
            generation_config (Optional[Dict[str, Any]]): Configuration for text generation
            safety_settings (Optional[List[Dict[str, str]]]): Safety filtering settings
        """
        pass

    @abstractmethod
    async def start_chat(self, tools: Optional[List[Any]] = None):
        """
        Start a new chat session with the LLM.
        
        Args:
            tools (Optional[List[Any]]): Optional list of tools/functions to be used by the LLM
        
        Returns:
            Any: A conversation object specific to the LLM provider
        """
        pass

    @abstractmethod
    async def send_message(self, conversation, message: str, tools: Optional[List[Any]] = None):
        """
        Send a message in an existing conversation.
        
        Args:
            conversation (Any): The conversation object from start_chat()
            message (str): The message to send
            tools (Optional[List[Any]]): Optional list of tools/functions to be used
        
        Returns:
            str: The model's response
        """
        pass

    @abstractmethod
    def format_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format conversation history to be compatible with the specific LLM's requirements.
        
        Args:
            history (List[Dict[str, Any]]): Conversation history to format
        
        Returns:
            List[Dict[str, Any]]: Formatted conversation history
        """
        pass
