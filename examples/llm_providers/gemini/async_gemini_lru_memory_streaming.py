import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from grami.memory.lru import LRUMemory
from grami.providers.gemini_provider import GeminiProvider
from grami.agents import AsyncAgent

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

async def process_stream(stream_gen):
    """Process a stream generator and return the full response."""
    response = ""
    async for chunk in stream_gen:
        print(chunk, end="", flush=True)
        response += chunk
    print()  # New line after stream ends
    return response

async def main():
    # Initialize LRU memory with capacity of 5 messages
    memory = LRUMemory(capacity=5)
    
    # Initialize Gemini provider
    provider = GeminiProvider(
        api_key=GEMINI_API_KEY
    )
    
    # Initialize agent with memory
    agent = AsyncAgent(
        name="LRUMemoryStreamingAgent",
        llm=provider,
        memory=memory
    )
    
    # Test 1: Regular message with memory
    print("\n=== Test 1: Regular Message with Memory ===")
    message = "Hi! My favorite color is blue and my favorite number is 7."
    print(f"\nUser: {message}")
    response = await agent.send_message(message)
    print(f"Agent: {response}")
    
    # Test 2: Streaming with memory
    print("\n=== Test 2: Streaming with Memory ===")
    message = "What's my favorite color? Please check our chat history."
    print(f"\nUser: {message}")
    print("Agent: ", end="", flush=True)
    response = await process_stream(agent.stream_message(message))
    
    # Test 3: Add more messages to test LRU capacity
    print("\n=== Test 3: Testing LRU Capacity ===")
    messages = [
        "I like pizza",
        "I live in California",
        "I speak English",
        "I enjoy coding",
        "I play guitar"
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        response = await agent.send_message(msg)
        print(f"Agent: {response}")
    
    # Test 4: Check if older messages were forgotten (should forget about blue)
    print("\n=== Test 4: Checking LRU Memory Limits ===")
    message = "What's my favorite color? The answer should be forgotten due to LRU capacity."
    print(f"\nUser: {message}")
    print("Agent: ", end="", flush=True)
    response = await process_stream(agent.stream_message(message))

if __name__ == "__main__":
    asyncio.run(main())
