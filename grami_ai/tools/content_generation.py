import asyncio
import logging
from typing import Optional, List, Dict, Any

from grami_ai.core.tools import AsyncBaseTool
from grami_ai.core.tools import ToolMetadata, ToolCategory

class ContentGenerationTool(AsyncBaseTool):
    def __init__(self, 
                 llm_provider: Optional[Any] = None,
                 metadata: Optional[ToolMetadata] = None):
        """
        Initialize the Content Generation Tool
        
        Args:
            llm_provider: Optional LLM provider for content generation
            metadata: Optional tool metadata
        """
        default_metadata = ToolMetadata(
            name="content_generation",
            description="Generate social media content for various platforms",
            category=ToolCategory.CONTENT,
            performance_score=0.8,
            reliability_score=0.7,
            tags=["social_media", "content", "generation"]
        )
        
        super().__init__(
            metadata=metadata or default_metadata
        )
        
        self.llm_provider = llm_provider
        self.logger = logging.getLogger(__name__)

    async def generate(self, 
                       platform: str = 'instagram', 
                       niche: str = 'general', 
                       content_type: str = 'post',
                       **kwargs) -> Dict[str, Any]:
        """
        Generate content for a specific platform and niche
        
        Args:
            platform: Social media platform (e.g., 'instagram', 'twitter')
            niche: Content niche or topic
            content_type: Type of content (e.g., 'post', 'reel', 'story')
            
        Returns:
            Dict containing generated content details
        """
        try:
            # Simulate content generation (replace with actual LLM generation later)
            content_ideas = {
                'instagram': {
                    'tech': {
                        'post': "🚀 Tech Innovation Alert! Just discovered how AI is revolutionizing problem-solving. What breakthrough are you most excited about? 💡 #TechInnovation #AIFuture",
                        'reel': "5 Mind-Blowing AI Tools That Will Change Your Workflow Forever 🤯 #TechTips #AIProductivity",
                        'story': "Behind the scenes of our latest AI project! Sneak peek coming soon 👀 #InnovationInProgress"
                    },
                    'general': {
                        'post': "Exploring new horizons and pushing boundaries every single day! 💪 What's your next big goal? #PersonalGrowth #Motivation",
                        'reel': "3 Life Hacks That Actually Work (Trust Me!) 🌟 #LifeHacks #PersonalDevelopment",
                        'story': "Quick morning inspiration to kickstart your day! ☀️ #MorningMotivation"
                    }
                },
                'twitter': {
                    'tech': {
                        'post': "AI is not just a technology, it's a paradigm shift. Are you ready? 🤖 #AIRevolution #TechTrends"
                    }
                }
            }
            
            # Default to general if specific niche not found
            niche = niche.lower()
            platform = platform.lower()
            content_type = content_type.lower()
            
            generated_content = content_ideas.get(platform, {}).get(niche, {}).get(content_type, 
                "Exciting content coming soon! Stay tuned! 🌟")
            
            self.logger.info(f"Generated content for {platform} in {niche} niche")
            
            return {
                'platform': platform,
                'niche': niche,
                'content_type': content_type,
                'text': generated_content,
                'hashtags': self._extract_hashtags(generated_content)
            }
        except Exception as e:
            self.logger.error(f"Content generation error: {e}")
            raise

    def _extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from the generated content
        
        Args:
            text: Generated content text
            
        Returns:
            List of hashtags
        """
        return [word.strip() for word in text.split() if word.startswith('#')]

# Optional: Add a factory method for easier instantiation
def create_content_generation_tool(**kwargs):
    """
    Factory method to create a content generation tool
    
    Args:
        **kwargs: Configuration parameters for the tool
        
    Returns:
        ContentGenerationTool instance
    """
    return ContentGenerationTool(**kwargs)
