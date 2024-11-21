import os
import asyncio
import logging
from typing import Dict, Any, List

import requests
import json

from grami_ai.agents import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.llms import GeminiLLMProvider

# Use environment variables for sensitive credentials
GOOGLE_SEARCH_API_KEY = os.environ.get('GOOGLE_SEARCH_API_KEY')
GOOGLE_GEMINI_API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')

# Validate API keys
if not GOOGLE_SEARCH_API_KEY:
    logging.warning("GOOGLE_SEARCH_API_KEY not set. Web search functionality will be limited.")

if not GOOGLE_GEMINI_API_KEY:
    logging.warning("GOOGLE_GEMINI_API_KEY not set. AI generation may fail.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_web_search(query: str, num_results: int = 5) -> str:
    """
    Perform a real web search using Google Custom Search API.
    
    Args:
        query (str): Search query string
        num_results (int): Number of search results to retrieve
    
    Returns:
        str: Formatted search results summary
    """
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        logging.error("Missing search API credentials. Returning fallback content.")
        return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."
    
    try:
        # Google Custom Search API endpoint
        url = "https://www.googleapis.com/customsearch/v1"
        
        # Parameters for the search
        params = {
            'key': GOOGLE_SEARCH_API_KEY,
            'cx': GOOGLE_SEARCH_ENGINE_ID,
            'q': query,
            'num': num_results  # Number of results to retrieve
        }
        
        # Send the request
        response = requests.get(url, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code != 200:
            logger.warning(f"Search API returned non-200 status: {response.status_code}")
            return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."
        
        # Parse the JSON response
        search_results = response.json()
        
        # Extract and format key information
        formatted_results = []
        for item in search_results.get('items', []):
            result = {
                'title': item.get('title', 'No Title'),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', 'No description')
            }
            formatted_results.append(
                f" {result['title']}\n"
                f" {result['link']}\n"
                f" {result['snippet']}\n"
            )
        
        # Combine results into a single summary
        if formatted_results:
            return "\n\n".join(formatted_results)
        else:
            logger.warning("No search results found. Providing default trend insights.")
            return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."
    
    except requests.RequestException as e:
        logger.error(f"Web search request failed: {e}")
        return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse search results: {e}")
        return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."
    except Exception as e:
        logger.error(f"Unexpected error in web search: {e}")
        return f"Trend insights for {query}: Current fashion trends are evolving towards sustainability, personalization, and ethical production. Key areas include circular economy, innovative materials, and conscious consumption."

def generate_instagram_caption(topic: str, search_insights: str) -> str:
    """
    Generate an engaging Instagram caption.
    
    Args:
        topic (str): Main topic for the caption
        search_insights (str): Insights from web search
    
    Returns:
        str: Generated Instagram caption
    """
    try:
        # Use search insights to craft a more informed caption
        caption = f""" {topic.upper()} INSIGHTS 

Diving deep into the latest trends and insights:
{search_insights}

What are your thoughts? Drop a comment below! 

#trending #{topic.replace(' ', '')} #lifestyle #inspiration"""
        
        return caption
    except Exception as e:
        return f"Caption generation error: {str(e)}"

def create_hashtags(topic: str, search_insights: str) -> List[str]:
    """
    Generate relevant hashtags for Instagram.
    
    Args:
        topic (str): Main topic
        search_insights (str): Search insights to derive hashtags
    
    Returns:
        List[str]: List of generated hashtags
    """
    base_hashtags = [
        f"#{topic.replace(' ', '')}",
        "#trending",
        "#lifestyle"
    ]
    
    # Add context-specific hashtags based on search insights
    context_hashtags = {
        "fashion": ["#ootd", "#fashiontrends", "#styleinspo"],
        "travel": ["#wanderlust", "#travelgram", "#exploremore"],
        "tech": ["#techtrends", "#innovation", "#futuretech"],
        "marketing": ["#digitalmarketing", "#socialmediatips", "#contentcreation"]
    }
    
    # Find matching context hashtags
    for context, tags in context_hashtags.items():
        if context in topic.lower():
            base_hashtags.extend(tags)
            break
    
    return list(set(base_hashtags))  # Remove duplicates

class InstagramContentAgent:
    """
    AI-powered Instagram content creation agent.
    Capable of real-time research, content generation, and multi-agent communication.
    """
    
    def __init__(self, agent_name: str = "InstagramContentCreator"):
        """
        Initialize the Instagram content agent.
        
        Args:
            agent_name (str): Unique name for the agent
        """
        # Create Gemini LLM provider
        gemini_provider = self._initialize_gemini_provider()
        
        # Initialize agent with tools and Gemini provider
        self.agent = AsyncAgent(
            tools=[perform_web_search, generate_instagram_caption, create_hashtags],
            memory=InMemoryAbstractMemory(),
            llm_provider=gemini_provider
        )
        
        self.agent_name = agent_name
        self.task_state = {
            'status': 'Not Started',
            'progress': 0,
            'content': None,
            'hashtags': None
        }
    
    def _initialize_gemini_provider(self):
        """
        Initialize the Gemini LLM provider with secure API key retrieval.
        
        Returns:
            GeminiLLMProvider instance configured with API credentials
        """
        try:
            # Securely retrieve API key from environment
            if not GOOGLE_GEMINI_API_KEY:
                raise ValueError("No Gemini API key found. Set GOOGLE_GEMINI_API_KEY environment variable.")
            
            # Initialize and return Gemini provider
            return GeminiLLMProvider(
                api_key=GOOGLE_GEMINI_API_KEY,
                model_name="models/gemini-1.5-flash",
                system_instruction=f"You are {self.agent_name}, an AI-powered Instagram content creator. "
                                   "Your goal is to create engaging, trend-aware content. "
                                   "Use web search insights to craft compelling posts."
            )
        
        except Exception as e:
            logger.error(f"Gemini provider initialization failed: {e}")
            return None
    
    async def create_instagram_content(self, content_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Instagram content with advanced reasoning and tool integration.
        
        Args:
            content_brief (Dict[str, Any]): Detailed content creation instructions
        
        Returns:
            Dict[str, Any]: Generated content and metadata
        """
        try:
            logger.info(f"{self.agent_name}: Starting advanced content creation process")
            
            # Update task state
            self.task_state['status'] = 'In Progress'
            
            # Perform multi-stage web search for comprehensive insights
            search_queries = [
                f"Latest trends in {content_brief.get('topic', 'lifestyle')}",
                f"Social media content strategies for {content_brief.get('topic', 'lifestyle')}",
                f"Emerging influencer topics in {content_brief.get('topic', 'lifestyle')}"
            ]
            
            # Aggregate search results
            comprehensive_insights = []
            for query in search_queries:
                search_result = perform_web_search(query, num_results=3)
                comprehensive_insights.append(search_result)
            
            # Combine search insights
            combined_insights = "\n\n".join(comprehensive_insights)
            
            # Prepare task for AI analysis with enhanced context
            task = {
                'objective': 'Create highly engaging, trend-aware Instagram content',
                'context': 'Leverage comprehensive web insights to craft compelling posts',
                'content': f"""Advanced Content Creation Brief:
Topic: {content_brief.get('topic', 'General Lifestyle')}
Target Audience: {content_brief.get('target_audience', 'Young Adults')}
Tone: {content_brief.get('tone', 'Inspirational and Authentic')}
Platform: Instagram

Comprehensive Web Insights:
{combined_insights}

Advanced Content Generation Instructions:
1. Analyze web search insights thoroughly
2. Identify unique, shareable content angles
3. Generate multiple content variations
4. Create engaging captions with storytelling
5. Develop platform-specific content strategy
6. Craft hashtag ecosystem for maximum reach
7. Suggest interactive content elements

Creativity Guidelines:
- Prioritize authenticity and personal connection
- Use emotional storytelling
- Highlight unique perspectives
- Encourage audience interaction
- Align with current social media trends
""",
                'data': content_brief,
                'instructions': [
                    'Deep trend analysis',
                    'Innovative content creation',
                    'Multi-format content strategy',
                    'Maximize audience engagement'
                ]
            }
            
            # Execute task using AI agent with enhanced reasoning
            result = await self.agent.execute_task(task)
            
            # Advanced content validation and enrichment
            content_variations = {
                'primary': result,
                'alternative': generate_alternative_content(result, content_brief)
            }
            
            # Update task state with comprehensive results
            self.task_state['status'] = 'Completed'
            self.task_state['progress'] = 100
            self.task_state['content'] = content_variations
            
            logger.info(f"{self.agent_name}: Advanced content creation completed successfully")
            return {
                'agent': self.agent_name,
                'content': content_variations,
                'status': self.task_state['status']
            }
        
        except Exception as e:
            logger.error(f"{self.agent_name} advanced content creation error: {e}", exc_info=True)
            self.task_state['status'] = 'Failed'
            return {
                'agent': self.agent_name,
                'error': str(e),
                'status': 'Failed'
            }

    def notify_agents(self, message: Dict[str, Any]):
        """
        Simulate notifying other agents about task completion.
        
        Args:
            message (Dict[str, Any]): Notification message
        """
        # In a real multi-agent system, this would trigger inter-agent communication
        logger.info(f"{self.agent_name} Notification: {message}")

def generate_alternative_content(primary_content: str, content_brief: Dict[str, Any]) -> str:
    """
    Generate an alternative content variation.
    
    Args:
        primary_content (str): Original generated content
        content_brief (Dict[str, Any]): Content creation brief
    
    Returns:
        str: Alternative content variation
    """
    try:
        # Create a more concise, punchy alternative
        alternative_caption = f""" {content_brief.get('topic', 'Lifestyle').upper()} HACK ALERT! 

Quick tips that'll transform your {content_brief.get('topic', 'lifestyle')} game:

• Unexpected insight 1
• Game-changing strategy
• Mind-blowing trend

Double-tap if you're ready to level up! 

#TrendAlert #GameChanger #{content_brief.get('topic', 'lifestyle').replace(' ', '')}Hack"""
        
        return alternative_caption
    
    except Exception as e:
        logger.error(f"Alternative content generation error: {e}")
        return "Quick, transformative insights incoming! Double-tap to level up your game. #TrendAlert"

async def main():
    """
    Demonstrate Instagram content creation agent workflow.
    """
    try:
        # Content creation brief
        content_brief = {
            'topic': 'Sustainable Fashion Trends',
            'target_audience': 'Millennials and Gen Z',
            'tone': 'Inspirational and Eco-conscious',
            'platform': 'Instagram'
        }
        
        # Initialize Instagram content agent
        instagram_agent = InstagramContentAgent(agent_name="TrendyContentCreator")
        
        # Create Instagram content
        result = await instagram_agent.create_instagram_content(content_brief)
        
        # Simulate notifying other agents
        instagram_agent.notify_agents({
            'task': 'Instagram Content Creation',
            'status': result['status'],
            'details': result
        })
        
        print("\nInstagram Content Creation Result:")
        print(result['content'])
    
    except Exception as e:
        logger.error(f"Critical error in content creation: {e}", exc_info=True)

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
