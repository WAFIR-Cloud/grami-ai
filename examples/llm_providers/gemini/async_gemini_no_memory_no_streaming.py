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
        name="NoMemoryNoStreamingAgent",
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

    # Send messages without memory or streaming
    for message in messages:
        print(f"User: {message}")
        response = await agent.send_message(message)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
