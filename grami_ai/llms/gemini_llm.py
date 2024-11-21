import google.generativeai as genai
from typing import Any, Dict, List, Optional

from grami_ai.llms.base_llm import BaseLLMProvider


class GeminiLLMProvider(BaseLLMProvider):
    """
    Concrete implementation of the BaseLLMProvider for Google's Gemini AI.
    """

    def __init__(
        self, 
        api_key: str, 
        model_name: str = "models/gemini-1.5-flash", 
        system_instruction: Optional[str] = "You are a helpful AI assistant.",
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, str]]] = None
    ):
        """
        Initialize the Gemini LLM provider.
        
        Args:
            api_key (str): Google AI API key
            model_name (str, optional): Gemini model to use. Defaults to "models/gemini-1.5-flash".
            system_instruction (Optional[str], optional): System-level instruction. Defaults to a generic instruction.
            generation_config (Optional[Dict[str, Any]], optional): Generation configuration.
            safety_settings (Optional[List[Dict[str, str]]], optional): Safety filtering settings.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.system_instruction = system_instruction
        
        # Default generation config if not provided
        self.generation_config = generation_config or {
            "max_output_tokens": 7000,
            "temperature": 0.5
        }
        
        # Default safety settings if not provided
        self.safety_settings = safety_settings or [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

    async def start_chat(self, tools: Optional[List[Any]] = None):
        """
        Start a new chat session with Gemini.
        
        Args:
            tools (Optional[List[Any]], optional): List of tools/functions to be used by the model.
        
        Returns:
            Any: Gemini conversation object
        """
        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings,
            tools=tools
        )
        return model.start_chat(enable_automatic_function_calling=True)

    async def send_message(self, conversation, message: str, tools: Optional[List[Any]] = None):
        """
        Send a message in an existing Gemini conversation.
        
        Args:
            conversation (Any): The Gemini conversation object
            message (str): The message to send
            tools (Optional[List[Any]], optional): Additional tools to use
        
        Returns:
            str: The model's response
        """
        response = await conversation.send_message_async(message)
        return response.text

    def format_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format conversation history for Gemini's requirements.
        
        Args:
            history (List[Dict[str, Any]]): Conversation history to format
        
        Returns:
            List[Dict[str, Any]]: Formatted conversation history
        """
        return [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]} 
            for msg in history
        ]
