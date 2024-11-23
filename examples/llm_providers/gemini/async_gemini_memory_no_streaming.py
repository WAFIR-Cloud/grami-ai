import asyncio
import os
from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

async def main():
    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Initialize memory 
    memory = LRUMemory(capacity=100)
    
    # Initialize provider with only API configs
    provider = GeminiProvider(api_key=api_key)

    # Create agent with memory and system instructions
    agent = AsyncAgent(
        name="MemoryNoStreamingAgent",
        llm=provider,
        memory=memory,
        system_instructions="You are a helpful AI assistant that tells engaging stories."
    )

    # Define conversation messages
    messages = [
        "Tell me a short story about a curious cat.",
        "What was the cat's name?",
        "Describe the cat's adventure in more detail."
    ]

    # Send messages with memory, but without streaming
    for message in messages:
        print(f"User: {message}")
        response = await agent.send_message(message)
        print(f"Agent: {response}\n")

    # Show memory contents
    print("\nMemory Contents:")
    memory_contents = await memory.list_contents()
    import json
    print(json.dumps(memory_contents, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
