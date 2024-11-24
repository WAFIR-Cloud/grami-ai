Getting Started
===============

This guide will help you get started with GRAMI-AI, a powerful async-first AI agent framework.

Installation
------------

Install GRAMI-AI using pip:

.. code-block:: bash

   pip install grami-ai

Basic Usage
----------

Creating a Simple Agent
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import asyncio
   from grami.agents import AsyncAgent
   from grami.providers.gemini_provider import GeminiProvider

   async def main():
       # Initialize provider
       provider = GeminiProvider(api_key="YOUR_API_KEY")
       
       # Create agent
       agent = AsyncAgent(
           name="AssistantAI",
           llm=provider,
           system_instructions="You are a helpful digital assistant."
       )

       # Send a message
       response = await agent.send_message("Hello!")
       print(response)

   asyncio.run(main())

Using Different Providers
-----------------------

Gemini Provider
^^^^^^^^^^^^^^

.. code-block:: python

   from grami.providers.gemini_provider import GeminiProvider

   # Initialize with configuration
   provider = GeminiProvider(
       api_key="YOUR_API_KEY",
       model="gemini-pro",  # Optional
       generation_config={   # Optional
           "temperature": 0.7,
           "top_p": 0.8,
           "top_k": 40
       }
   )

Memory Management
---------------

LRU Memory
^^^^^^^^^

.. code-block:: python

   from grami.memory.lru import LRUMemory

   # Initialize memory
   memory = LRUMemory(capacity=100)

   # Add to provider
   provider.set_memory_provider(memory)

Redis Memory
^^^^^^^^^^^

.. code-block:: python

   from grami.memory.redis import RedisMemory

   # Initialize Redis memory
   memory = RedisMemory(
       host="localhost",
       port=6379,
       capacity=1000
   )

   # Add to provider
   provider.set_memory_provider(memory)

Streaming Capabilities
--------------------

Basic Streaming
^^^^^^^^^^^^^

.. code-block:: python

   async def stream_example():
       async for chunk in provider.stream_message("Generate a story"):
           print(chunk, end="", flush=True)

Streaming with Memory
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   async def stream_with_memory():
       # First message
       response = await provider.send_message("My name is Alice")
       
       # Stream follow-up (will remember context)
       async for chunk in provider.stream_message("What's my name?"):
           print(chunk, end="", flush=True)

Best Practices
-------------

1. **API Keys**: Always use environment variables for API keys
2. **Memory Management**: Choose appropriate memory provider based on your needs
3. **Error Handling**: Implement proper error handling for API calls
4. **Streaming**: Use streaming for long responses to improve user experience

Example: Complete Implementation
-----------------------------

.. code-block:: python

   import os
   import asyncio
   from dotenv import load_dotenv
   from grami.agents import AsyncAgent
   from grami.providers.gemini_provider import GeminiProvider
   from grami.memory.lru import LRUMemory

   async def main():
       # Load environment variables
       load_dotenv()
       
       # Initialize provider with memory
       provider = GeminiProvider(api_key=os.getenv("GEMINI_API_KEY"))
       memory = LRUMemory(capacity=100)
       provider.set_memory_provider(memory)
       
       # Create agent
       agent = AsyncAgent(
           name="AssistantAI",
           llm=provider,
           system_instructions="You are a helpful digital assistant."
       )
       
       # Regular message
       response = await agent.send_message("Remember that my name is Alice")
       print(f"Response: {response}")
       
       # Streaming follow-up
       print("\nStreaming response:")
       async for chunk in agent.stream_message("What's my name?"):
           print(chunk, end="", flush=True)

   if __name__ == "__main__":
       asyncio.run(main())

Next Steps
---------

- Explore advanced provider configurations
- Implement custom memory providers
- Add error handling and logging
- Integrate with your application
