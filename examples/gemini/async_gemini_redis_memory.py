import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from grami.memory import RedisMemory
from grami.providers.gemini_provider import GeminiProvider
from grami.agent import AsyncAgent

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

async def main():
    # Initialize memory with a unique chat ID
    chat_id = "cat_story_chat"
    memory = RedisMemory(
        provider_id=chat_id,
        host='localhost', 
        port=6379, 
        db=0, 
        capacity=100
    )
    
    # Initialize provider with only API configs
    provider = GeminiProvider(api_key=os.getenv('GEMINI_API_KEY'))

    # Create agent with memory and system instructions
    agent = AsyncAgent(
        name="RedisMemoryNoStreamingAgent",
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
    conversation = []
    for i, message in enumerate(messages):
        print(f"User: {message}")
        response = await agent.send_message(message)
        print(f"Agent: {response}\n")
        
        # Add conversation to memory after each interaction
        await memory.store(f"user_query_{i+1}", message)
        await memory.store(f"agent_response_{i+1}", response)

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
