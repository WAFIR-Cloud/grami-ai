"""
Basic example demonstrating the GRAMI framework with Gemini provider.
This example shows:
1. Basic agent setup without memory
2. Non-streaming message handling
3. Proper error handling and configuration
4. Custom safety and generation settings
"""

import asyncio
import os
import logging
from typing import List
from dotenv import load_dotenv

from grami.agents import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def setup_agent() -> AsyncAgent:
    """Initialize and configure the agent.
    
    Returns:
        AsyncAgent: Configured agent instance
    
    Raises:
        ValueError: If API key is not found
    """
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    
    # Custom generation config
    generation_config = {
        "temperature": 0.7,  # More creative
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2000,
    }
    
    # Custom safety settings (more permissive)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]
    
    # Initialize provider with custom configuration
    provider = GeminiProvider(
        api_key=api_key,
        model="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    # Create agent without memory
    agent = AsyncAgent(
        name="NoMemoryNoStreamingAgent",
        llm=provider,
        memory=None,  # Explicitly disable memory
        system_instructions="You are a helpful AI assistant focused on providing clear and concise responses."
    )
    
    return agent

async def process_messages(agent: AsyncAgent, messages: List[str]):
    """Process a list of messages and handle responses.
    
    Args:
        agent: Configured AsyncAgent instance
        messages: List of messages to process
    """
    for message in messages:
        try:
            logger.info(f"Sending message: {message}")
            response = await agent.send_message(message)
            logger.info(f"Received response: {response}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

async def main():
    """Main execution function."""
    try:
        # Setup agent
        agent = await setup_agent()
        
        # Test messages
        messages = [
            "What is artificial intelligence?",
            "Can you explain machine learning in simple terms?",
            "What are neural networks?",
            "How is AI being used in healthcare?",
        ]
        
        # Process messages
        await process_messages(agent, messages)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
