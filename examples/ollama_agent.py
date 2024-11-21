import asyncio
import os

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.llms.ollama_llm import OllamaLLMProvider
from grami_ai.memory.memory import InMemoryAbstractMemory


async def main():
    # Create an in-memory abstract memory for conversation history
    memory = InMemoryAbstractMemory()

    # Create an OLLAMA LLM provider
    ollama_provider = OllamaLLMProvider(
        model_name="llama2",  # Make sure this model is pulled in OLLAMA
        system_instruction="You are a helpful AI assistant specialized in coding and technical topics.",
        base_url="http://localhost:11434",  # Default OLLAMA API endpoint
        generation_config={
            "temperature": 0.7,
            "max_tokens": 2048
        }
    )

    # Create a BaseAgent using the OLLAMA LLM provider
    agent = BaseAgent(
        llm_provider=ollama_provider,
        memory=memory
    )

    # Demonstrate interaction with OLLAMA LLAMA model
    conversations = [
        "Explain how dependency injection works in Python",
        "Can you provide an example of implementing dependency injection?",
        "What are the benefits of using dependency injection?"
    ]

    for message in conversations:
        response = await agent.send_message(message)
        print(f"Message: {message}")
        print(f"Response: {response}\n")


if __name__ == '__main__':
    asyncio.run(main())
