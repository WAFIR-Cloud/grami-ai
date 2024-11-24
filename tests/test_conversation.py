import asyncio
import os
from dotenv import load_dotenv
from grami.providers.gemini_provider import GeminiProvider

async def test_conversation_memory():
    print("\n=== Testing Conversation Memory ===")
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    
    # First message to establish context
    print("\nUser: Let's talk about a specific planet. What's the largest planet in our solar system?")
    response = await provider.send_message("Let's talk about a specific planet. What's the largest planet in our solar system?")
    print(f"Assistant: {response}")
    
    # Follow-up question about the same topic
    print("\nUser: How many moons does it have?")
    response = await provider.send_message("How many moons does it have?")
    print(f"Assistant: {response}")
    
    # Another follow-up requiring context
    print("\nUser: What's its largest moon?")
    async for chunk in provider.stream_message("What's its largest moon?"):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Final follow-up to test deep context
    print("\nUser: How does that moon compare to Earth's moon?")
    async for chunk in provider.stream_message("How does that moon compare to Earth's moon?"):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Print full conversation history
    print("\nFull Conversation History:")
    for msg in provider.get_history():
        print(f"{msg['role']}: {msg['content']}")

async def main():
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("Please set GEMINI_API_KEY in your environment variables")
        return
    
    await test_conversation_memory()

if __name__ == "__main__":
    asyncio.run(main())
