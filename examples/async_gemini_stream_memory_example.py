import asyncio
import os
from dotenv import load_dotenv
import json
import logging

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")
    return api_key

async def main():
    # Initialize components
    memory = LRUMemory(capacity=1000)
    provider = GeminiProvider(
        api_key=read_api_key(),
        system_prompt="You are a helpful AI assistant with perfect memory capabilities.",
        memory_provider=memory
    )
    
    # Create agent with memory
    agent = AsyncAgent(
        name="MemoryBot",
        role="A helpful AI assistant with perfect memory capabilities",
        llm_provider=provider
    )

    # Example streaming conversation
    messages = [
        "Tell me a short story about a curious cat.",
        "What happened to the cat in the end?"
    ]

    # Conversation loop
    for msg in messages:
        print(f"User: {msg}")
        print("Agent: ", end='', flush=True)
        
        # Stream the response with improved error handling
        full_response = ""
        try:
            async for token in agent.stream_message(msg):
                print(token, end='', flush=True)
                full_response += token
            print("\n")
        except Exception as e:
            # Log the error and provide a fallback response
            logger.error(f"Error during streaming: {e}")
            
            # If streaming fails, try a non-streaming message send
            try:
                full_response = await agent.send_message(msg)
                print(f"\nFallback Response: {full_response}\n")
            except Exception as fallback_error:
                logger.error(f"Fallback message send failed: {fallback_error}")
                full_response = "I apologize, but I encountered an error generating a response."
                print(f"\n{full_response}\n")

    # Demonstrate memory retrieval
    print("Memory Contents:")
    contents = await memory.list_contents()
    print(json.dumps(contents, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
