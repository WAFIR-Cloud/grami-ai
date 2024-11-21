"""
Example of using GRAMI AI with Ollama for private AI deployment.

This example demonstrates how to use GRAMI with Ollama for fully private AI deployment,
ensuring all data processing happens locally within your infrastructure.
"""

import asyncio
import logging
from typing import Dict, Any

from grami_ai.agents import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools.base_tools import CalculatorTool, WebScraperTool
from grami_ai.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure tools with default implementations
calculator_tool = CalculatorTool()
web_scraper_tool = WebScraperTool()

async def process_sensitive_data(agent, sensitive_data):
    """
    Process sensitive data using the AI agent with tools.
    
    Args:
        agent (AsyncAgent): Configured AI agent
        sensitive_data (dict): Sensitive data to process
    
    Returns:
        str or None: Processed result or None if processing fails
    """
    # Modify the task to include tool configurations
    task = {
        'objective': 'Analyze private company data securely and locally',
        'tools': [
            {
                'name': 'calculator',
                'method': 'add',
                'args': [sensitive_data['company_financials']['revenue'], 
                         sensitive_data['company_financials']['expenses']]
            }
        ],
        'content': f"""
        Analyze the following private company data:
        Company Financials: {sensitive_data['company_financials']}
        Strategic Plans: {sensitive_data['strategic_plans']}
        
        Provide insights while ensuring data privacy and confidentiality.
        """
    }
    
    try:
        logger.info("Starting secure data analysis...")
        result = await agent.execute_task(task)
        logger.info("Data analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error processing sensitive data: {e}", exc_info=True)
        return None

async def main():
    """
    Main async function to demonstrate secure, local AI data processing.
    """
    try:
        # Initialize agent with Ollama
        agent = AsyncAgent(
            tools=[
                calculator_tool,  # For data calculations
                web_scraper_tool  # For public data enrichment
            ],
            memory=InMemoryAbstractMemory(),  # Keep memory local
            model="llama3.2:latest",  # Local Llama 3.2 model
            provider_config={
                "base_url": "http://localhost:11434",  # Local Ollama server
            }
        )
        
        # Simulated sensitive company data
        sensitive_data = {
            'company_financials': {
                'revenue': 1500000, 
                'expenses': 1200000, 
                'employees': 50
            },
            'strategic_plans': [
                'Expand to new markets',
                'Develop proprietary technology', 
                'Increase R&D investment'
            ]
        }
        
        logger.info("Processing sensitive data locally with Ollama...")
        result = await process_sensitive_data(agent, sensitive_data)
        
        if result:
            print("Analysis Result:", result)
        else:
            print("Data analysis failed.")
        
        logger.info("Analysis complete, all processing done locally")
    
    except Exception as e:
        logger.error(f"Critical error in main execution: {e}", exc_info=True)

if __name__ == '__main__':
    # Configure settings
    settings.configure(
        ollama_base_url="http://localhost:11434",
        log_level="INFO"
    )

    asyncio.run(main())
