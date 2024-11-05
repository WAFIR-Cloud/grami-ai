# import google.generativeai as genai
# from typing import Any, Dict, List, Optional
# import uuid
# import logging
# from grami_ai.memory.memory import AbstractMemory
#
# # Set up logging configuration
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Default model and configuration for Gemini
# DEFAULT_MODEL_NAME = "gemini-1.5-flash"
# DEFAULT_SYSTEM_INSTRUCTION = "You Are Called Grami, an Expert Digital Media agent, responsible for Plan, Create, Schedule, and Grow Instagram accounts, use tools when you can"
#
#
# class GeminiAPI:
#     def __init__(
#             self,
#             api_key: str,
#             model_name: str = DEFAULT_MODEL_NAME,
#             system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
#             memory: Optional[AbstractMemory] = None,
#             safety_settings: Optional[List[Dict[str, str]]] = None,
#             generation_config: Optional[genai.GenerationConfig] = None,
#             tools: Optional[list] = None
#     ):
#         self.api_key = api_key
#         self.model_name = model_name
#         self.system_instruction = system_instruction
#         self.memory = memory
#         self.safety_settings = safety_settings
#         self.generation_config = generation_config
#         self.tools = tools
#         self.chat_id = str(uuid.uuid4())
#         self.convo = None  # Holds the conversation instance
#
#         # Configure the Gemini API
#         genai.configure(api_key=self.api_key)
#
#     def initialize_chat(self) -> None:
#         """Initializes the chat session, model, and starts a new conversation."""
#         if not self.convo:
#             self.convo = self._create_conversation()
#             logger.info(f"Initialized chat with model {self.model_name}, chat ID: {self.chat_id}")
#
#     def _create_conversation(self) -> Any:
#         """Creates a new conversation with the specified configuration."""
#         model = genai.GenerativeModel(
#             model_name=self.model_name,
#             safety_settings=self.safety_settings,
#             generation_config=self.generation_config,
#             tools=self.tools
#         )
#         return model.start_chat(enable_automatic_function_calling=True)
#
#     async def send_message(self, message: str) -> str:
#         """
#         Sends a message to the model and handles chat history.
#         """
#         if not self.convo:
#             self.initialize_chat()
#
#         # Load history if memory is enabled
#         if self.memory:
#             self.convo.history = await self._load_memory()
#
#         # Send the message and receive a response
#         response = self.convo.send_message(message)
#
#         # Store the interaction in memory, if enabled
#         if self.memory:
#             await self._store_interaction(message, response.text)
#
#         return response.text
#
#     async def _load_memory(self) -> List[Dict[str, Any]]:
#         """Loads chat history from memory for a given chat ID, if available."""
#         history = await self.memory.get_items(self.chat_id)
#         return self._format_history_for_gemini(history)
#
#     async def _store_interaction(self, user_message: str, model_response: str) -> None:
#         """Stores user message and model response in memory."""
#         await self.memory.add_item(self.chat_id, {"role": "user", "content": user_message})
#         await self.memory.add_item(self.chat_id, {"role": "model", "content": model_response})
#
#     @staticmethod
#     def _format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """Formats the history data to the structure required by Gemini."""
#         return [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]
