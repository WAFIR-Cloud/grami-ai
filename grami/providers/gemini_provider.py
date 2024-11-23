from typing import Optional, Dict, Any, List, Callable
from ..core.base import BaseLLMProvider
import google.generativeai as genai
import logging
import inspect
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiProvider(BaseLLMProvider):
    """Provider for Google's Gemini API."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-pro",
        tools: Optional[List[Dict[str, Any]]] = None,
        enable_automatic_function_calling: bool = False,
        system_prompt: Optional[str] = None,
        memory_provider=None
    ):
        """Initialize the provider.
        
        Args:
            api_key: The API key for Gemini
            model_name: The model name to use
            tools: Optional list of tools to register
            enable_automatic_function_calling: Whether to enable automatic function calling
            system_prompt: Optional system-level prompt to guide the model's behavior
            memory_provider: Memory provider to use for storing and retrieving conversation context
        """
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(
            model_name=model_name,
            tools=tools,
        )
        self._chat = None
        self._tools = {}
        self._memory_provider = memory_provider
        self._system_prompt = system_prompt
        self._enable_automatic_function_calling = enable_automatic_function_calling
        self._conversation_history = []

    def validate_configuration(self, **kwargs) -> None:
        """Validate the configuration parameters."""
        if not kwargs.get("api_key"):
            raise ValueError("API key is required")
        if not kwargs.get("model_name"):
            raise ValueError("Model name is required")

    def register_tools(self, tools: Dict[str, Callable]) -> None:
        """Register tools with the provider.
        
        Args:
            tools: Dictionary mapping tool names to callable functions
        """
        self._tools = tools
        logger.info(f"Registered {len(tools)} tools with GeminiProvider")

    async def initialize_conversation(self, chat_id: Optional[str] = None) -> None:
        """Initialize a new conversation."""
        try:
            self._chat = self._model.start_chat()
            logger.info("Chat session initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing conversation: {str(e)}")
            raise

    async def send_message(self, message: Dict[str, str], context: Optional[Dict] = None) -> str:
        """
        Asynchronously send a message and get a response.
        
        :param message: User message with role and content
        :param context: Optional context
        :return: LLM's response
        """
        if not self._chat:
            await self.initialize_conversation()
        
        # Use memory provider to store and retrieve context if available
        if self._memory_provider:
            # Store the current message in memory
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await self._memory_provider.store(current_timestamp, {
                "message": message.get('content', ''),
                "role": message.get('role', 'user')
            })
        
        # Add current message to conversation history
        self._conversation_history.append(message)
        
        try:
            # Use native async method
            response = await self._chat.send_message_async(message['content'])
            
            # Store the response in memory if available
            if self._memory_provider:
                await self._memory_provider.store(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    {
                        "message": message.get('content', ''),
                        "response": response.text,
                        "role": "assistant"
                    }
                )
            
            return response.text
        except Exception as e:
            # Handle potential errors
            print(f"Error sending message: {e}")
            return f"An error occurred: {e}"

    async def stream_message(self, message: Dict[str, str], chat_id: Optional[str] = None):
        """Stream a message response."""
        try:
            if not self._chat:
                await self.initialize_conversation(chat_id)

            content = message.get("content", "")
            logger.info(f"Streaming message to Gemini: {content[:100]}...")

            # Send message to Gemini
            response = await self._chat.send_message_async(content)
            response_text = ""

            # Stream the response
            async for chunk in response:
                if chunk.text:
                    response_text += chunk.text
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error in stream_message: {str(e)}")
            yield f"Error streaming message: {e}"

    def set_memory_provider(self, memory_provider):
        """
        Set the memory provider for the Gemini provider.
        
        Args:
            memory_provider: Memory provider to use for storing and retrieving conversation context
        """
        self._memory_provider = memory_provider
