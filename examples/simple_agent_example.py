import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import Agent
from grami.providers import GeminiProvider
from examples.tools import CalculatorTool

async def main():
    # Initialize Gemini Provider with the provided API key
    gemini_provider = GeminiProvider(
        api_key="AIzaSyCVcxzO6mSvZX-5j7T3pUqeJPto4FOO6v8"
    )

    # Create a simple math agent
    math_agent = Agent(
        name="SimpleMathAgent",
        role="Basic Mathematical Calculation Assistant",
        llm_provider=gemini_provider,
        tools=[CalculatorTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a helpful math assistant who can solve simple mathematical problems."
            }
        ]
    )

    # Demonstrate agent capabilities
    async def agent_demonstration():
        # Perform a calculation
        print("\n--- Math Calculation ---")
        math_response = await math_agent.send_message("Calculate the area of a circle with radius 5")
        print(math_response)

        # Demonstrate streaming
        print("\n--- Streaming Calculation Explanation ---")
        async for token in math_agent.stream_message("Explain how to calculate the area of a circle step by step"):
            print(token, end='', flush=True)
        print()  # New line after streaming

    # Run the agent demonstration
    await agent_demonstration()

if __name__ == "__main__":
    asyncio.run(main())
