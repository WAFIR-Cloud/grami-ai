import json
import os
from typing import Any, Callable, Dict, Optional, Awaitable

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

# Environment configuration for Kafka
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("GRAMI_KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class KafkaEvents:
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumer: Optional[AIOKafkaConsumer] = None

    async def connect_producer(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self._producer.start()

    async def connect_consumer(self, topics: list[str], group_id: str):
        if self._consumer is None:
            self._consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                enable_auto_commit=True,
                auto_offset_reset="earliest",
            )
            await self._consumer.start()

    async def close_producer(self):
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def close_consumer(self):
        if self._consumer is not None:
            await self._consumer.stop()
            self._consumer = None

    async def publish(self, topic: str, event: Dict[str, Any]):
        await self.connect_producer()
        await self._producer.send_and_wait(topic, json.dumps(event).encode())

    async def consume(self, topics: list[str], group_id: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        await self.connect_consumer(topics, group_id)
        async for msg in self._consumer:
            event = json.loads(msg.value.decode())
            await callback(event)  # Process the event using the provided callback
