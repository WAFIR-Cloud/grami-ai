import asyncio
import uuid

from grami_ai.events.KafkaEvents import KafkaEvents
from grami_ai.loggers.Logger import Logger

event_publisher = KafkaEvents()
logger = Logger()


def check_task_status():
    return """
    Task Still under process...
    """


def select_agent_type() -> list:
    """
    Provides a list of allowed agent types for Crew Remembers tasks.
    This function defines the valid agent types that can be used
    when creating tasks. It returns a list of strings, each representing
    a valid agent type.

    :return: A list of strings representing the allowed agent types.
    """
    logger.info('[*] selecting agent type')
    return [
        "copywriter",
        "content_creator_planner",
        "social_media_manager",
        "photographer_designer",
        "content_scheduler",
        "hashtags_market_researcher"
    ]

def select_task_topic_name(agent_type: str) -> str:
    """
    A tool used to select the proper Kafka topic name used by publish_task_sync()
    where target_topic is the topic selected from the string returned by this function.
    Each topic matches the type of the agent.

    :param agent_type: Type selected by select_agent_type() tool. This function
                         has a list with the exact same match of the agent type.
                         e.g., if agent_type is 'copywriter' then the topic is
                         'copywriter_consume_topic'.
    :return: A string with the Kafka topic name.
    """
    logger.info('[*] selecting task topic name')

    topic_mapping = {
        "copywriter": "copywriter_consume_topic",
        "content_creator_planner": "content_creator_planner_consume_topic",
        "social_media_manager": "social_media_manager_consume_topic",
        "photographer_designer": "photographer_designer_consume_topic",
        "content_scheduler": "content_scheduler_consume_topic",
        "hashtags_market_researcher": "hashtags_market_researcher_consume_topic"
    }

    try:
        return topic_mapping[agent_type]
    except KeyError:
        logger.error(f"Invalid agent_type: {agent_type}")
        # Handle the error appropriately, e.g., raise an exception or return a default value
        # raise ValueError(f"Invalid agent_type: {agent_type}")
        return "invalid agent type passed, make sure you select an existing one"


async def publish_task(agent_type: str, task_description: str, target_topic: str) -> str:
    """
    A tool function used to publish a task to the target Kafka topic.
    :param agent_type: The type of the Agent to send to.
    :param task_description: The query as a description of the task.
    :param target_topic: The topic to publish to. for topics fixed
    :return: A string response.
    """
    logger.info(f'[*] publishing Task: {agent_type} {task_description} {target_topic}')
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
        logger.debug(f'[*] publish task: {task}')
        return "Task scheduled, waiting for agent to finish the task"
    else:
        return loop.run_until_complete(publish_task(agent_type, task_description, target_topic))
