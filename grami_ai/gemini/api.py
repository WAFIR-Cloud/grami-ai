import asyncio
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from grami_ai.memory.redis_memory import RedisMemory

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default model and configuration for Gemini
DEFAULT_MODEL_NAME = "models/gemini-1.5-flash"
DEFAULT_SYSTEM_INSTRUCTION = "You are a helpful AI assistant for Instagram marketing."


class GeminiAPI:
    """
    A wrapper around the Gemini API with persistent chat history management.
    """

    def __init__(
        self,
        api_key: str = None,
        model_name: str = DEFAULT_MODEL_NAME,
        system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
        safety_settings: Optional[List[Dict[str, str]]] = None,
        generation_config: Optional[genai.GenerationConfig] = None,
        memory: Optional[RedisMemory] = None,
    ):
        """
        Initializes the GeminiAPI.

        Args:
            api_key: Your Gemini API key. If None, it will be fetched from the
                     GEMINI_API_KEY environment variable.
            model_name: The name of the Gemini model to use.
            system_instruction: The system instruction for the Gemini model.
            safety_settings: A list of safety settings to apply.
            generation_config: Configuration for text generation.
            memory: The RedisMemory object to use for history management.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        self.model_name = model_name
        self.system_instruction = system_instruction
        self.safety_settings = safety_settings
        self.generation_config = generation_config
        self.memory = memory
        self.chat_id = None

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

        # Initialize the Gemini model
        self.model = self._configure_generative_model()

    def _configure_generative_model(self):
        """
        Configures the generative model with desired settings.
        """
        return genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings=self.safety_settings,
            generation_config=self.generation_config,
            system_instruction=self.system_instruction,
        )

    def start_new_chat(self):
        """
        Starts a new chat session and generates a new chat_id.
        """
        self.chat_session = self.model.start_chat()
        self.chat_id = str(uuid.uuid4())

    async def send_message(self, message: str, chat_id: str = None) -> str:
        """
        Sends a message in the chat session, managing chat_id and history.
        """
        if chat_id is None:
            if self.chat_id is None:
                self.start_new_chat()
            chat_id = self.chat_id
        elif self.chat_id is None or self.chat_id != chat_id:
            self.start_new_chat()
            self.chat_id = chat_id

        if self.memory:
            # Retrieve history from Redis before sending the message
            history = await self.memory.get_items(chat_id)
            transformed_history = self.transform_history_for_gemini(history)
            self.chat_session.history = transformed_history

        response = self.chat_session.send_message(message)

        if self.memory:
            # Add user message to history
            await self.memory.add_item(
                chat_id=chat_id,
                item={"role": "user", "content": message}
            )
            # Add assistant message to history
            await self.memory.add_item(
                chat_id=chat_id,
                item={"role": "model", "content": response.text}
            )

        return response.text

    def transform_history_for_gemini(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transforms conversation history to the format required by Gemini.
        """
        return [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]