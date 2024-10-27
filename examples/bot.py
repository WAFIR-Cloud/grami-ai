import asyncio
import os
from grami_ai.gemini.api import GeminiAPI
from grami_ai.memory.redis_memory import RedisMemory
from grami_ai.tools.tool_wrapper import GramiTool

os.environ['GEMINI_API_KEY'] = 'AIzaSyCVcxzO6mSvZX-5j7T3pUqeJPto4FOO6v8'

memory = RedisMemory()


def sum(a: int, b: int) -> int:
    return a + b


sum_tool = GramiTool(sum)

gemini_api = GeminiAPI(api_key=os.getenv('GEMINI_API_KEY'), memory=memory, tools=[sum_tool])


async def main():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        response = await gemini_api.send_message(message, 'test-chat-id')
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
