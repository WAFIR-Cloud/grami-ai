import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

class KafkaCommunicationBus:
    """
    Kafka-based communication bus for distributed agent communication.
    """
    
    def __init__(self, 
                 bootstrap_servers: str = 'localhost:9092', 
                 group_id: Optional[str] = None):
        """
        Initialize Kafka communication bus.
        
        Args:
            bootstrap_servers (str): Kafka bootstrap servers
            group_id (Optional[str]): Consumer group ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id or f'digital_marketing_agency_{id(self)}'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    
    async def publish_task(self, topic: str, task: Dict[str, Any]):
        """
        Publish a task to a specific Kafka topic.
        
        Args:
            topic (str): Kafka topic name
            task (Dict[str, Any]): Task details to publish
        """
        try:
            producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await producer.start()
            
            task_json = json.dumps(task).encode('utf-8')
            await producer.send_and_wait(topic, task_json)
            
            self.logger.info(f"Published task to topic {topic}")
        except Exception as e:
            self.logger.error(f"Error publishing task: {e}")
        finally:
            await producer.stop()
    
    async def consume_tasks(self, 
                             topics: list[str], 
                             handler: Callable[[Dict[str, Any]], Any]):
        """
        Consume tasks from specified topics and process them.
        
        Args:
            topics (list[str]): List of Kafka topics to consume
            handler (Callable): Function to handle incoming tasks
        """
        consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest'
        )
        
        await consumer.start()
        
        try:
            async for msg in consumer:
                try:
                    task = json.loads(msg.value.decode('utf-8'))
                    await handler(task)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON in message: {msg.value}")
                except Exception as e:
                    self.logger.error(f"Error processing task: {e}")
        
        except Exception as e:
            self.logger.error(f"Kafka consumer error: {e}")
        
        finally:
            await consumer.stop()
