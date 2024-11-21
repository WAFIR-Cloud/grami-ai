import asyncio
import os

from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.memory import InMemoryAbstractMemory


async def main():
    # Create an in-memory abstract memory for conversation history
    memory = InMemoryAbstractMemory()

    # Create a BaseAgent using Gemini LLM with a configuration dictionary
    agent = BaseAgent(
        llm_provider={
            'api_key': os.getenv('GOOGLE_AI_API_KEY', 'your_api_key_here'),
            'model_name': 'models/gemini-1.5-flash',
            'system_instruction': 'You are a helpful AI assistant.',
        },
        memory=memory
    )

    # Send a message and get a response
    response = await agent.send_message("Tell me a short joke about programming.")
    print("Agent's Response:", response)

    # Demonstrate memory persistence by sending a follow-up message
    follow_up_response = await agent.send_message("Can you explain the joke?")
    print("Follow-up Response:", follow_up_response)


if __name__ == '__main__':
    asyncio.run(main())
