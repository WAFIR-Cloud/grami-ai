Getting Started
===============

This guide will help you create your first AI agent with Grami AI.

Creating Your First Agent
------------------------

Basic Agent Setup
^^^^^^^^^^^^^^^^

.. code-block:: python

   from grami.agent import Agent
   from grami.providers import GeminiProvider
   from grami.tools import CalculatorTool

   async def create_math_agent():
       math_agent = Agent(
           name="MathAssistant",
           role="Mathematical Problem Solver",
           llm_provider=GeminiProvider(api_key="your_api_key"),
           tools=[CalculatorTool()],
           initial_context=[
               {
                   "role": "system", 
                   "content": "You are a helpful math assistant."
               }
           ]
       )
       return math_agent

Sending Messages
^^^^^^^^^^^^^^^^

.. code-block:: python

   async def main():
       math_agent = await create_math_agent()
       
       # Send a simple message
       response = await math_agent.send_message(
           "Calculate the area of a circle with radius 5"
       )
       print(response)

       # Stream a detailed explanation
       async for token in math_agent.stream_message(
           "Explain how to calculate the area of a circle"
       ):
           print(token, end='', flush=True)

Key Concepts
------------

1. **Agents**: Customizable AI entities with specific roles
2. **Providers**: Language model interfaces (Gemini, OpenAI)
3. **Tools**: Extensible capabilities for agents
4. **Async Design**: Non-blocking, high-performance operations

Best Practices
--------------

- Always use an async context
- Manage API keys securely
- Choose appropriate tools for your agent's role
- Implement error handling

Next Steps
----------

- Explore advanced agent configurations
- Learn about custom tool development
- Understand streaming and message handling
