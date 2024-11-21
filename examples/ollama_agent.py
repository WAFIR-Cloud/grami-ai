"""
Example of using GRAMI AI with Ollama for private AI deployment.

This example demonstrates how to use GRAMI with Ollama for fully private AI deployment,
ensuring all data processing happens locally within your infrastructure.
"""

import asyncio
import logging
from typing import Dict, Any

from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool, WebScraperTool
from grami_ai.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_sensitive_data(agent: AsyncAgent, data: Dict[str, Any]) -> str:
    """Process sensitive data privately using Ollama.
    
    Args:
        agent: Configured GRAMI agent
        data: Sensitive data to process
    
    Returns:
        Processed result
    """
    try:
        result = await agent.execute_task({
            "objective": "Process sensitive data",
            "input": f"Analyze this private data: {data}",
            "constraints": [
                "Keep all processing local",
                "Do not share or store data externally",
                "Follow data privacy guidelines"
            ]
        })
        return result
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise

async def main():
    # Initialize agent with Ollama
    agent = AsyncAgent(
        tools=[
            CalculatorTool(),  # For data calculations
            WebScraperTool()   # For public data enrichment
        ],
        memory=InMemoryAbstractMemory(),  # Keep memory local
        model="ollama/llama2",  # Local Llama 2 model
        provider_config={
            "base_url": "http://localhost:11434",  # Local Ollama server
            "generation_config": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
    )
    
    # Example sensitive data
    sensitive_data = {
        "company_financials": {
            "revenue": 1500000,
            "expenses": 1200000,
            "employees": 50
        },
        "strategic_plans": [
            "Expand to new markets",
            "Develop proprietary technology",
            "Increase R&D investment"
        ]
    }
    
    # Process data privately
    logger.info("Processing sensitive data locally with Ollama...")
    result = await process_sensitive_data(agent, sensitive_data)
    logger.info("Analysis complete, all processing done locally")
    print("\nAnalysis Result:")
    print(result)

if __name__ == "__main__":
    # Configure settings
    settings.configure(
        ollama_base_url="http://localhost:11434",
        log_level="INFO"
    )
    
    # Run the example
    asyncio.run(main())
