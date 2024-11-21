"""
Basic example of creating and using a GRAMI AI agent.
"""

import asyncio
from typing import Dict, Any, List

from grami_ai.agent import BaseAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool, WebSearchTool
from grami_ai.core.config import settings
from grami_ai.core.constants import Priority

class ResearchAgent(BaseAgent):
    """A simple research agent that can perform calculations and web searches."""
    
    async def initialize(self) -> None:
        """Initialize agent with tools and memory."""
        self.memory = InMemoryAbstractMemory()
        self.tools = [
            CalculatorTool(),
            WebSearchTool()
        ]
        self.name = "Research Assistant"
        self.description = "I can help with calculations and web searches."

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a given task using available tools."""
        query = task.get("query", "")
        
        # First try calculation if it looks like a math query
        if any(op in query for op in ["+", "-", "*", "/", "="]):
            try:
                result = await self.execute_tool(
                    "calculator",
                    {"expression": query}
                )
                return {
                    "result": f"Calculation result: {result}",
                    "tool_used": "calculator"
                }
            except Exception:
                pass  # Not a valid calculation, try web search
        
        # Perform web search
        result = await self.execute_tool(
            "web_search",
            {"query": query}
        )
        
        # Store result in memory
        await self.memory.add_item(
            f"search_{task.get('id', 'default')}",
            {"query": query, "result": result}
        )
        
        return {
            "result": result,
            "tool_used": "web_search"
        }

async def main():
    # Initialize agent
    agent = ResearchAgent()
    await agent.initialize()
    
    # Create some example tasks
    tasks = [
        {
            "id": "calc_1",
            "query": "2 + 2 * 3",
            "priority": Priority.HIGH
        },
        {
            "id": "search_1",
            "query": "latest developments in AI",
            "priority": Priority.NORMAL
        }
    ]
    
    # Process tasks
    for task in tasks:
        print(f"\nProcessing task: {task['id']}")
        result = await agent.process_task(task)
        print(f"Result: {result}")
        
        # Retrieve from memory
        if result.get("tool_used") == "web_search":
            memory_item = await agent.memory.get_items(f"search_{task['id']}")
            print(f"Memory entry: {memory_item}")

if __name__ == "__main__":
    # Set up logging
    settings.configure(log_level="INFO")
    
    # Run the example
    asyncio.run(main())
