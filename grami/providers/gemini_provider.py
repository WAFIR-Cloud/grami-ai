from typing import Optional, Dict, Any, List, Callable, AsyncGenerator, Union
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
        enable_automatic_function_calling: bool = False
    ):
        """Initialize the provider.
        
        Args:
            api_key: The API key for Gemini
            model_name: The model name to use
            tools: Optional list of tools to register
            enable_automatic_function_calling: Whether to enable automatic function calling
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
        if not hasattr(self, '_memory_provider') or not self._memory_provider:
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

    async def stream_message(self, message: Union[str, Dict[str, str]], context: Optional[Dict] = None):
        """
        Asynchronously stream a message response.
        
        :param message: User message (string or dictionary)
        :param context: Optional context
        :return: Streaming response object to be iterated by the caller
        """
        if not self._chat:
            await self.initialize_conversation()
        
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {'content': message, 'role': 'user'}
        else:
            message_payload = message
        
        # Add current message to conversation history
        self._conversation_history.append(message_payload)
        
        try:
            # Prepare contents, handling empty conversation history
            contents = [
                {'role': 'user', 'parts': [part['content'] for part in self._conversation_history if part.get('role') == 'user']},
                {'role': 'model', 'parts': [part['content'] for part in self._conversation_history if part.get('role') == 'model']}
            ]
            
            # Remove empty lists to prevent API errors
            contents = [content for content in contents if content['parts']]
            
            # Add current message
            contents.append({'role': 'user', 'parts': [message_payload['content']]})
            
            # Send message with streaming, including conversation history
            response = self._model.generate_content(
                contents=contents,
                stream=True
            )
            
            # Prepare to collect full response for memory
            full_response = ""
            last_chunk = None
            
            # Iterate through chunks
            for chunk in response:
                token = chunk.text
                full_response += token
                last_chunk = chunk
                yield token
            
            # Store memory after last chunk
            if last_chunk and hasattr(self, '_memory_provider'):
                await self._store_conversation_memory(
                    user_message=message_payload['content'], 
                    model_response=full_response
                )
        except Exception as e:
            logger.error(f"Error preparing streaming message: {e}")
            raise

    def set_memory_provider(self, memory_provider):
        """
        Set the memory provider for the Gemini provider.
        
        :param memory_provider: Memory provider to use
        """
        self._memory_provider = memory_provider