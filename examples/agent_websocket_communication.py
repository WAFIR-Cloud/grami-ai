import asyncio
import json
import logging
import os
from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

# Example tools for demonstration
def get_current_time() -> str:
    """
    Get the current time.
    
    :return: Current time as a string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_age(birth_year: int) -> int:
    """
    Calculate age based on birth year.
    
    :param birth_year: Year of birth
    :return: Current age
    """
    from datetime import datetime
    current_year = datetime.now().year
    return current_year - birth_year

async def main():
    """
    Demonstrate AsyncAgent WebSocket communication.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Initialize Gemini Provider
    provider = GeminiProvider(api_key=api_key)

    # Create an AsyncAgent with tools
    agent = AsyncAgent(
        name="WebSocketEnabledAgent",
        llm=provider,
        system_instructions="You are a helpful AI assistant that can answer questions and perform simple calculations.",
        tools={
            "get_current_time": get_current_time,
            "calculate_age": calculate_age
        }
    )

    # Setup WebSocket communication interface
    communication_interface = await agent.setup_communication(
        communication_type='websocket', 
        host='localhost', 
        port=8765
    )

    # Simulate a client interaction
    async def simulate_client_interaction():
        """
        Simulate WebSocket client interaction with the agent.
        """
        import websockets
        
        uri = "ws://localhost:8765/ws"
        
        async with websockets.connect(uri) as websocket:
            # Test agent message
            logger.info("Sending agent message...")
            agent_message = {
                "type": "agent_message",
                "content": "What is the current time?"
            }
            await websocket.send(json.dumps(agent_message))
            response = await websocket.recv()
            logger.info(f"Agent Message Response: {response}")

            # Test tool call
            logger.info("Sending tool call...")
            tool_call = {
                "type": "tool_call",
                "tool": "calculate_age",
                "args": {"birth_year": 1990}
            }
            await websocket.send(json.dumps(tool_call))
            response = await websocket.recv()
            logger.info(f"Tool Call Response: {response}")

    # Create tasks for communication server and client simulation
    communication_task = asyncio.create_task(agent.start_communication_server())
    client_task = asyncio.create_task(simulate_client_interaction())

    # Wait for tasks to complete
    await asyncio.gather(communication_task, client_task)

if __name__ == "__main__":
    asyncio.run(main())
