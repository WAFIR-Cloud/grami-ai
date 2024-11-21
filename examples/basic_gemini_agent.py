"""
Example of using GRAMI AI with Google's Gemini for enterprise deployment.

This example demonstrates how to use GRAMI with Gemini for enterprise-grade
AI deployment with strong privacy controls and performance.
"""

import asyncio
import logging
from typing import Dict, Any, List

from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import WebScraperTool, CalculatorTool
from grami_ai.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnterpriseAgent:
    """Enterprise agent with privacy controls and monitoring."""
    
    def __init__(self):
        """Initialize enterprise agent."""
        self.agent = AsyncAgent(
            tools=[
                WebScraperTool(),   # For market research
                CalculatorTool()     # For financial analysis
            ],
            memory=InMemoryAbstractMemory(),
            model="gemini-pro",
            provider_config={
                "api_key": settings.google_api_key,
                "generation_config": {
                    "temperature": 0.3,  # More deterministic for enterprise use
                    "top_p": 0.9,
                    "max_tokens": 2000
                },
                "safety_settings": [
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_HIGH_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_HIGH_AND_ABOVE"
                    }
                ]
            }
        )
        self.audit_log = []
    
    async def analyze_market_data(
        self,
        market_sectors: List[str],
        timeframe: str
    ) -> Dict[str, Any]:
        """Analyze market data with privacy controls.
        
        Args:
            market_sectors: List of sectors to analyze
            timeframe: Time period for analysis
        
        Returns:
            Analysis results
        """
        try:
            # Log operation for audit
            self.audit_log.append({
                "operation": "market_analysis",
                "sectors": market_sectors,
                "timeframe": timeframe,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            # Execute analysis
            result = await self.agent.execute_task({
                "objective": "Market Analysis",
                "input": f"Analyze market trends for sectors {market_sectors} over {timeframe}",
                "constraints": [
                    "Only use publicly available data",
                    "Follow data privacy regulations",
                    "Maintain data residency requirements"
                ]
            })
            
            return {
                "analysis": result,
                "metadata": {
                    "sectors": market_sectors,
                    "timeframe": timeframe,
                    "privacy_compliant": True
                }
            }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise

async def main():
    # Initialize enterprise agent
    enterprise = EnterpriseAgent()
    
    # Example market analysis
    sectors = ["AI/ML", "Cloud Computing", "Cybersecurity"]
    timeframe = "last 6 months"
    
    logger.info(f"Analyzing {len(sectors)} sectors over {timeframe}...")
    
    try:
        result = await enterprise.analyze_market_data(sectors, timeframe)
        
        print("\nMarket Analysis Results:")
        print(f"Sectors: {', '.join(sectors)}")
        print(f"Timeframe: {timeframe}")
        print("\nAnalysis:")
        print(result["analysis"])
        
        # Show audit log
        print("\nAudit Log:")
        for entry in enterprise.audit_log:
            print(f"Operation: {entry['operation']}")
            print(f"Timestamp: {entry['timestamp']}")
            print("---")
            
    except Exception as e:
        logger.error(f"Failed to complete analysis: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure settings
    settings.configure(
        google_api_key="your-api-key-here",
        log_level="INFO"
    )
    
    # Run the example
    asyncio.run(main())
