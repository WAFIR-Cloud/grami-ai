import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from grami.memory import RedisMemory
from grami.providers.gemini_provider import GeminiProvider
from grami.agents import AsyncAgent

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

async def main():
    # Initialize Redis memory
    memory = RedisMemory(
        host='localhost',
        port=6379,
        db=0,
        capacity=100
    )
    
    # Initialize Gemini provider with memory
    provider = GeminiProvider(
        api_key=GEMINI_API_KEY
    )
    
    # Initialize agent with memory
    agent = AsyncAgent(
        name="MemoryTestAgent",
        llm=provider,
        memory=memory
    )
    
    # First message - introduce yourself
    message = "Hi, my name is Feras!"
    print(f"\nUser: {message}")
    response = await agent.send_message(message)
    print(f"Agent: {response}")
    
    # Second message - check if it remembers the name
    message = "What's my name? Please check our conversation history to answer."
    print(f"\nUser: {message}")
    response = await agent.send_message(message)
    print(f"Agent: {response}")
    
    # Third message - ask about something mentioned earlier
    message = "What information did I share with you in our conversation? Please check our chat history."
    print(f"\nUser: {message}")
    response = await agent.send_message(message)
    print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
