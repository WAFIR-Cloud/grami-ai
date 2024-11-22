import os
import asyncio
import logging
import uuid
from typing import Dict, Any, List

from grami_ai.agents import BaseMarketingAgent
from grami_ai.communication import KafkaCommunicationBus

class GrowthManagerService(BaseMarketingAgent):
    def __init__(self):
        super().__init__(
            name="Growth Manager Service",
            system_prompt="Orchestrate and coordinate Instagram growth campaigns"
        )
        
        # Kafka communication bus
        self.kafka_bus = KafkaCommunicationBus(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        )
    
    async def process_growth_campaign(self, campaign_request: Dict[str, Any]):
        """
        Orchestrate a complete Instagram growth campaign
        
        Expected request structure:
        {
            'client_niche': str,
            'target_audience': str,
            'campaign_goals': list
        }
        """
        project_id = str(uuid.uuid4())
        niche = campaign_request.get('client_niche', '')
        target_audience = campaign_request.get('target_audience', '')
        campaign_goals = campaign_request.get('campaign_goals', ['growth'])
        
        # Distribute tasks to different services
        tasks = [
            {
                'task_id': f'{project_id}_market_research',
                'type': 'market_research',
                'niche': niche,
                'target_market': target_audience
            },
            {
                'task_id': f'{project_id}_content_strategy',
                'type': 'content_strategy',
                'niche': niche,
                'target_audience': target_audience
            },
            {
                'task_id': f'{project_id}_social_media_strategy',
                'type': 'social_media_strategy',
                'niche': niche,
                'target_audience': target_audience,
                'campaign_goals': campaign_goals
            }
        ]
        
        # Publish tasks to respective Kafka topics
        task_results = {}
        
        for task in tasks:
            topic_map = {
                'market_research': 'market_research_tasks',
                'content_strategy': 'content_creation_tasks',
                'social_media_strategy': 'social_media_strategy_tasks'
            }
            
            await self.kafka_bus.publish_task(
                topic_map.get(task['type'], 'default_tasks'), 
                task
            )
            
            # Simulate task processing (in real scenario, use async callbacks)
            await asyncio.sleep(2)
            
            # Placeholder for task result retrieval
            task_results[task['type']] = f"Processed {task['type']} for {niche}"
        
        # Compile final campaign strategy
        campaign_strategy = await self.generate_response(
            f"""
            Compile a comprehensive Instagram growth campaign strategy:
            
            Niche: {niche}
            Target Audience: {target_audience}
            Campaign Goals: {', '.join(campaign_goals)}
            
            Integrate insights from:
            1. Market Research
            2. Content Strategy
            3. Social Media Strategy
            
            Generate a cohesive, actionable growth plan.
            """
        )
        
        # Update project state
        await self.update_task_state(
            project_id,
            'completed',
            {
                'campaign_strategy': campaign_strategy,
                'task_results': task_results
            }
        )
        
        return {
            'project_id': project_id,
            'campaign_strategy': campaign_strategy
        }
    
    async def start_service(self):
        """Start the growth manager service"""
        logging.info("Growth Manager Service starting...")
        
        # Subscribe to growth campaign requests
        await self.kafka_bus.consume_tasks(
            topics=['growth_campaign_requests'],
            handler=self.process_growth_campaign
        )

async def main():
    service = GrowthManagerService()
    await service.start_service()

if __name__ == '__main__':
    asyncio.run(main())
