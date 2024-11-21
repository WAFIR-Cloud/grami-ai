import uuid
from abc import ABC
from collections.abc import Iterable
from typing import Any, Dict, List, Optional, Type, Union

from grami_ai.events import KafkaEvents
from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.llms.gemini_llm import GeminiLLMProvider
from grami_ai.loggers.Logger import Logger
from grami_ai.memory.memory import AbstractMemory
from grami_ai.tools.api_tools import publish_task_sync, select_agent_type, select_task_topic_name

# Usage
logger = Logger()

class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    Provides core functionalities for interacting with LLM providers,
    including chat initialization, message sending, and memory management.
    
    Attributes:
        llm_provider (BaseLLMProvider): Language Model provider for the agent
        memory (Optional[AbstractMemory]): Memory object for storing conversation history
        kafka (Optional[KafkaEvents]): Kafka event producer for logging events
        tools (List[Any]): List of tools available to the agent
        built_in_tools (List[Any]): List of built-in tools
        chat_id (str): Unique identifier for the chat session
        convo (Any): Conversation object from the LLM provider
    """

    def __init__(
            self,
            llm_provider: Union[BaseLLMProvider, Dict[str, Any]],
            memory: Optional[AbstractMemory] = None,
            kafka: Optional[KafkaEvents] = None,
            tools: Optional[List[Any]] = None
    ):
        """
        Initializes a new agent instance.
        
        Args:
            llm_provider (Union[BaseLLMProvider, Dict[str, Any]]): 
                Either a pre-configured LLM provider or a dictionary of configuration 
                to create a default Gemini LLM provider
            memory (Optional[AbstractMemory], optional): Memory object. Defaults to None.
            kafka (Optional[KafkaEvents], optional): Kafka event producer. Defaults to None.
            tools (Optional[List[Any]], optional): List of tools. Defaults to None.
        """
        # Handle different input types for LLM provider
        if isinstance(llm_provider, dict):
            # If a dictionary is provided, create a default Gemini LLM provider
            llm_provider = GeminiLLMProvider(
                api_key=llm_provider.get('api_key'),
                model_name=llm_provider.get('model_name', "models/gemini-1.5-flash"),
                system_instruction=llm_provider.get('system_instruction'),
                generation_config=llm_provider.get('generation_config'),
                safety_settings=llm_provider.get('safety_settings')
            )
        
        self.llm_provider = llm_provider
        self.memory = memory
        self.kafka = kafka
        self.tools = tools or []  # Initialize with provided tools or an empty list
        self.built_in_tools = [publish_task_sync, select_agent_type, select_task_topic_name]
        self.tools.extend(self.built_in_tools)  # Extend the list with built-in tools
        self.chat_id = str(uuid.uuid4())  # Generate a unique ID for this chat session
        self.convo = None  # Initialize conversation object to None

    async def initialize_chat(self) -> None:
        """
        Initializes a new chat session with the LLM provider.
        """
        if not self.convo:
            self.convo = await self.llm_provider.start_chat(tools=self.tools)
            logger.info(f"Initialized chat for {self.__class__.__name__}, chat ID: {self.chat_id}")

    async def send_message(self, message: str) -> str:
        """
        Sends a message to the LLM provider and receives a response.
        Handles loading and storing conversation history in memory if a memory object is provided.
        
        Args:
            message (str): The message to send to the model.
        
        Returns:
            str: The model's response.
        """
        if not self.convo:
            await self.initialize_chat()

        if self.memory:
            # Load history from memory and format it for the specific LLM provider
            history = await self._load_memory()
            self.convo.history = self.llm_provider.format_history(history)

        response = await self.llm_provider.send_message(self.convo, message, tools=self.tools)
        
        if self.memory and response is not None:
            logger.info(f'[*] Storing interaction to memory')
            await self._store_interaction(message, response)

        return response

    async def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Loads conversation history from the memory object.
        
        Returns:
            List[Dict[str, Any]]: List of conversation turns
        """
        return await self.memory.get_items(self.chat_id)

    async def _store_interaction(self, user_message: str, model_response: str) -> None:
        """
        Stores a user message and the model's response in memory.
        
        Args:
            user_message (str): The user's message.
            model_response (str): The model's response.
        """
        await self.memory.add_item(self.chat_id, {"role": "user", "content": user_message})
        await self.memory.add_item(self.chat_id, {"role": "model", "content": model_response})


def create_agent(agent_class: Type[BaseAgent], llm_provider: Union[BaseLLMProvider, Dict[str, Any]], **kwargs) -> BaseAgent:
    """
    Factory function to create an agent instance.
    Simplifies agent creation by handling instantiation and argument passing.
    
    Args:
        agent_class (Type[BaseAgent]): The class of the agent to create.
        llm_provider (Union[BaseLLMProvider, Dict[str, Any]]): LLM provider configuration
        **kwargs: Additional keyword arguments
    
    Returns:
        BaseAgent: An instance of the specified agent class
    """
    return agent_class(llm_provider=llm_provider, **kwargs)
