import os
import asyncio
import logging
from typing import Dict, Any

from grami_ai.agents import BaseMarketingAgent
from grami_ai.communication import KafkaCommunicationBus

class MarketResearcherService(BaseMarketingAgent):
    def __init__(self):
        super().__init__(
            name="Market Researcher Service",
            system_prompt="Specialize in comprehensive market and competitive analysis for Instagram marketing"
        )
        
        # Kafka communication bus
        self.kafka_bus = KafkaCommunicationBus(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        )
    
    async def process_market_research_task(self, task: Dict[str, Any]):
        """
        Process market research task for Instagram niche
        
        Expected task structure:
        {
            'task_id': str,
            'niche': str,
            'target_market': str
        }
        """
        niche = task.get('niche', '')
        target_market = task.get('target_market', '')
        
        # Perform web search for market insights
        market_insights = await self.toolkit.web_search(f"Instagram marketing trends for {niche}")
        competitive_research = await self.toolkit.web_search(f"Top competitors in {niche} on Instagram")
        
        # Generate comprehensive market research report
        research_prompt = f"""
        Comprehensive Market Research Report for {niche} on Instagram:
        
        Target Market: {target_market}
        
        Market Insights:
        {market_insights}
        
        Competitive Landscape:
        {competitive_research}
        
        Research Components:
        1. Market size and growth potential
        2. Target audience demographics
        3. Competitive analysis
        4. Emerging trends
        5. Potential growth strategies
        """
        
        market_research_report = await self.generate_response(research_prompt)
        
        # Update task state
        await self.update_task_state(
            task.get('task_id', 'unknown'),
            'completed',
            {
                'market_research_report': market_research_report,
                'market_insights': market_insights,
                'competitive_landscape': competitive_research
            }
        )
        
        return {'market_research_report': market_research_report}
    
    async def start_service(self):
        """Start the market researcher service"""
        logging.info("Market Researcher Service starting...")
        
        # Subscribe to market research tasks
        await self.kafka_bus.consume_tasks(
            topics=['market_research_tasks'],
            handler=self.process_market_research_task
        )

async def main():
    service = MarketResearcherService()
    await service.start_service()

if __name__ == '__main__':
    asyncio.run(main())
