import asyncio
import logging
import os

from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MemoryWebSocketAgent(AsyncAgent):
    """
    A memory-enabled agent for WebSocket communication.
    """
    def __init__(
        self, 
        name: str = "MemoryAgent",
        system_instructions: str = None
    ):
        """
        Initialize the memory-enabled agent.
        
        Args:
            name (str, optional): Name of the agent. Defaults to "MemoryAgent".
            system_instructions (str, optional): Custom system instructions.
        """
        # Retrieve API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize memory 
        memory = LRUMemory(capacity=100)
        
        # Initialize provider
        llm = GeminiProvider(api_key=api_key)
        
        # Set default system instructions
        system_instructions = system_instructions or (
            "You are a helpful AI assistant that provides informative and engaging responses."
        )
        
        # Initialize the parent AsyncAgent
        super().__init__(
            name=name, 
            llm=llm, 
            memory=memory,
            system_instructions=system_instructions
        )

async def main():
    """
    Main function to demonstrate memory agent communication.
    """
    # Create the memory-enabled agent
    agent = MemoryWebSocketAgent()
    
    # Setup communication interface
    communication_interface = await agent.setup_communication(
        host='localhost', 
        port=0  # Dynamic port selection
    )
    
    logger.info(f"Memory agent server started on {communication_interface['host']}:{communication_interface['port']}")
    
    # Keep the server running
    await communication_interface['server'].wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
