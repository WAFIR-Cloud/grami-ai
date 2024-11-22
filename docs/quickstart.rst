Quickstart Guide
===============

Welcome to GRAMI AI! This guide will help you get started with creating your first AI agent.

Installation
------------

First, install GRAMI AI:

.. code-block:: bash

    pip install grami-ai

Basic Agent Creation
-------------------

Here's a simple example of creating an AI agent for marketing:

.. code-block:: python

    import asyncio
    from grami_ai.core.agent import AsyncAgent

    async def main():
        # Create a marketing assistant agent
        agent = await AsyncAgent.create(
            name="MarketingAssistant",
            llm="gemini",  # Use Gemini LLM
            tools=["content_generation", "web_search"],
            system_instruction="Help small businesses improve their social media marketing"
        )

        # Generate Instagram content
        response = await agent.process({
            "type": "content_request",
            "platform": "instagram",
            "niche": "coffee shop",
            "content_type": "post"
        })

        print(response)

    # Run the agent
    asyncio.run(main())

Custom Tool Example
------------------

You can create custom tools to extend your agent's capabilities:

.. code-block:: python

    from grami_ai.tools.base import AsyncBaseTool
    from typing import Optional, Dict, Any

    class ImageGenerationTool(AsyncBaseTool):
        def __init__(self):
            super().__init__()
            self.metadata.name = "generate_images"
            self.metadata.description = "Generate marketing images"

        async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
            # Implement image generation logic
            return {
                'status': 'success',
                'images': [f"generated_image_{i+1}.jpg" for i in range(context.get('number_of_images', 1))]
            }

        def get_parameters(self):
            return {
                "query": {
                    "type": "string",
                    "description": "Image generation prompt"
                },
                "number_of_images": {
                    "type": "integer",
                    "description": "Number of images to generate",
                    "default": 1
                }
            }

Key Concepts
------------

Agents
~~~~~~

- Orchestrate LLM, memory, tools, and interfaces
- Support async message processing
- Enable dynamic tool selection

Tools
~~~~~

- Extensible async tool base class
- Metadata-driven tool configuration
- Support for various tool categories

Memory
~~~~~~

- Async memory providers
- In-memory and Redis backends
- Conversation and state management

Configuration
~~~~~~~~~~~~~

GRAMI AI supports environment-based configuration:

.. code-block:: python

    from grami_ai.core.config import get_settings

    # Get environment-specific settings
    settings = get_settings()

Next Steps
----------

- Explore the API reference
- Check out more advanced examples
- Join our community for support and collaboration

Happy building!
