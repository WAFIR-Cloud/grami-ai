import asyncio
import os
from typing import List, Any

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.memory import InMemoryAbstractMemory


def create_calculator_tools() -> List[Any]:
    """
    Create a list of calculator tools for the agent.
    
    Returns:
        List[Any]: A list of calculator function tools
    """
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(a: float, b: float) -> float:
        """Subtract the second number from the first."""
        return a - b

    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(a: float, b: float) -> float:
        """Divide the first number by the second."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    return [add, subtract, multiply, divide]


async def main():
    # Create an in-memory abstract memory for conversation history
    memory = InMemoryAbstractMemory()

    # Create calculator tools
    calculator_tools = create_calculator_tools()

    # Create a BaseAgent using Gemini LLM with custom tools
    agent = BaseAgent(
        llm_provider={
            'api_key': os.getenv('GOOGLE_AI_API_KEY', 'your_api_key_here'),
            'model_name': 'models/gemini-1.5-flash',
            'system_instruction': 'You are a helpful AI assistant with access to calculator tools.',
        },
        memory=memory,
        tools=calculator_tools
    )

    # Demonstrate tool usage and memory persistence
    math_queries = [
        "What is 5 plus 3?",
        "Can you multiply the previous result by 2?",
        "Now subtract 4 from that result.",
        "What calculations have we done so far?"
    ]

    for query in math_queries:
        response = await agent.send_message(query)
        print(f"Query: {query}")
        print(f"Response: {response}\n")


if __name__ == '__main__':
    asyncio.run(main())
