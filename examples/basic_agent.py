import asyncio
import os
from dotenv import load_dotenv

from grami.agents.async_agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

async def test_streaming():
    """Test streaming functionality with memory."""
    print("\nTesting streaming responses...")
    
    # Initialize memory and provider
    memory = LRUMemory(capacity=5)
    provider = GeminiProvider(
        api_key=os.getenv("GEMINI_API_KEY"),
        generation_config={
            "temperature": 0.9,  # Increased temperature for more creative responses
            "top_p": 0.9,       # Increased top_p for more diverse responses
            "top_k": 40,
            "max_output_tokens": 1000,
            "candidate_count": 1,  # Only need one response
            "stop_sequences": []   # No stop sequences to avoid early cutoff
        }
    )
    
    # Create agent
    agent = AsyncAgent(
        name="StreamingTestAgent",
        llm=provider,
        memory=memory,
        system_instructions="You are a helpful AI assistant. Provide natural and engaging responses."
    )
    
    # Test messages
    messages = [
        "Remember that my name is Alice and I like blue.",
        "What's my name and what color do I like?",
        "Tell me a very short story about someone named Alice who likes blue."
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        print("Agent: ", end="", flush=True)
        
        try:
            # Stream the response
            async for chunk in agent.stream_message(msg):
                print(chunk, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    
    # Print memory contents
    print("\nMemory Contents:")
    try:
        messages = await memory.get_messages()
        for i, msg in enumerate(messages, 1):
            print(f"Message {i}:")
            print(f"Role: {msg.get('role', 'unknown')}")
            print(f"Content: {msg.get('content', '')}\n")
    except Exception as e:
        print(f"Error accessing memory: {str(e)}\n")

async def test_non_streaming():
    """Test non-streaming functionality with memory."""
    print("\nTesting non-streaming responses...")
    
    # Initialize memory and provider
    memory = LRUMemory(capacity=5)
    provider = GeminiProvider(
        api_key=os.getenv("GEMINI_API_KEY"),
        generation_config={
            "temperature": 0.9,  # Increased temperature for more creative responses
            "top_p": 0.9,       # Increased top_p for more diverse responses
            "top_k": 40,
            "max_output_tokens": 1000,
            "candidate_count": 1,  # Only need one response
            "stop_sequences": []   # No stop sequences to avoid early cutoff
        }
    )
    
    # Create agent
    agent = AsyncAgent(
        name="NonStreamingTestAgent",
        llm=provider,
        memory=memory,
        system_instructions="You are a helpful AI assistant. Provide natural and engaging responses."
    )
    
    # Test messages
    messages = [
        "My favorite food is pizza.",
        "What's my favorite food?",
        "Tell me a very short story about someone who loves pizza."
    ]
    
    for msg in messages:
        print(f"\nUser: {msg}")
        try:
            response = await agent.send_message(msg)
            print(f"Agent: {response}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
    
    # Print memory contents
    print("\nMemory Contents:")
    try:
        messages = await memory.get_messages()
        for i, msg in enumerate(messages, 1):
            print(f"Message {i}:")
            print(f"Role: {msg.get('role', 'unknown')}")
            print(f"Content: {msg.get('content', '')}\n")
    except Exception as e:
        print(f"Error accessing memory: {str(e)}\n")

async def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    # Run tests
    await test_streaming()
    await test_non_streaming()

if __name__ == "__main__":
    asyncio.run(main())
