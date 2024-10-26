import asyncio
import os

from grami_ai.gemini.api import GeminiAPI
from grami_ai.memory.redis_memory import RedisMemory

os.environ['GEMINI_API_KEY'] = 'AIzaSyCVcxzO6mSvZX-5j7T3pUqeJPto4FOO6v8'

# Initialize memory
memory = RedisMemory()

# Initialize GeminiAPI with memory
gemini_api = GeminiAPI(memory=memory)

async def main():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        response = await gemini_api.send_message(message, 'f69ed4d5-0739-4a18-b79e-dcc0d1a095c0')
        print(response)

if __name__ == "__main__":
    asyncio.run(main())