import asyncio
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from grami_ai.core.agent import AsyncAgent
from grami_ai.core.interfaces import WebSocketInterface
from grami_ai.core.memory import AsyncRedisMemory

# Load environment variables from .env file
load_dotenv()

async def main():
    # Create the growth manager agent
    agent = await AsyncAgent.create(
        name="growth_manager",
        llm="gemini",  # You'll need to set GOOGLE_API_KEY env var
        memory="redis",  # Make sure Redis is running locally
        interface="websocket",
        tools=["instagram", "content_generation"],
        system_instruction="""You are a Growth Manager AI agent responsible for managing social media growth.
        Your tasks include:
        1. Analyzing Instagram engagement metrics
        2. Generating content ideas
        3. Scheduling posts
        4. Responding to user interactions
        
        Use the available tools to execute these tasks efficiently."""
    )
    
    try:
        # Start the agent (this will start the WebSocket server)
        await agent.start()
        
        # Keep the agent running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Gracefully shutdown on Ctrl+C
        await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
