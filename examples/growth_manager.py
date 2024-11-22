import asyncio
from typing import Dict, Any, List
import os
import logging
from dotenv import load_dotenv
from grami_ai.core.agent import AsyncAgent
from grami_ai.core.interfaces import WebSocketInterface
from grami_ai.core.memory import AsyncRedisMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("Starting agent...")
        await agent.start()
        
        # Print the WebSocket port for the client to use
        logger.info(f"Agent interface type: {type(agent.interface)}")
        
        if hasattr(agent.interface, 'port'):
            port = agent.interface.port
            logger.info(f"WebSocket server running on port {port}")
            
            # Set environment variable and write to a file for client to read
            os.environ['GRAMI_WEBSOCKET_PORT'] = str(port)
            
            # Write port to a file for easier access
            with open('/tmp/grami_websocket_port.txt', 'w') as f:
                f.write(str(port))
        else:
            logger.error("No port attribute found on interface")
        
        # Keep the agent running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Gracefully shutdown on Ctrl+C
        await agent.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
