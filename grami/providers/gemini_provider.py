from typing import Any, Dict, Optional, AsyncGenerator, List
import google.generativeai as genai
from ..core.base import BaseLLMProvider, BaseTool
import asyncio

class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini LLM Provider with async support and streaming.
    """
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initialize Gemini provider.
        
        :param api_key: Google AI API key
        :param model: Gemini model to use
        """
        super().__init__()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self._chat_session = None
        self._conversation_history = []
    
    async def initialize_conversation(self, context: Optional[List[Dict[str, str]]] = None):
        """
        Asynchronously initialize conversation with context.
        
        :param context: List of context messages with role and content
        """
        # Prepare initial conversation history
        self._conversation_history = context or []
        
        # Start chat session with initial context
        history = [
            {
                'role': 'user' if msg['role'] == 'user' else 'model', 
                'parts': [msg['content']]
            } 
            for msg in self._conversation_history
        ]
        
        self._chat_session = self.model.start_chat(
            history=history,
            # Enable automatic function calling
            enable_automatic_function_calling=True
        )
    
    async def send_message(self, message: Dict[str, str], context: Optional[Dict] = None) -> str:
        """
        Asynchronously send a message and get a response.
        
        :param message: User message with role and content
        :param context: Optional context
        :return: LLM's response
        """
        if not self._chat_session:
            await self.initialize_conversation()
        
        # Add current message to conversation history
        self._conversation_history.append(message)
        
        # Use synchronous send_message and convert to async
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(None, self._chat_session.send_message, message['content'])
            return response.text
        except Exception as e:
            # Handle potential errors
            print(f"Error sending message: {e}")
            return f"An error occurred: {e}"
    
    async def stream_message(self, message: Dict[str, str], context: Optional[Dict] = None) -> AsyncGenerator[str, None]:
        """
        Asynchronously stream a message response.
        
        :param message: User message with role and content
        :param context: Optional context
        :yield: Streamed response tokens
        """
        if not self._chat_session:
            await self.initialize_conversation()
        
        # Add current message to conversation history
        self._conversation_history.append(message)
        
        try:
            # Temporarily disable automatic function calling for streaming
            self._chat_session = self.model.start_chat(
                history=self._chat_session.history,
                enable_automatic_function_calling=False
            )
            
            response = self._chat_session.send_message(message['content'], stream=True)
            for chunk in response:
                yield chunk.text
        except Exception as e:
            # Handle potential errors
            print(f"Error streaming message: {e}")
            yield f"An error occurred: {e}"
        finally:
            # Restore automatic function calling
            self._chat_session = self.model.start_chat(
                history=self._chat_session.history,
                enable_automatic_function_calling=True
            )

    async def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """
        Validate the Gemini provider configuration.
        
        :param config: Configuration dictionary
        :return: Boolean indicating if configuration is valid
        """
        # Basic validation for Gemini provider
        return (
            'api_key' in config and 
            isinstance(config['api_key'], str) and 
            len(config['api_key']) > 0
        )
