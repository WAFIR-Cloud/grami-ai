import asyncio
import os
from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.redis_memory import RedisMemory

async def main():
    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Use a unique chat ID for memory storage
    chat_id = "cat_story_chat_streaming"
    memory = RedisMemory(provider_id=chat_id)

    # Initialize provider with only API configs
    provider = GeminiProvider(api_key=api_key)

    # Create agent with memory and system instructions
    agent = AsyncAgent(
        name="RedisMemoryStreamingAgent",
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

    # Send messages with memory and streaming
    conversation = []
    for i, message in enumerate(messages):
        print(f"User: {message}")
        print("Agent: ", end='', flush=True)
        
        full_response = ""
        async for token in agent.stream_message(message):
            print(token, end='', flush=True)
            full_response += token
        print("\n")
        
        # Add conversation to memory after each interaction
        await memory.store(f"user_query_{i+1}", message)
        await memory.store(f"agent_response_{i+1}", full_response)

    # Show memory contents
    print("\nMemory Contents:")
    memory_contents = await memory.list_contents()
    import json
    print(json.dumps(memory_contents, indent=2))
    
    # Debug: print recent items
    print("\nRecent Items:")
    recent_items = await memory.get_recent_items()
    print(json.dumps(recent_items, indent=2))
    
    # Retrieve a specific memory item
    retrieved_item = await memory.retrieve("user_query_2")
    print("\nRetrieved Item:")
    print(retrieved_item)

if __name__ == "__main__":
    asyncio.run(main())
