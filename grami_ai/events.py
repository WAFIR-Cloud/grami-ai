import asyncio
import json
import os
from typing import Any, AsyncIterable, Callable, Dict, Optional, Awaitable

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

# Configuration using environment variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("GRAMI_KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class KafkaEvents:
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumer: Optional[AIOKafkaConsumer] = None

    async def connect_producer(self):
        if self._producer is None:
            try:
                self._producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers
                )
                await self._producer.start()
            except KafkaError as e:
                raise ConnectionError(f"Failed to connect to Kafka as producer: {e}")

    async def connect_consumer(self, topics: list[str], group_id: str):
        if self._consumer is None:
            try:
                self._consumer = AIOKafkaConsumer(
                    *topics,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id=group_id,
                    enable_auto_commit=True,
                    auto_offset_reset="earliest",
                )
                await self._consumer.start()
            except KafkaError as e:
                raise ConnectionError(f"Failed to connect to Kafka as consumer: {e}")

    async def close_producer(self):
        if self._producer is not None:
            try:
                await self._producer.stop()
            except KafkaError as e:
                raise ConnectionError(f"Failed to close Kafka producer: {e}")
            finally:
                self._producer = None

    async def close_consumer(self):
        if self._consumer is not None:
            try:
                await self._consumer.stop()
            except KafkaError as e:
                raise ConnectionError(f"Failed to close Kafka consumer: {e}")
            finally:
                self._consumer = None

    async def publish(self, topic: str, event: Dict[str, Any]):
        try:
            await self.connect_producer()
            await self._producer.send_and_wait(
                topic, json.dumps(event).encode()
            )
        except KafkaError as e:
            raise KafkaError(f"Failed to publish event to topic '{topic}': {e}")

    async def consume(
            self, topics: list[str], group_id: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]
    ) -> AsyncIterable[Dict[str, Any]]:
        await self.connect_consumer(topics, group_id)
        try:
            async for msg in self._consumer:
                event = json.loads(msg.value.decode())
                await callback(event)  # Await the callback here
                yield event
        except KafkaError as e:
            raise KafkaError(f"Failed to consume events from topics '{topics}': {e}")


# Create a global instance of KafkaEvents
events = KafkaEvents()


async def handle_new_user(event):
    # Process the new user event
    print(f"New user event received: {event}")


async def main():
    async for event in events.consume(["new_users"], "my_group", handle_new_user):
        print(f"Processed event: {event}")


if __name__ == "__main__":
    asyncio.run(main())
