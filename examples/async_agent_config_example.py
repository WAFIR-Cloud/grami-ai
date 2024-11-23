import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import AsyncAgent

async def main():
    # Create an AsyncAgent with initial configuration
    research_agent = AsyncAgent(
        name="ResearchAssistant",
        description="An AI agent for conducting research",
        role="Research Analyst",
        config={
            "max_sources": 10,
            "confidence_threshold": 0.75,
            "verbose": True
        }
    )

    # Print initial configuration
    print(f"Agent Name: {research_agent.name}")
    print(f"Initial Configuration: {research_agent.config}")

    # Update configuration dynamically
    await research_agent.update_config({
        "domain_focus": "Technology",
        "max_sources": 15
    })

    # Print updated configuration
    print(f"Updated Configuration: {research_agent.config}")

    # Demonstrate async context management
    async with research_agent:
        print("Working within the agent's async context")
        # Simulate some async work
        await asyncio.sleep(1)
        print("Async context work completed")

if __name__ == "__main__":
    asyncio.run(main())
