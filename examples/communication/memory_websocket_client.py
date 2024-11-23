import asyncio
import logging
import os
from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MemoryWebSocketClient(AsyncAgent):
    """
    A client agent for sending queries.
    """
    async def send_query(self, query: str):
        """
        Send a query and return the response.
        
        Args:
            query (str): The query to send.
        
        Returns:
            str: The response from the agent.
        """
        return await self.send_message(query)

async def main():
    """
    Demonstrate the usage of the memory WebSocket client.
    """
    # Create a Gemini provider
    llm_provider = GeminiProvider(
        api_key=os.getenv('GEMINI_API_KEY')
    )
    
    # Create a client agent
    client = MemoryWebSocketClient(
        name="QueryClient", 
        llm=llm_provider
    )
    
    # Example queries
    queries = [
        "Tell me a short story about a curious cat.",
        "What was the cat's name?",
        "Describe the cat's adventure in more detail."
    ]
    
    # Send each query and print the response
    for query in queries:
        try:
            response = await client.send_query(query)
            print(f"Query: {query}\nResponse: {response}\n")
        except Exception as e:
            print(f"Error sending query '{query}': {e}")

if __name__ == "__main__":
    asyncio.run(main())
