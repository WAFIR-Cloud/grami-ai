import asyncio
import os
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

async def test_instagram_growth_campaign():
    """
    Simulate a complete Instagram growth campaign workflow
    by publishing a campaign request to Kafka and monitoring results
    """
    # Kafka configuration
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    # Create Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    
    # Prepare campaign request
    campaign_request = {
        'client_niche': 'Sustainable Fashion',
        'target_audience': 'Eco-conscious millennials and Gen Z',
        'campaign_goals': ['brand_awareness', 'engagement', 'follower_growth']
    }
    
    try:
        # Publish campaign request to Growth Manager
        await producer.send_and_wait(
            'growth_campaign_requests', 
            campaign_request
        )
        print("✅ Campaign request published successfully!")
        
        # Create consumers for each service's output
        consumers = [
            AIOKafkaConsumer(
                topic, 
                bootstrap_servers=bootstrap_servers,
                group_id=f'{topic}_test_group',
                auto_offset_reset='earliest'
            ) for topic in [
                'market_research_tasks',
                'content_creation_tasks', 
                'social_media_strategy_tasks'
            ]
        ]
        
        # Start consumers
        for consumer in consumers:
            await consumer.start()
        
        # Collect results from each service
        service_results = {}
        
        async def consume_results(consumer, topic):
            async for msg in consumer:
                task_result = json.loads(msg.value.decode('utf-8'))
                service_results[topic] = task_result
                print(f"📊 Received result from {topic}: {task_result}")
                await consumer.commit()
        
        # Run consumers concurrently
        await asyncio.gather(*[
            consume_results(consumer, topic) 
            for consumer, topic in zip(consumers, [
                'market_research_tasks',
                'content_creation_tasks', 
                'social_media_strategy_tasks'
            ])
        ])
    
    except Exception as e:
        print(f"❌ Error in campaign workflow: {e}")
    
    finally:
        # Clean up
        await producer.stop()
        for consumer in consumers:
            await consumer.stop()

def main():
    print("🚀 Instagram Growth Agency Campaign Test")
    print("--------------------------------------")
    asyncio.run(test_instagram_growth_campaign())

if __name__ == '__main__':
    main()
