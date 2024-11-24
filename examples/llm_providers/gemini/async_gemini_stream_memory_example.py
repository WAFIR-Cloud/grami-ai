import asyncio
import os
from dotenv import load_dotenv

from grami.agents import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

async def main():
    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Initialize memory and provider
    memory = LRUMemory(capacity=100)
    provider = GeminiProvider(api_key=api_key)
    provider.set_memory_provider(memory)

    # Create agent with memory and system instructions
    agent = AsyncAgent(
        name="CuriousCatStoryAgent",
        llm=provider,
        memory=memory,
        system_instructions="You are an AI that tells engaging stories about curious cats."
    )

    # Define conversation messages
    messages = [
        "Tell me a short story about a curious cat.",
        "What happened to the cat in the end?"
    ]

    # Stream responses
    for message in messages:
        print(f"User: {message}")
        print("Agent: ", end='', flush=True)
        
        # Stream the response
        async for token in agent.stream_message(message):
            print(token, end='', flush=True)
        print("\n")

    # Show memory contents
    print("\nMemory Contents:")
    messages = await memory.get_messages()
    import json
    print(json.dumps(messages, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
