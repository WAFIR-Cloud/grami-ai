from typing import Optional, Dict, Any, List, Callable, AsyncGenerator
from typing import Union
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
            safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
        generation_config=genai.GenerationConfig(
            max_output_tokens=4000,
            temperature=0.5,
            top_p=0.95,
            top_k=64,
            response_mime_type="text/plain",
        ),
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

    async def _store_conversation_memory(self, user_message: str, model_response: str) -> None:
        """
        Store a conversation turn in the memory provider.
        
        :param user_message: The user's input message
        :param model_response: The model's response
        """
        if not self._memory_provider:
            return
        
        try:
            import uuid
            from datetime import datetime
            
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            memory_entry = {
                "type": "conversation_turn",
                "user_message": {
                    "content": user_message,
                    "role": "user"
                },
                "model_response": {
                    "content": model_response,
                    "role": "model"
                },
                "timestamp": current_timestamp
            }
            
            await self._memory_provider.store(unique_key, memory_entry)
        except Exception as memory_error:
            logging.error(f"Failed to store memory: {memory_error}")

    async def send_message(self, message: Union[str, Dict[str, str]], context: Optional[Dict] = None) -> str:
        """
        Asynchronously send a message and get a response.
        
        :param message: User message (string or dictionary)
        :param context: Optional context
        :return: LLM's response as a string
        """
        if not self._chat:
            await self.initialize_conversation()
        
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Add current message to conversation history
        self._conversation_history.append(message_payload)
        
        try:
            # Send message and get response
            response = await self._chat.send_message_async(message_payload['content'])
            
            # Store memory for this conversation turn
            await self._store_conversation_memory(
                user_message=message_payload['content'], 
                model_response=response.text
            )
            
            return response.text
        except Exception as e:
            print(f"Error sending message: {e}")
            raise

    async def stream_message(self, message: Union[str, Dict[str, str]], context: Optional[Dict] = None) -> AsyncGenerator[str, None]:
        """
        Asynchronously stream a message response.
        
        :param message: User message (string or dictionary)
        :param context: Optional context
        :return: Async generator of response tokens
        """
        if not self._chat:
            await self.initialize_conversation()
        
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        # Add current message to conversation history
        self._conversation_history.append(message_payload)
        
        full_response = ""
        try:
            # Use native method to stream response
            response = await self._chat.send_message_async(message_payload['content'])
            
            # Yield tokens from the response
            for chunk in response.text.split():
                full_response += chunk + ' '
                yield chunk + ' '
            
            # Store memory after streaming is complete
            await self._store_conversation_memory(
                user_message=message_payload['content'], 
                model_response=full_response
            )
        
        except Exception as e:
            print(f"Error streaming message: {e}")
            raise StopAsyncIteration(f"An error occurred: {e}")

    def set_memory_provider(self, memory_provider):
        """
        Set the memory provider for the Gemini provider.
        
        Args:
            memory_provider: Memory provider to use for storing and retrieving conversation context
        """
        self._memory_provider = memory_provider

    def count_tokens(self, text: Union[str, Dict[str, str]]) -> int:
        """
        Count the number of tokens in the given text using the Gemini tokenizer.
        
        :param text: Input text or dictionary with a 'content' key
        :return: Number of tokens in the input
        """
        # Normalize input to string
        if isinstance(text, dict):
            text = text.get('content', '')
        elif not isinstance(text, str):
            text = str(text)
        
        try:
            # Use the model's tokenizer to count tokens
            token_count = self._model.count_tokens(text)
            return token_count.total_tokens
        except Exception as e:
            logging.error(f"Error counting tokens: {e}")
            # Fallback token estimation (rough approximation)
            return len(text.split())
