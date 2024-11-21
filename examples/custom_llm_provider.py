import asyncio
from typing import Any, Dict, List, Optional

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.memory.memory import InMemoryAbstractMemory


class MockLLMProvider(BaseLLMProvider):
    """
    A simple mock LLM provider for demonstration purposes.
    This simulates an LLM with predefined responses.
    """

    def __init__(
        self, 
        api_key: str, 
        model_name: str = "mock-model", 
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, str]]] = None
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.system_instruction = system_instruction or "You are a helpful mock AI assistant."
        self.conversation_history = []

    async def start_chat(self, tools: Optional[List[Any]] = None):
        """
        Start a mock chat session.
        
        Args:
            tools (Optional[List[Any]], optional): Ignored in this mock implementation.
        
        Returns:
            MockLLMProvider: Returns self as the conversation object
        """
        return self

    async def send_message(self, conversation, message: str, tools: Optional[List[Any]] = None):
        """
        Send a message and get a predefined response.
        
        Args:
            conversation (MockLLMProvider): The mock conversation object
            message (str): The input message
            tools (Optional[List[Any]], optional): Ignored in this mock implementation
        
        Returns:
            str: A predefined response based on the input message
        """
        # Simple mock responses
        mock_responses = {
            "hello": "Hi there! I'm a mock AI assistant.",
            "how are you": "I'm functioning perfectly, thanks for asking!",
            "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
        }
        
        # Store the conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Find a matching response or use a default
        response = mock_responses.get(
            message.lower(), 
            "I'm a mock AI and don't have a specific response for that."
        )
        
        self.conversation_history.append({"role": "model", "content": response})
        return response

    def format_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format the conversation history.
        
        Args:
            history (List[Dict[str, Any]]): Input conversation history
        
        Returns:
            List[Dict[str, Any]]: Formatted history
        """
        return [
            {"role": msg["role"], "parts": [{"text": msg["content"]}]} 
            for msg in history
        ]


async def main():
    # Create an in-memory abstract memory for conversation history
    memory = InMemoryAbstractMemory()

    # Create a custom LLM provider
    mock_llm_provider = MockLLMProvider(
        api_key="mock-key",
        model_name="mock-conversational-model",
        system_instruction="You are a witty mock AI assistant."
    )

    # Create a BaseAgent using the custom LLM provider
    agent = BaseAgent(
        llm_provider=mock_llm_provider,
        memory=memory
    )

    # Demonstrate interaction with the mock LLM
    messages = ["hello", "how are you", "tell me a joke"]
    
    for message in messages:
        response = await agent.send_message(message)
        print(f"Message: {message}")
        print(f"Response: {response}\n")


if __name__ == '__main__':
    asyncio.run(main())
