import asyncio
import os
from dotenv import load_dotenv
from grami import AsyncAgent
from grami.providers import GeminiProvider
from grami.memory import LRUMemory

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the memory provider with a small capacity for demonstration
    memory = LRUMemory(capacity=5)
    
    # Initialize the Gemini provider
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Create an async agent with memory
    agent = AsyncAgent(
        name="MemoryAgent",
        role="AI Assistant with memory capabilities",
        llm_provider=provider,
        memory_provider=memory
    )
    
    print("1. Testing memory storage and retrieval:")
    # Store a greeting with 60-second expiry
    await memory.store("greeting", "Hello, I am an AI assistant!")
    greeting = await memory.retrieve("greeting")
    print(f"Retrieved greeting: {greeting}")
    
    print("\n2. Testing LRU functionality:")
    # Add items beyond capacity
    for i in range(6):
        await memory.store(f"item_{i}", f"Value {i}")
    
    # List all keys
    keys = await memory.list_keys()
    print("Current keys in memory:")
    for key in keys:
        value = await memory.retrieve(key)
        print(f"- {key}: {value}")
    
    print("\n3. Testing pattern matching:")
    # List keys matching a pattern
    item_keys = await memory.list_keys(pattern="item_.*")
    print("Keys matching 'item_' pattern:")
    for key in item_keys:
        value = await memory.retrieve(key)
        print(f"- {key}: {value}")
    
    print("\n4. Testing memory with agent conversation:")
    # Have a conversation that uses memory
    response = await agent.send_message("What is the capital of France?")
    print("Agent: " + response)
    
    # List recent conversation keys
    print("\nConversation memory keys:")
    conv_keys = await memory.list_keys(pattern=r"\d{4}-\d{2}-\d{2}.*")
    for key in conv_keys:
        value = await memory.retrieve(key)
        if isinstance(value, dict):
            print(f"- {key}:")
            print(f"  Message: {value.get('message', 'N/A')}")
            print(f"  Response: {value.get('response', 'N/A')}\n")

if __name__ == "__main__":
    asyncio.run(main())
