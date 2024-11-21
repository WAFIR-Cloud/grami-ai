import asyncio
from typing import Any, AsyncIterator, Optional

import aiokafka
from grami_ai.core.interfaces import AsyncKafkaIntegration

class AsyncKafkaProvider(AsyncKafkaIntegration):
    """
    Async Kafka integration with comprehensive message handling
    
    Supports:
    - Async message production
    - Async message consumption
    - Multiple topic support
    - Error handling
    """
    
    def __init__(
        self, 
        bootstrap_servers: str, 
        client_id: Optional[str] = None,
        group_id: Optional[str] = None
    ):
        """
        Initialize Kafka provider
        
        Args:
            bootstrap_servers: Comma-separated list of Kafka brokers
            client_id: Optional client identifier
            group_id: Optional consumer group identifier
        """
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id or 'grami-ai-kafka-client'
        self.group_id = group_id or 'grami-ai-consumer-group'
        
        self.producer: Optional[aiokafka.AIOKafkaProducer] = None
        self.consumer: Optional[aiokafka.AIOKafkaConsumer] = None

    async def _ensure_producer(self):
        """Ensure producer is initialized"""
        if not self.producer:
            self.producer = aiokafka.AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=self.client_id
            )
            await self.producer.start()

    async def _ensure_consumer(self, topic: str):
        """Ensure consumer is initialized"""
        if not self.consumer:
            self.consumer = aiokafka.AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                client_id=self.client_id
            )
            await self.consumer.start()

    async def produce(self, topic: str, message: Any) -> None:
        """
        Produce a message to a specified Kafka topic
        
        Args:
            topic: Kafka topic name
            message: Message to be sent (will be encoded)
        """
        await self._ensure_producer()
        try:
            # Convert message to bytes if not already
            if not isinstance(message, bytes):
                message = str(message).encode('utf-8')
            
            await self.producer.send_and_wait(topic, message)
        except Exception as e:
            # Log or handle Kafka production errors
            print(f"Kafka production error: {e}")

    async def consume(self, topic: str) -> AsyncIterator[str]:
        """
        Consume messages from a specified Kafka topic
        
        Args:
            topic: Kafka topic to consume from
        
        Yields:
            Decoded message strings
        """
        await self._ensure_consumer(topic)
        try:
            async for msg in self.consumer:
                yield msg.value.decode('utf-8')
        except Exception as e:
            # Log or handle Kafka consumption errors
            print(f"Kafka consumption error: {e}")
        finally:
            await self.consumer.stop()

    async def close(self):
        """
        Close all Kafka connections
        """
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
