import sys
import os
import asyncio

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import Agent
from grami.providers import GeminiProvider
from examples.tools import WebSearchTool, ImageGenerationTool

class ContentCreationAgent:
    def __init__(self, api_key):
        # Initialize the LLM provider
        self.llm_provider = GeminiProvider(api_key=api_key)
        
        # Create the content creation agent
        self.agent = Agent(
            name="ContentMaster",
            role="Professional Content and Marketing Copywriter",
            llm_provider=self.llm_provider,
            tools=[
                WebSearchTool(),
                ImageGenerationTool()
            ],
            initial_context=[
                {
                    "role": "system",
                    "content": """You are an expert content creator and marketing strategist.
                    Your goal is to create engaging, SEO-optimized content that resonates with the target audience.
                    You can research topics, generate compelling copy, and even create supporting visuals."""
                }
            ]
        )

    async def create_blog_post(self, topic, target_audience):
        """
        Generate a comprehensive blog post with research and image support
        """
        # Research the topic
        research_query = f"Latest trends and insights about {topic} for {target_audience}"
        research_response = await self.agent.send_message(f"Research: {research_query}")
        
        # Generate blog post outline
        outline_response = await self.agent.send_message(
            f"Create a detailed blog post outline about {topic}. "
            f"Target audience: {target_audience}. "
            "Include key sections, potential subheadings, and main points."
        )
        
        # Generate full blog post
        blog_post = await self.agent.send_message(
            f"Write a comprehensive, engaging blog post based on this outline: {outline_response}. "
            "Ensure it's SEO-friendly, informative, and tailored to the target audience."
        )
        
        # Generate supporting image
        image_prompt = f"Featured image for blog post about {topic}, appealing to {target_audience}"
        image_response = await self.agent.send_message(f"Generate an image: {image_prompt}")
        
        return {
            "research": research_response,
            "outline": outline_response,
            "content": blog_post,
            "image_prompt": image_prompt
        }

async def main():
    # Initialize the Content Creation Agent
    content_agent = ContentCreationAgent(
        api_key="YOUR_API_KEY"  # Replace with actual API key
    )
    
    # Demonstrate content creation
    result = await content_agent.create_blog_post(
        topic="AI in Marketing",
        target_audience="Digital Marketing Professionals"
    )
    
    # Print the generated content
    print("--- Research Insights ---")
    print(result['research'])
    
    print("\n--- Blog Post Outline ---")
    print(result['outline'])
    
    print("\n--- Full Blog Post ---")
    print(result['content'])
    
    print("\n--- Image Generation Prompt ---")
    print(result['image_prompt'])

if __name__ == "__main__":
    asyncio.run(main())
