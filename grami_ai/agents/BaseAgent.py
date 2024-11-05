import google.generativeai as genai
from typing import Any, Dict, List, Optional, Type
import uuid
import logging
from abc import ABC, abstractmethod

from grami_ai.events import KafkaEvents
from grami_ai.memory.memory import AbstractMemory
from grami_ai.tools.api_tools import publish_task

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default model and configuration for Gemini
DEFAULT_MODEL_NAME = "gemini-1.5-pro"
DEFAULT_SYSTEM_INSTRUCTION = "You are Grami, an Expert Digital Media agent."


class BaseAgent(ABC):
    """Abstract base class for agents."""

    def __init__(
            self,
            api_key: str,
            model_name: str = DEFAULT_MODEL_NAME,
            system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
            memory: Optional[AbstractMemory] = None,
            kafka: Optional[KafkaEvents] = None,
            safety_settings: Optional[List[Dict[str, str]]] = None,
            generation_config: Optional[genai.GenerationConfig] = None,
            tools: Optional[List[Any]] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.memory = memory
        self.kafka = kafka
        self.safety_settings = safety_settings
        self.generation_config = generation_config
        self.tools = tools or []  # Initialize with provided tools or empty list
        # List of built-in tools
        self.built_in_tools = [publish_task, ]  # Add more tools as needed
        self.tools.extend(self.built_in_tools)  # Extend the list with built-in tools
        self.chat_id = str(uuid.uuid4())
        self.convo = None  # Holds the conversation instance

        genai.configure(api_key=self.api_key)

    def initialize_chat(self) -> None:
        """Initializes the chat session and model conversation."""
        if not self.convo:
            self.convo = self._create_conversation()
            logger.info(f"Initialized chat for {self.__class__.__name__}, chat ID: {self.chat_id}")

    def _create_conversation(self) -> Any:
        """Creates a new conversation with the specified configuration."""
        model = genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings=self.safety_settings,
            generation_config=self.generation_config,
            tools=self.tools
        )
        return model.start_chat(enable_automatic_function_calling=True)

    async def send_message(self, message: str) -> str:
        """Handles message sending with memory support."""
        if not self.convo:
            self.initialize_chat()

        if self.memory:
            self.convo.history = await self._load_memory()

        response = self.convo.send_message(message)
        if self.memory:
            await self._store_interaction(message, response.text)

        return response.text

    async def _load_memory(self) -> List[Dict[str, Any]]:
        """Loads chat history from memory."""
        history = await self.memory.get_items(self.chat_id)
        return self._format_history_for_gemini(history)

    async def _store_interaction(self, user_message: str, model_response: str) -> None:
        """Stores user and model interactions in memory."""
        await self.memory.add_item(self.chat_id, {"role": "user", "content": user_message})
        await self.memory.add_item(self.chat_id, {"role": "model", "content": model_response})

    @staticmethod
    def _format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formats history for Gemini compatibility."""
        return [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]

    async def listen_for_tasks(self):
        """Listens for tasks directed at this agent."""
        async for task in self.kafka.consume(["tasks_planner", "tasks_content_creator"], "agent_group",
                                             self.handle_task):
            pass  # Handle task here


def create_agent(agent_class: Type[BaseAgent], api_key: str, **kwargs) -> BaseAgent:
    """
    Factory function to create and return an instance of an agent.

    :param agent_class: The class of the agent to instantiate.
    :param api_key: API key for authentication.
    :param kwargs: Additional arguments for agent initialization.
    :return: An instance of the specified agent.
    """
    return agent_class(api_key=api_key, **kwargs)
