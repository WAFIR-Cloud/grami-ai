import asyncio

from grami_ai.events.KafkaEvents import KafkaEvents

# async def create_task(task_id: str, agent_type: str, payload: Dict[str, Any]):
#     """Creates a new task and publishes it to a Kafka topic for the specified agent type."""
#     self.tasks[task_id] = "pending"
#     await self.kafka.publish(f"tasks_{agent_type}", {"task_id": task_id, "payload": payload})
#
#
# async def update_task_status( task_id: str, status: str):
#     """Updates the status of a task."""
#     self.tasks[task_id] = status
#     # Notify all agents of status changes if needed
#     await self.kafka.publish("task_updates", {"task_id": task_id, "status": status})

event_publisher = KafkaEvents()
import asyncio
import uuid


async def publish_task(agent_type: str, task_description: str, target_topic: str) -> str:
    """
    A tool function used to publish a task to the target Kafka topic.
    :param agent_type: The type of the Agent to send to.
    :param task_description: The query as a description of the task.
    :param target_topic: The topic to publish to.
    :return: A string response.
    """
    print(f'[*] publishing Task: {agent_type} {task_description} {target_topic}')
    task_id = str(uuid.uuid4())

    # Use the awaitable publish method directly
    await event_publisher.publish(f"tasks_{agent_type}", {
        "task_id": task_id,
        "payload": {'task_description': task_description}
    })

    return "Task published, waiting for agent to finish the task"


def publish_task_sync(agent_type: str, task_description: str, target_topic: str) -> str:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        task = asyncio.create_task(publish_task(agent_type, task_description, target_topic))
        print(task)
        return "Task scheduled, waiting for agent to finish the task"
    else:
        return loop.run_until_complete(publish_task(agent_type, task_description, target_topic))
