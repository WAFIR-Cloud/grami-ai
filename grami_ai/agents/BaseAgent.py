import uuid
from abc import ABC
from collections.abc import Iterable
from typing import Any, Dict, List, Optional, Type

import google.generativeai as genai
from google.api_core import retry
from google.generativeai.types import content_types

from grami_ai.events import KafkaEvents
from grami_ai.loggers.Logger import Logger
from grami_ai.memory.memory import AbstractMemory
from grami_ai.tools.api_tools import publish_task_sync, select_agent_type, select_task_topic_name

# Usage
logger = Logger()

# Default model and configuration for Gemini
# DEFAULT_MODEL_NAME = "models/gemini-1.5-pro"  # Latest Gemini Pro model
DEFAULT_MODEL_NAME = "models/gemini-1.5-flash"  # Latest Gemini Pro model
DEFAULT_SYSTEM_INSTRUCTION = "You are Grami, an Expert Digital Media agent."

default_generation_config = genai.types.GenerationConfig(
    max_output_tokens=7000,  # Limit response length
    temperature=0.5,  # Control response creativity (1.0 is balanced)
)

default_safety = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Provides core functionalities for interacting with Gemini models,
    including chat initialization, message sending, and memory management.
    Attributes:
        api_key (str): API key for authentication with Gemini.
        model_name (str): Name of the Gemini model to use.
        system_instruction (str): Initial instructions for the model.
        memory (Optional[AbstractMemory]): Memory object for storing conversation history.
        kafka (Optional[KafkaEvents]): Kafka event producer for logging events.
        safety_settings (Optional[Dict[str, str]]): Safety settings for content filtering.
        generation_config (Optional[genai.GenerationConfig]): Configuration for text generation.
        tools (List[Any]): List of tools available to the agent.
        built_in_tools (List[Any]): List of built-in tools (e.g., `publish_task`).
        chat_id (str): Unique identifier for the chat session.
        convo (Any): Gemini conversation object.
    """

    def __init__(
            self,
            api_key: str,
            model_name: str = DEFAULT_MODEL_NAME,
            system_instruction: str = DEFAULT_SYSTEM_INSTRUCTION,
            memory: Optional[AbstractMemory] = None,
            kafka: Optional[KafkaEvents] = None,
            safety_settings: Optional[Dict[str, str]] = None,
            generation_config: Optional[genai.GenerationConfig] = default_generation_config,
            tools: Optional[List[Any]] = None
    ):
        """
        Initializes a new agent instance.
        Args:
            api_key (str): API key for authentication.
            model_name (str, optional): Name of the Gemini model. Defaults to DEFAULT_MODEL_NAME.
            system_instruction (str, optional): System instructions for the model. Defaults to DEFAULT_SYSTEM_INSTRUCTION.
            memory (Optional[AbstractMemory], optional): Memory object. Defaults to None.
            kafka (Optional[KafkaEvents], optional): Kafka event producer. Defaults to None.
            safety_settings (Optional[Dict[str, str]], optional): Safety settings. Defaults to None.
            generation_config (Optional[genai.GenerationConfig], optional): Generation config. Defaults to default_generation_config.
            tools (Optional[List[Any]], optional): List of tools. Defaults to None.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.memory = memory
        self.kafka = kafka
        if safety_settings is None:
            self.safety_settings = default_safety  # Use default safety settings if none provided
        else:
            self.safety_settings = safety_settings
        self.generation_config = generation_config
        self.tools = tools or []  # Initialize with provided tools or an empty list
        self.built_in_tools = [publish_task_sync, select_agent_type,
                               select_task_topic_name]  # Add more built-in tools as needed
        self.tools.extend(self.built_in_tools)  # Extend the list with built-in tools
        self.chat_id = str(uuid.uuid4())  # Generate a unique ID for this chat session
        self.convo = None  # Initialize conversation object to None
        self.tool_config = self.tool_config_from_mode("auto")
        genai.configure(api_key=self.api_key)  # Configure Gemini with the provided API key

    def initialize_chat(self) -> None:
        """
        Initializes a new chat session with the Gemini model.
        """
        if not self.convo:
            self.convo = self._create_conversation()
            logger.info(f"Initialized chat for {self.__class__.__name__}, chat ID: {self.chat_id}")

    def _create_conversation(self) -> Any:
        """
        Creates a new conversation with the specified model and configuration.
        Returns:
            Any: Gemini conversation object.
        """
        model = genai.GenerativeModel(
            self.model_name,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings,  # Use instance safety settings
            tools=self.tools,
        )
        return model.start_chat(enable_automatic_function_calling=True)

    async def send_message(self, message: str) -> str:
        """
        Sends a message to the Gemini model and receives a response.
        Handles loading and storing conversation history in memory if a memory object is provided.
        Args:
            message (str): The message to send to the model.
        Returns:
            str: The model's response.
        """
        if not self.convo:
            self.initialize_chat()

        if self.memory:
            self.convo.history = await self._load_memory()  # Load history from memory

        response = await self.convo.send_message_async(
            message,
            request_options={'retry': retry.AsyncRetry()}  # Add retry logic for robustness
        )
        logger.info(response.usage_metadata)  # Print usage metadata (token consumption, etc.)
        if self.memory and response.text is not None:
            logger.info(f'[*] to memory')
            await self._store_interaction(message, response.text)  # Store the interaction in memory

        return response.text  # Return the model's response text

    def tool_config_from_mode(self, mode: str, fns: Iterable[str] = ()):
        """Create a tool config with the specified function calling mode."""
        return content_types.to_tool_config(
            {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
        )

    async def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Loads conversation history from the memory object.
        Returns:
            List[Dict[str, Any]]: List of conversation turns in Gemini's format.
        """
        history = await self.memory.get_items(self.chat_id)
        return self._format_history_for_gemini(history)

    async def _store_interaction(self, user_message: str, model_response: str) -> None:
        """
        Stores a user message and the model's response in memory.
        Args:
            user_message (str): The user's message.
            model_response (str): The model's response.
        """
        await self.memory.add_item(self.chat_id, {"role": "user", "content": user_message})
        await self.memory.add_item(self.chat_id, {"role": "model", "content": model_response})

    @staticmethod
    def _format_history_for_gemini(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Formats conversation history from memory to be compatible with Gemini's expected format.
        Args:
            history (List[Dict[str, Any]]): History in the memory's format.
        Returns:
            List[Dict[str, Any]]: History formatted for Gemini.
        """
        return [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]


def create_agent(agent_class: Type[BaseAgent], api_key: str, **kwargs) -> BaseAgent:
    """
    Factory function to create an agent instance.
    Simplifies agent creation by handling instantiation and argument passing.
    Args:
        agent_class (Type[BaseAgent]): The class of the agent to create.
        api_key (str): API key for authentication.
        **kwargs: Additional keyword arguments
        """
    return agent_class(api_key=api_key, **kwargs)
