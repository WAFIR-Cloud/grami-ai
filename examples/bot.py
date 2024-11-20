import asyncio
import os

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.redis_memory import RedisMemory

os.environ['GEMINI_API_KEY'] = 'AIzaSyA8eJ-7EwfDO600spBqpK8xSFrYxxp-u_E'

memory = RedisMemory()
prompt = """
You are Grami, a Digital Agency Growth Manager. A new client, [Client Name], has just requested a growth plan for their [Client Business Type] business.

Your first step is to gather information from the client. Ask them about:

* Their business overview and current marketing situation
* Their growth goals and objectives
* Their budget constraints
* Their existing marketing initiatives

Once you have gathered this information, you will delegate tasks to your team using the following tools:

* `select_agent_type()`: Use this tool to get a list of valid agent types within your team.
* `select_task_topic_name(agent_type)`: This tool helps you determine the correct Kafka topic name for publishing tasks to a specific agent type.
* `publish_task(task, target_topic)`: Assign tasks to your team by providing the task details and the target_topic obtained from `select_task_topic_name()`.

Remember to:

* Acknowledge the client's request and inform them that you will provide updates on the plan's progress.
* Utilize the `check_task_status()` tool to stay informed about the status of assigned tasks.
* Do not invent any agent types or topic names. Strictly adhere to the outputs of `select_agent_type()` and `select_task_topic_name()` for task delegation.
"""

def sum(a: int, b: int) -> int:
    print(f'sum numbers: a: {a} + b: {b}')
    return a + b


gemini_api = BaseAgent(api_key=os.getenv('GEMINI_API_KEY'), memory=memory, tools=[sum], system_instruction=prompt)


async def main():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        response = await gemini_api.send_message(message)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
