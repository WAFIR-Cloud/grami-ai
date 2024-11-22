import asyncio
import os
from typing import Dict, Any, Optional

from grami_ai.core.agent import AsyncAgent
from grami_ai.tools.base import AsyncBaseTool

class InstagramContentGenerationTool(AsyncBaseTool):
    """
    A specialized tool for generating social media content
    """
    def __init__(self):
        super().__init__()
        self.metadata.name = "instagram_content_generator"
        self.metadata.description = "Generate engaging Instagram content for businesses"

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate content based on the given context
        
        :param task: Type of content generation task
        :param context: Context for content generation
        :return: Generated content details
        """
        niche = context.get('niche', 'general')
        content_type = context.get('content_type', 'post')
        
        # Simulated content generation logic
        content_templates = {
            'coffee_shop': {
                'post': "☕ Brewing happiness, one cup at a time! Our artisan coffee is crafted with passion and precision. #CoffeeLovers #LocalCafe",
                'story': "Behind the scenes: Our baristas preparing your perfect morning brew! 🌞🍵 #CraftCoffee"
            },
            'fitness_studio': {
                'post': "Transform your body, elevate your mind. Join our fitness community today! 💪🔥 #FitnessJourney",
                'story': "Quick workout tip: 10-minute HIIT that burns calories and boosts energy! 🏋️‍♀️ #FitnessTips"
            }
        }
        
        generated_content = content_templates.get(niche, {}).get(content_type, "Generic engaging content")
        
        return {
            'status': 'success',
            'content': generated_content,
            'platform': 'instagram',
            'niche': niche,
            'content_type': content_type
        }

async def main():
    """
    Demonstrate social media assistant agent workflow
    """
    # Create a marketing assistant agent with custom Instagram content generation tool
    agent = await AsyncAgent.create(
        name="SocialMediaAssistant",
        llm="gemini",  # Can be switched to other providers
        tools=[InstagramContentGenerationTool()],
        system_instruction="Help businesses create engaging social media content"
    )

    # Generate content for different niches
    niches = ['coffee_shop', 'fitness_studio']
    
    for niche in niches:
        response = await agent.process({
            "type": "content_generation",
            "platform": "instagram",
            "niche": niche,
            "content_type": "post"
        })
        
        print(f"Generated Content for {niche.replace('_', ' ').title()}:")
        print(response['content'])
        print("\n---\n")

if __name__ == "__main__":
    asyncio.run(main())
