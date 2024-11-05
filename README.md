# grami-ai

Open-source Python library for building AI-powered Instagram marketing tools with Google Gemini.

**grami-ai** provides a set of tools and abstractions to simplify the development of intelligent Instagram bots and marketing applications. It leverages the power of Google Gemini for advanced AI capabilities and integrates seamlessly with other essential services like Redis and Amazon S3.

## Features

* **Shared Memory Wrapper:** A convenient interface for managing shared state in Redis, enabling efficient communication and data sharing between different components of your application.
* **Event Publisher/Consumer (Coming Soon):**  Asynchronous communication between AI agents using Kafka. (This will be added when you implement `events.py`)
* **Gemini API Wrapper (Coming Soon):**  Simplified interactions with the Gemini API for tasks like content generation, image analysis, and more. (This will be added when you implement `gemini.py`)
* **S3 Wrapper (Coming Soon):**  Easy-to-use functions for media upload, storage, and retrieval with Amazon S3. (This will be added when you implement `s3.py`)

## Installation

```bash
pip install grami-ai
```
## example

```python
import asyncio
import os
from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.redis_memory import RedisMemory

# Set your Gemini API key
os.environ['GEMINI_API_KEY'] = 'YOUR_GEMINI_API_KEY'

# Initialize memory and set up your agent's prompt
memory = RedisMemory()
prompt = """
You are Grami, a Digital Agency Growth Manager. Your role is to:

Understand the client's needs: Gather information about their business, goals, budget, and existing marketing efforts.
Delegate tasks to your team: Based on the client's needs, create and assign tasks to the appropriate team members.
Oversee project progress: Monitor task completion and ensure timely delivery of the final plan to the client.

Your team includes:
- Copywriter
- Content creator & Planner
- Social media manager
- Photographer/Designer
- Content scheduler
- Hashtags & market researcher

Available tools:
- publish_task: Assign tasks to your team members.
- check_task_status: Monitor the progress of ongoing tasks.

Important Notes:
- You are not responsible for creating the growth plan itself. Your role is to manage client communication and delegate tasks to your team.
- Always acknowledge receipt of a client request and inform them that you'll update them when the plan is ready.
- Use the check_task_status tool to stay informed about task progress.
"""

# Example tool function
def sum(a: int, b: int) -> int:
    print(f'sum numbers: a: {a} + b: {b}')
    return a + b

# Initialize the agent with API key, memory, and tools
gemini_api = BaseAgent(api_key=os.getenv('GEMINI_API_KEY'), memory=memory, tools=[sum], system_instruction=prompt)

# Run the agent
async def main():
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        response = await gemini_api.send_message(message)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Licence
MIT License

Copyright (c) 2024 WAFIR Cloud LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
