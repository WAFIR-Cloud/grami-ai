import pytest
import os
import asyncio
import logging
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from grami_ai.core.agent import AsyncAgent
from grami_ai.llms import GeminiLLMProvider
from grami_ai.llms.base import Message, MessageRole, ConversationMemory
from grami_ai.tools.base import AsyncBaseTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Prompt (similar to the lambda function's system instruction)
BOT_PROMPT = """
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

Important Notes:
- You are not responsible for creating the growth plan itself. Your role is to manage client communication and delegate tasks to your team.
- Always acknowledge receipt of a client request and inform them that you'll update them when the plan is ready.
"""

class ImageGenerationTool(AsyncBaseTool):
    """
    Async tool for generating images
    """
    def __init__(self):
        super().__init__()
        self.metadata.name = "generate_images"
        self.metadata.description = "Generate images based on a query for social media or marketing."

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute the image generation tool
        
        Args:
            task: Task description
            context: Additional context for image generation
        
        Returns:
            Generated image(s)
        """
        # Default to 1 image if not specified in context
        number_of_images = context.get('number_of_images', 1) if context else 1
        
        logger.info(f"Generating {number_of_images} image(s) for task: {task}")
        
        # Simulated image generation
        return {
            'status': 'success',
            'images': [f"generated_image_{i+1}.jpg" for i in range(number_of_images)]
        }

    async def generate(self, query: str, number_of_images: int = 1) -> List[str]:
        """
        Simulate image generation
        
        Args:
            query: Description of the image to generate
            number_of_images: Number of images to generate
        
        Returns:
            List of generated image URLs or placeholders
        """
        result = await self.execute(query, {'number_of_images': number_of_images})
        return result['images']

    def get_parameters(self):
        return {
            "query": {
                "type": "string",
                "description": "Detailed description of the image to generate"
            },
            "number_of_images": {
                "type": "integer", 
                "description": "Number of images to generate",
                "default": 1
            }
        }

@pytest.mark.asyncio
async def test_gemini_chat():
    """
    Comprehensive test of Gemini chat functionality using AsyncAgent
    
    Demonstrates:
    - Creating an agent with Gemini LLM
    - Processing messages
    - Tool integration
    """
    # Create image generation tool
    image_tool = ImageGenerationTool()

    # Create agent
    agent = await AsyncAgent.create(
        name="MarketingAssistant",
        llm="gemini",  # This will use the Gemini LLM provider
        tools=[image_tool],
        system_instruction=BOT_PROMPT
    )

    # Conversation scenarios
    conversation_scenarios = [
        {"type": "text", "content": "Hi, I run a small coffee shop and want to improve my Instagram marketing. Can you help?"},
        {"type": "text", "content": "What kind of content would you recommend for attracting more customers?"},
        {"type": "text", "content": "Can you help me create some images for my social media?"}
    ]

    # Collect responses
    responses = []

    # Run conversation
    for scenario in conversation_scenarios:
        # Process message
        response = await agent.process(scenario)
        
        # Add to responses
        responses.append(response)

        # Optional: Add a small delay between messages
        await asyncio.sleep(1)

    # Assertions
    assert len(responses) == len(conversation_scenarios), "Should have a response for each scenario"
    for response in responses:
        assert isinstance(response, dict), "Response should be a dictionary"
        assert 'status' in response, "Response should have a status"
        assert response['status'] in ['success', 'error'], "Status should be success or error"

    # Print conversation for manual verification
    print("\n--- Conversation Responses ---")
    for response in responses:
        print(response)

    return responses
