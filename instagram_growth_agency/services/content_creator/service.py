import os
import asyncio
import logging
from typing import Dict, Any

from grami_ai.agents import BaseMarketingAgent
from grami_ai.communication import KafkaCommunicationBus

class ContentCreatorService(BaseMarketingAgent):
    def __init__(self):
        super().__init__(
            name="Content Creator Service",
            system_prompt="Specialize in creating compelling Instagram content"
        )
        
        # Kafka communication bus
        self.kafka_bus = KafkaCommunicationBus(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        )
    
    async def process_content_task(self, task: Dict[str, Any]):
        """
        Process content creation task for Instagram
        
        Expected task structure:
        {
            'task_id': str,
            'niche': str,
            'target_audience': str,
            'content_type': str  # e.g., 'reel', 'post', 'story'
        }
        """
        niche = task.get('niche', '')
        content_type = task.get('content_type', 'post')
        
        # Generate content using LLM
        content_prompt = f"""
        Create an engaging Instagram {content_type} for {niche}:
        - Develop a creative and platform-specific content piece
        - Include trending hashtags
        - Ensure high engagement potential
        """
        
        content = await self.generate_response(content_prompt)
        
        # Update task state
        await self.update_task_state(
            task.get('task_id', 'unknown'),
            'completed',
            {
                'content': content,
                'hashtags': self.toolkit.generate_hashtags(niche)
            }
        )
        
        return {'content': content}
    
    async def start_service(self):
        """Start the content creator service"""
        logging.info("Content Creator Service starting...")
        
        # Subscribe to content creation tasks
        await self.kafka_bus.consume_tasks(
            topics=['content_creation_tasks'],
            handler=self.process_content_task
        )

async def main():
    service = ContentCreatorService()
    await service.start_service()

if __name__ == '__main__':
    asyncio.run(main())
