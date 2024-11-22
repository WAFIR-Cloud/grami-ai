import os
import asyncio
import logging
from typing import Dict, Any

from grami_ai.agents import BaseMarketingAgent
from grami_ai.communication import KafkaCommunicationBus

class SocialMediaManagerService(BaseMarketingAgent):
    def __init__(self):
        super().__init__(
            name="Social Media Manager Service",
            system_prompt="Specialize in creating strategic Instagram social media plans"
        )
        
        # Kafka communication bus
        self.kafka_bus = KafkaCommunicationBus(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        )
    
    async def process_social_media_task(self, task: Dict[str, Any]):
        """
        Process social media strategy task for Instagram
        
        Expected task structure:
        {
            'task_id': str,
            'niche': str,
            'target_audience': str,
            'campaign_goals': list
        }
        """
        niche = task.get('niche', '')
        target_audience = task.get('target_audience', '')
        campaign_goals = task.get('campaign_goals', ['engagement', 'growth'])
        
        # Generate social media strategy using LLM
        strategy_prompt = f"""
        Develop a comprehensive Instagram social media strategy for {niche}:
        
        Target Audience: {target_audience}
        Campaign Goals: {', '.join(campaign_goals)}
        
        Strategy Components:
        1. Content pillars
        2. Posting frequency and timing
        3. Engagement tactics
        4. Growth hacking techniques
        5. Performance metrics to track
        """
        
        social_media_strategy = await self.generate_response(strategy_prompt)
        
        # Update task state
        await self.update_task_state(
            task.get('task_id', 'unknown'),
            'completed',
            {
                'social_media_strategy': social_media_strategy,
                'recommended_hashtags': self.toolkit.generate_hashtags(niche)
            }
        )
        
        return {'social_media_strategy': social_media_strategy}
    
    async def start_service(self):
        """Start the social media manager service"""
        logging.info("Social Media Manager Service starting...")
        
        # Subscribe to social media strategy tasks
        await self.kafka_bus.consume_tasks(
            topics=['social_media_strategy_tasks'],
            handler=self.process_social_media_task
        )

async def main():
    service = SocialMediaManagerService()
    await service.start_service()

if __name__ == '__main__':
    asyncio.run(main())
