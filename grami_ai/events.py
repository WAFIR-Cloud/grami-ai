import asyncio
import json
import os
from typing import Any, AsyncIterable, Callable, Dict, Optional, Awaitable, List, Set
from collections import defaultdict

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from .core.interfaces import AsyncKafkaIntegration

# Configuration using environment variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("GRAMI_KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


class KafkaEvents(AsyncKafkaIntegration):
    """Implementation of AsyncKafkaIntegration using aiokafka."""
    
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._subscribers: Dict[str, Set[Callable[[Any], Awaitable[None]]]] = defaultdict(set)
        self._consumer_task: Optional[asyncio.Task] = None

    async def connect_producer(self) -> None:
        """Connect to Kafka as a producer."""
        if self._producer is None:
            try:
                self._producer = AIOKafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode()
                )
                await self._producer.start()
            except KafkaError as e:
                raise ConnectionError(f"Failed to connect to Kafka as producer: {e}")

    async def connect_consumer(self, topics: List[str]) -> None:
        """Connect to Kafka as a consumer for specified topics."""
        if self._consumer is None or set(self._consumer.subscription()) != set(topics):
            try:
                if self._consumer:
                    await self.close_consumer()
                
                self._consumer = AIOKafkaConsumer(
                    *topics,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id="grami_agent_group",
                    enable_auto_commit=True,
                    auto_offset_reset="latest",
                    value_deserializer=lambda v: json.loads(v.decode())
                )
                await self._consumer.start()
                
                # Start message processing loop
                if self._consumer_task is None:
                    self._consumer_task = asyncio.create_task(self._process_messages())
            except KafkaError as e:
                raise ConnectionError(f"Failed to connect to Kafka as consumer: {e}")

    async def close_producer(self) -> None:
        """Close the Kafka producer connection."""
        if self._producer is not None:
            try:
                await self._producer.stop()
            except KafkaError as e:
                raise ConnectionError(f"Failed to close Kafka producer: {e}")
            finally:
                self._producer = None

    async def close_consumer(self) -> None:
        """Close the Kafka consumer connection."""
        if self._consumer is not None:
            try:
                if self._consumer_task:
                    self._consumer_task.cancel()
                    try:
                        await self._consumer_task
                    except asyncio.CancelledError:
                        pass
                    self._consumer_task = None
                await self._consumer.stop()
            except KafkaError as e:
                raise ConnectionError(f"Failed to close Kafka consumer: {e}")
            finally:
                self._consumer = None

    async def publish(self, topic: str, message: Any) -> None:
        """
        Publish a message to a Kafka topic.
        
        Args:
            topic: Target Kafka topic
            message: Message to publish (will be JSON serialized)
        """
        try:
            await self.connect_producer()
            await self._producer.send_and_wait(topic, message)
        except KafkaError as e:
            raise KafkaError(f"Failed to publish message to topic '{topic}': {e}")

    async def subscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]) -> None:
        """
        Subscribe to a Kafka topic with a callback function.
        
        Args:
            topic: Topic to subscribe to
            callback: Async function to handle received messages
        """
        self._subscribers[topic].add(callback)
        await self.connect_consumer([topic])

    async def unsubscribe(self, topic: str) -> None:
        """
        Unsubscribe all callbacks from a topic.
        
        Args:
            topic: Topic to unsubscribe from
        """
        if topic in self._subscribers:
            del self._subscribers[topic]
            if self._consumer and not self._subscribers:
                await self.close_consumer()

    async def _process_messages(self) -> None:
        """Internal message processing loop."""
        try:
            async for message in self._consumer:
                topic = message.topic
                if topic in self._subscribers:
                    for callback in self._subscribers[topic]:
                        try:
                            await callback(message.value)
                        except Exception as e:
                            print(f"Error in subscriber callback: {e}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in message processing loop: {e}")


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
