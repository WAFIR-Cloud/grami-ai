import asyncio
import json
import logging
import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.core.base import BaseLLMProvider

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketExampleAgent(AsyncAgent):
    """
    Example WebSocket-enabled AI agent demonstrating communication capabilities.
    """
    
    def __init__(
        self, 
        name: str = "WebSocket Example Agent",
        llm: Optional[BaseLLMProvider] = None,
        system_instructions: Optional[str] = None
    ):
        """
        Initialize the WebSocket example agent.
        
        Args:
            name (str): Agent's name
            llm (Optional[BaseLLMProvider]): Language model provider
            system_instructions (Optional[str]): Initial system context
        """
        # Retrieve API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Use Gemini provider if no LLM is provided
        llm = llm or GeminiProvider(api_key=api_key)
        
        # Set default system instructions if not provided
        system_instructions = system_instructions or (
            "You are a helpful AI assistant that can answer questions "
            "and provide information through a WebSocket interface."
        )
        
        # Initialize the parent AsyncAgent
        super().__init__(
            name=name, 
            llm=llm, 
            system_instructions=system_instructions
        )
    
    async def send_message(self, message: str) -> str:
        """
        Process incoming messages and generate responses.
        
        Args:
            message (str): Incoming message to process
        
        Returns:
            str: Generated response
        """
        logger.info(f"Processing message: {message}")
        
        # Use the parent class's send_message method
        response = await super().send_message(message)
        logger.info(f"Generated response: {response}")
        
        return response

async def main():
    """
    Main function to demonstrate WebSocket communication setup.
    """
    # Create the WebSocket agent
    agent = WebSocketExampleAgent()
    
    # Setup communication interface
    communication_interface = await AsyncAgent.setup_communication(
        host='localhost', 
        port=8765
    )
    
    logger.info(f"WebSocket server started on {communication_interface['host']}:{communication_interface['port']}")
    
    # Keep the server running
    await communication_interface['server'].wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
