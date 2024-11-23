import sys
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import Agent
from grami.providers import GeminiProvider
from examples.tools import WebSearchTool, WeatherTool, CalculatorTool

async def main():
    # Initialize Gemini Provider
    gemini_provider = GeminiProvider(
        api_key=os.getenv('GEMINI_API_KEY')
    )

    # Create an AI Agent with Gemini Provider and Tools
    agent = Agent(
        name="GeminiAssistant",
        role="Intelligent Multi-Tool Assistant",
        llm_provider=gemini_provider,
        tools=[
            WebSearchTool(),
            WeatherTool(),
            CalculatorTool()
        ],
        initial_context=[
            {
                "role": "system", 
                "content": (
                    "You are an intelligent AI assistant named GeminiAssistant. "
                    "When responding to user queries, you should proactively use "
                    "the available tools to provide the most accurate and helpful information. "
                    "Available tools:\n"
                    "1. WebSearchTool: Search for recent information online\n"
                    "2. WeatherTool: Get current weather information for a city\n"
                    "3. CalculatorTool: Perform mathematical calculations\n\n"
                    "Always explain which tool you're using and why, and provide "
                    "results in a clear, conversational manner."
                )
            }
        ]
    )

    # Demonstration scenarios
    async def interactive_demo():
        # Series of queries that should trigger different tool usages
        queries = [
            "What are the latest trends in AI for 2023?",
            "What's the current temperature in London?",
            "Can you help me calculate the area of a circle with radius 5?",
            "I want to compare the prices of the latest smartphones. Can you help me?"
        ]

        for query in queries:
            print("\n--- User Query ---")
            print(f"User: {query}")
            
            # Get the agent's response
            response = await agent.send_message(query)
            
            print("\n--- Agent Response ---")
            print(response)
            
            # Add a separator between queries
            print("\n" + "="*50)

    # Run the interactive demonstration
    await interactive_demo()

    # Demonstrate streaming
    async def streaming_demo():
        print("\n--- Streaming Demo ---")
        query = "Explain the concept of machine learning"
        print(f"User: {query}")
        
        print("\n--- Streamed Response ---")
        async for token in agent.stream_message(query):
            print(token, end='', flush=True)
        print()  # New line after streaming

    # Run the streaming demonstration
    await streaming_demo()

if __name__ == "__main__":
    asyncio.run(main())
