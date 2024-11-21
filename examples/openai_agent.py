"""
Example of using GRAMI AI with OpenAI (GPT-3.5/4) provider.
"""

import asyncio
import os
from typing import Dict, Any

from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool, WebScraperTool
from grami_ai.core.config import settings

async def main():
    # Initialize agent with OpenAI
    agent = AsyncAgent(
        tools=[CalculatorTool(), WebScraperTool()],
        memory=InMemoryAbstractMemory(),
        model="gpt-3.5-turbo",  # or "gpt-4" for GPT-4
        provider_config={
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    )
    
    # Example tasks
    tasks = [
        {
            "objective": "Calculate and explain",
            "input": "What is the square root of 144 divided by 3?"
        },
        {
            "objective": "Research and summarize",
            "input": "What are the latest developments in quantum computing?"
        }
    ]
    
    # Process tasks
    for task in tasks:
        print(f"\nProcessing task: {task['input']}")
        result = await agent.execute_task(task)
        print(f"Result: {result}")

if __name__ == "__main__":
    # Configure settings
    settings.configure(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        log_level="INFO"
    )
    
    # Run the example
    asyncio.run(main())
