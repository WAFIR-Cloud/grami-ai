import asyncio
import os
import math

from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Utility functions
def calculate_area(shape: str, *dimensions):
    """
    Calculate area of different shapes.
    
    Args:
        shape: Shape type (circle, rectangle, triangle)
        dimensions: Relevant dimensions for the shape
    
    Returns:
        Calculated area
    """
    if shape == 'circle' and len(dimensions) == 1:
        radius = dimensions[0]
        return math.pi * radius ** 2
    
    elif shape == 'rectangle' and len(dimensions) == 2:
        length, width = dimensions
        return length * width
    
    elif shape == 'triangle' and len(dimensions) == 2:
        base, height = dimensions
        return 0.5 * base * height
    
    raise ValueError(f"Invalid shape or dimensions for {shape}")

def generate_fibonacci(n: int):
    """
    Generate Fibonacci sequence up to n terms.
    
    Args:
        n: Number of Fibonacci terms to generate
    
    Returns:
        List of Fibonacci numbers
    """
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

class SimpleToolsAgent(AsyncAgent):
    """
    An agent with simple mathematical tools.
    """
    def __init__(
        self, 
        name: str = "SimpleToolsAgent",
        system_instructions: str = None
    ):
        """
        Initialize the agent with tools.
        
        Args:
            name (str, optional): Name of the agent.
            system_instructions (str, optional): Custom system instructions.
        """
        # Create a Gemini provider
        llm_provider = GeminiProvider(
            api_key=os.getenv('GEMINI_API_KEY')
        )
        
        # Set default system instructions
        system_instructions = system_instructions or (
            "You are a helpful AI assistant with mathematical tools. "
            "Available functions: calculate_area(shape, *dimensions), generate_fibonacci(n)"
        )
        
        # Initialize the parent AsyncAgent
        super().__init__(
            name=name, 
            llm=llm_provider,
            memory=LRUMemory(capacity=100),
            tools=[calculate_area, generate_fibonacci],
            system_instructions=system_instructions
        )

async def main():
    """
    Demonstrate the usage of the simple tools agent.
    """
    # Create the agent
    agent = SimpleToolsAgent()
    
    # Setup communication interface
    communication_interface = await agent.setup_communication(
        host='localhost', 
        port=0  # Dynamic port selection
    )
    
    print(f"Tools agent server started on {communication_interface['host']}:{communication_interface['port']}")
    
    # Keep the server running
    await communication_interface['server'].wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
