API Reference
=============

This document provides detailed information about GRAMI-AI's API components.

Providers
--------

GeminiProvider
^^^^^^^^^^^^^

.. code-block:: python

   class GeminiProvider:
       """Provider for Google's Gemini API."""
       
       def __init__(
           self,
           api_key: str,
           model: str = "gemini-pro",
           generation_config: Optional[Dict] = None,
           safety_settings: Optional[List[Dict[str, str]]] = None
       ):
           """Initialize the Gemini provider.
           
           Args:
               api_key: Gemini API key
               model: Model name (default: gemini-pro)
               generation_config: Optional generation configuration
               safety_settings: Optional safety settings
           """

       async def send_message(
           self,
           message: Union[str, Dict[str, str]],
           context: Optional[Dict] = None
       ) -> str:
           """Send a message and get a response.
           
           Args:
               message: User message (string or dictionary)
               context: Optional context
           
           Returns:
               Model's response as string
           """

       async def stream_message(
           self,
           message: Union[str, Dict[str, str]],
           context: Optional[Dict] = None
       ):
           """Stream a message response.
           
           Args:
               message: User message (string or dictionary)
               context: Optional context
           
           Yields:
               Response tokens as they are generated
           """

Memory Providers
--------------

LRUMemory
^^^^^^^^^

.. code-block:: python

   class LRUMemory:
       """LRU-based memory provider for conversation history."""
       
       def __init__(self, capacity: int = 100):
           """Initialize LRU memory.
           
           Args:
               capacity: Maximum number of messages to store
           """

       async def add_message(self, message: Dict[str, Any]):
           """Add a message to memory.
           
           Args:
               message: Message dictionary with role and content
           """

       def get_messages(self) -> List[Dict[str, Any]]:
           """Get all stored messages.
           
           Returns:
               List of message dictionaries
           """

RedisMemory
^^^^^^^^^^

.. code-block:: python

   class RedisMemory:
       """Redis-based memory provider for distributed storage."""
       
       def __init__(
           self,
           host: str = "localhost",
           port: int = 6379,
           capacity: int = 1000
       ):
           """Initialize Redis memory.
           
           Args:
               host: Redis host
               port: Redis port
               capacity: Maximum number of messages
           """

AsyncAgent
---------

.. code-block:: python

   class AsyncAgent:
       """Async-first AI agent for handling conversations."""
       
       def __init__(
           self,
           name: str,
           llm: BaseLLMProvider,
           memory: Optional[BaseMemoryProvider] = None,
           system_instructions: Optional[str] = None
       ):
           """Initialize async agent.
           
           Args:
               name: Agent name
               llm: Language model provider
               memory: Optional memory provider
               system_instructions: Optional system instructions
           """

       async def send_message(
           self,
           message: str,
           context: Optional[Dict] = None
       ) -> str:
           """Send a message to the agent.
           
           Args:
               message: User message
               context: Optional context
           
           Returns:
               Agent's response
           """

       async def stream_message(
           self,
           message: str,
           context: Optional[Dict] = None
       ):
           """Stream a message response from the agent.
           
           Args:
               message: User message
               context: Optional context
           
           Yields:
               Response tokens as they are generated
           """

Configuration
-----------

Generation Config
^^^^^^^^^^^^^^^

.. code-block:: python

   {
       "temperature": 0.7,    # Controls randomness (0.0 to 1.0)
       "top_p": 0.8,         # Nucleus sampling parameter
       "top_k": 40,          # Top-k sampling parameter
       "max_tokens": 1000    # Maximum response length
   }

Safety Settings
^^^^^^^^^^^^^

.. code-block:: python

   [
       {
           "category": "HARM_CATEGORY_HARASSMENT",
           "threshold": "BLOCK_NONE"
       },
       {
           "category": "HARM_CATEGORY_HATE_SPEECH",
           "threshold": "BLOCK_ONLY_HIGH"
       }
   ]

Examples
-------

Basic Usage
^^^^^^^^^^

.. code-block:: python

   import asyncio
   from grami.agents import AsyncAgent
   from grami.providers.gemini_provider import GeminiProvider

   async def main():
       provider = GeminiProvider(api_key="YOUR_API_KEY")
       agent = AsyncAgent(
           name="Assistant",
           llm=provider
       )
       
       response = await agent.send_message("Hello!")
       print(response)

Memory Usage
^^^^^^^^^^^

.. code-block:: python

   from grami.memory.lru import LRUMemory

   memory = LRUMemory(capacity=100)
   provider.set_memory_provider(memory)

   # Messages will be remembered
   await provider.send_message("My name is Alice")
   await provider.send_message("What's my name?")

Streaming
^^^^^^^^

.. code-block:: python

   async for chunk in provider.stream_message("Tell me a story"):
       print(chunk, end="", flush=True)

Error Handling
^^^^^^^^^^^^

.. code-block:: python

   try:
       response = await provider.send_message("Hello")
   except Exception as e:
       print(f"Error: {str(e)}")

Best Practices
------------

1. Always use environment variables for API keys
2. Implement proper error handling
3. Choose appropriate memory provider based on needs
4. Use streaming for long responses
5. Keep memory capacity reasonable
6. Update chat history before sending messages
