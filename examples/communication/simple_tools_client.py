import asyncio
import os

from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Utility functions (matching the agent's tools)
def calculate_area(shape: str, *dimensions):
    import math
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
    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

async def main():
    # Create a Gemini provider for the client
    llm_provider = GeminiProvider(
        api_key=os.getenv('GEMINI_API_KEY')
    )
    
    # Create an async agent
    agent = AsyncAgent(
        name="ToolsClient", 
        llm=llm_provider,
        memory=LRUMemory(capacity=10),
        tools=[calculate_area, generate_fibonacci]
    )
    
    # Test area calculation
    area_result = calculate_area('circle', 5)
    print("Circle Area (radius 5):", area_result)
    
    # Test Fibonacci generation
    fib_result = generate_fibonacci(10)
    print("Fibonacci (10 terms):", fib_result)
    
    # Test LLM query
    llm_response = await agent.send_message("What is the largest prime number less than 100?")
    print("LLM Response:", llm_response)

if __name__ == "__main__":
    asyncio.run(main())
