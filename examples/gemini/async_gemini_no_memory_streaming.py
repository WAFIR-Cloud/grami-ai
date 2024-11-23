import asyncio
import os
from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

async def main():
    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Initialize provider with only API configs
    provider = GeminiProvider(api_key=api_key)

    # Create agent without memory and with system instructions
    agent = AsyncAgent(
        name="NoMemoryStreamingAgent",
        llm=provider,
        memory=None,
        system_instructions="You are a helpful AI assistant that tells engaging stories."
    )

    # Define conversation messages
    messages = [
        "Tell me a short story about a curious cat.",
        "What was the cat's name?",
        "Describe the cat's adventure in more detail."
    ]

    # Stream responses without memory
    for message in messages:
        print(f"User: {message}")
        print("Agent: ", end='', flush=True)
        
        # Stream the response
        async for token in agent.stream_message(message):
            print(token, end='', flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
