import asyncio
import os
from dotenv import load_dotenv
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

async def test_regular_message():
    print("\n=== Testing Regular Message ===")
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Test single message
    response = await provider.send_message("What is the capital of France?")
    print(f"Response: {response}")
    
    # Test conversation
    response = await provider.send_message("And what's its population?")
    print(f"Follow-up response: {response}")
    
    # Print history
    print("\nConversation History:")
    for msg in provider.get_history():
        print(f"{msg['role']}: {msg['content']}")

async def test_streaming():
    print("\n=== Testing Streaming ===")
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    
    print("Streaming response:")
    async for chunk in provider.stream_message("Tell me about the solar system in 5 sentences."):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Test follow-up with streaming
    print("Streaming follow-up response:")
    async for chunk in provider.stream_message("What's the largest planet?"):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Print history
    print("\nConversation History:")
    for msg in provider.get_history():
        print(f"{msg['role']}: {msg['content']}")

async def test_with_memory():
    print("\n=== Testing with Memory ===")
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    memory = LRUMemory(capacity=5)
    provider.set_memory_provider(memory)
    
    # First message
    response = await provider.send_message("What's your favorite color?")
    print(f"First response: {response}")
    
    # Stream second message
    print("\nStreaming second response:")
    async for chunk in provider.stream_message("Why do you like that color?"):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Print memory contents
    print("\nMemory Contents:")
    for msg in memory.messages:
        print(f"{msg['role']}: {msg['content']}")

async def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("Please set GEMINI_API_KEY in your environment variables")
        return
    
    # Run tests
    await test_regular_message()
    await test_streaming()
    await test_with_memory()

if __name__ == "__main__":
    asyncio.run(main())
