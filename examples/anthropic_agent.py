"""
Example of using GRAMI AI with Anthropic (Claude) provider.
"""

import asyncio
import os
from typing import Dict, Any

from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool, WebScraperTool
from grami_ai.core.config import settings

async def main():
    # Initialize agent with Anthropic
    agent = AsyncAgent(
        tools=[CalculatorTool(), WebScraperTool()],
        memory=InMemoryAbstractMemory(),
        model="claude-2.1",  # or "claude-instant-1" for faster responses
        provider_config={
            "api_key": os.getenv("ANTHROPIC_API_KEY")
        }
    )
    
    # Example tasks demonstrating Claude's capabilities
    tasks = [
        {
            "objective": "Complex analysis",
            "input": "Analyze the environmental impact of electric vehicles compared to traditional vehicles. Consider manufacturing, usage, and disposal."
        },
        {
            "objective": "Code review",
            "input": """Review this Python code for best practices and security:
            def process_user_data(data):
                user_id = data.get('id')
                if user_id:
                    query = f"SELECT * FROM users WHERE id = {user_id}"
                    return execute_query(query)
                return None
            """
        }
    ]
    
    # Process tasks
    for task in tasks:
        print(f"\nProcessing task: {task['objective']}")
        result = await agent.execute_task(task)
        print(f"Result: {result}")

if __name__ == "__main__":
    # Configure settings
    settings.configure(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        log_level="INFO"
    )
    
    # Run the example
    asyncio.run(main())
