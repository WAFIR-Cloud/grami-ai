import asyncio
import os
from grami_ai.gemini.api import GeminiAPI
from grami_ai.memory.redis_memory import RedisMemory

os.environ['GEMINI_API_KEY'] = 'AIzaSyCVcxzO6mSvZX-5j7T3pUqeJPto4FOO6v8'

memory = RedisMemory()
gemini_api = GeminiAPI(api_key=os.getenv('GEMINI_API_KEY'), memory=memory)


async def main():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        response = await gemini_api.send_message(message, 'test-chat-id')
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
