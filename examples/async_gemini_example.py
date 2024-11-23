import asyncio
import os
from dotenv import load_dotenv
from grami import AsyncAgent
from grami.providers import GeminiProvider

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the Gemini provider
    provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Create an async agent with Gemini
    agent = AsyncAgent(
        name="GeminiAssistant",
        role="You are a helpful AI assistant powered by Google's Gemini model.",
        llm_provider=provider
    )
    
    print("\n1. Testing direct content generation:")
    content = await provider.generate_content("What are the three laws of robotics?")
    print(content)
    
    print("\n2. Testing agent message sending:")
    response = await agent.send_message("Tell me a short story about a curious cat.")
    print(response)
    
    print("\n3. Testing streaming capability:")
    async for chunk in agent.stream_message("Count from 1 to 5 slowly, explaining each number's significance."):
        print(chunk, end="", flush=True)
        await asyncio.sleep(0.3)  # Add a small delay to simulate real-time streaming
    print("\n")
    
    print("\n4. Testing chat context maintenance:")
    await agent.send_message("Remember the story about the curious cat you told earlier?")
    response = await agent.send_message("What happened to the cat in the end?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
