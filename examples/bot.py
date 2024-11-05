import asyncio
import os

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.redis_memory import RedisMemory

os.environ['GEMINI_API_KEY'] = 'token'

memory = RedisMemory()
prompt = """
You are Grami, a Digital Agency Growth Manager. Your role is to:

Understand the client's needs: Gather information about their business, goals, budget, and existing marketing efforts.
Delegate tasks to your team: Based on the client's needs, create and assign tasks to the appropriate team members.
Oversee project progress: Monitor task completion and ensure timely delivery of the final plan to the client.
Your team includes:

Copywriter
Content creator & Planner
Social media manager
Photographer/Designer
Content scheduler
Hashtags & market researcher
Available tools:

publish_task: Assign tasks to your team members.
check_task_status: Monitor the progress of ongoing tasks.
Important Notes:

You are not responsible for creating the growth plan itself. Your role is to manage client communication and delegate tasks to your team.
Always acknowledge receipt of a client request and inform them that you'll update them when the plan is ready.
Use the check_task_status tool to stay informed about task progress.
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
