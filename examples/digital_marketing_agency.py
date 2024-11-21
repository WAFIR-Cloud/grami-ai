import os
import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import redis
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from grami_ai.agents import AsyncAgent
from grami_ai.memory import RedisMemory
from grami_ai.communication import KafkaCommunicationBus
from grami_ai.llms import GeminiLLMProvider

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rich console for beautiful output
console = Console()

class AgentToolkit:
    """
    Shared toolkit for agents with common utilities
    """
    @staticmethod
    async def web_search(query: str, num_results: int = 3) -> List[Dict[str, str]]:
        """
        Perform web search with fallback mechanism
        """
        try:
            # Use Google Custom Search API
            api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
            engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
            
            if not api_key or not engine_id:
                logger.warning("Search API credentials not found. Using mock search.")
                return [{"title": f"Mock Result for {query}", "link": "https://example.com", "snippet": "Mock search result"}]
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': engine_id,
                'q': query,
                'num': num_results
            }
            
            response = requests.get(url, params=params)
            results = response.json().get('items', [])
            
            return [
                {
                    "title": item.get('title', 'No Title'),
                    "link": item.get('link', ''),
                    "snippet": item.get('snippet', 'No description')
                } for item in results
            ]
        
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []

    @staticmethod
    def generate_hashtags(topic: str) -> List[str]:
        """
        Generate relevant hashtags for a given topic
        """
        base_hashtags = [
            f"#{topic.replace(' ', '')}",
            f"#{topic.replace(' ', '').lower()}Marketing"
        ]
        trending_hashtags = [
            "#DigitalMarketing",
            "#MarketingStrategy",
            "#BusinessGrowth"
        ]
        return base_hashtags + trending_hashtags

class BaseMarketingAgent:
    """
    Enhanced base agent with comprehensive capabilities
    """
    def __init__(
        self, 
        name: str, 
        redis_client: redis.Redis, 
        kafka_bus: KafkaCommunicationBus,
        system_prompt: str = ""
    ):
        self.name = name
        self.redis_client = redis_client
        self.kafka_bus = kafka_bus
        self.toolkit = AgentToolkit()
        
        # Initialize Gemini LLM Provider with enhanced system prompt
        full_system_prompt = f"""
        You are {name} in a professional digital marketing agency.
        Your core responsibilities include strategic thinking, creative problem-solving, 
        and delivering high-quality marketing solutions.
        
        Additional Context:
        {system_prompt}
        
        Communication Guidelines:
        - Be professional and concise
        - Provide actionable insights
        - Collaborate effectively with team members
        """
        
        self.llm_provider = GeminiLLMProvider(
            api_key=os.getenv('GOOGLE_GEMINI_API_KEY'),
            model_name="gemini-1.5-flash",
            system_instruction=full_system_prompt
        )

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Gemini LLM
        """
        try:
            return await self.llm_provider.generate_text(prompt)
        except Exception as e:
            logger.error(f"{self.name} response generation error: {e}")
            return f"I apologize, but I encountered an error: {e}"

    async def update_task_state(
        self, 
        task_id: str, 
        status: str, 
        details: Dict[str, Any] = None
    ):
        """
        Update task state in Redis and publish to Kafka
        """
        state = {
            "agent": self.name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            **(details or {})
        }
        
        # Update Redis
        self.redis_client.hset(f"task:{task_id}", mapping=state)
        
        # Publish to Kafka
        self.kafka_bus.publish(
            topic="task_updates", 
            message={
                "task_id": task_id,
                "state": state
            }
        )

    async def process_task(self, task: Dict[str, Any]):
        """
        Base task processing method to be overridden by specific agents
        """
        raise NotImplementedError("Subclasses must implement task processing")

class DigitalMarketingAgency:
    def __init__(self):
        # Redis connection for global state management
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )

        # Kafka communication bus
        self.kafka_bus = KafkaCommunicationBus(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        )

        # Initialize agency agents
        self.growth_manager = GrowthManagerAgent(
            name="Growth Manager",
            redis_client=self.redis_client,
            kafka_bus=self.kafka_bus
        )
        
        self.content_creator = ContentCreatorAgent(
            name="Content Creator",
            redis_client=self.redis_client,
            kafka_bus=self.kafka_bus
        )
        
        self.social_media_manager = SocialMediaManagerAgent(
            name="Social Media Manager",
            redis_client=self.redis_client,
            kafka_bus=self.kafka_bus
        )
        
        self.market_researcher = MarketResearchAgent(
            name="Market Researcher",
            redis_client=self.redis_client,
            kafka_bus=self.kafka_bus
        )

    async def start_agency_interaction(self):
        """
        Start interactive session with the Growth Manager
        """
        console.print(Panel(
            Text(" GRAMI Digital Marketing Agency AI", style="bold green"),
            title="Agency Interaction"
        ))
        
        while True:
            user_input = console.input("[bold cyan]You: [/bold cyan]")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print(Panel(
                    Text("Thank you for using GRAMI Digital Marketing Agency AI!", style="bold green")
                ))
                break
            
            # Process user input through Growth Manager
            response = await self.growth_manager.process_client_interaction(user_input)
            
            console.print(Panel(
                Text(response, style="bold white"),
                title="[bold blue]Growth Manager[/bold blue]",
                border_style="blue"
            ))

class GrowthManagerAgent(BaseMarketingAgent):
    async def process_client_interaction(self, user_input: str) -> str:
        """
        Process client interaction and delegate tasks
        """
        # Use Gemini to analyze client needs and generate response
        prompt = f"""
        As a Digital Agency Growth Manager, analyze the following client interaction:
        Client Message: {user_input}
        
        Provide a strategic response that:
        1. Understands the client's needs
        2. Suggests potential marketing strategies
        3. Indicates which team members will be involved
        4. Shows empathy and professionalism
        """
        
        response = await self.generate_response(prompt)
        
        # Create and distribute tasks based on the interaction
        await self.create_agency_tasks(user_input)
        
        return response

    async def create_agency_tasks(self, client_request: str):
        """
        Create and distribute tasks to different agents
        """
        task_id = f"task_{hash(client_request)}"
        
        # Distribute tasks to different agents via Kafka
        tasks = [
            {
                "agent": "Market Researcher",
                "task": "Analyze market trends related to the client's business",
                "priority": "high"
            },
            {
                "agent": "Content Creator",
                "task": "Develop initial content strategy based on market research",
                "priority": "medium"
            },
            {
                "agent": "Social Media Manager",
                "task": "Create platform-specific content plan",
                "priority": "medium"
            }
        ]
        
        for task in tasks:
            self.kafka_bus.publish(
                topic="agency_tasks", 
                message={
                    "task_id": task_id,
                    "client_request": client_request,
                    **task
                }
            )
            
            # Update Redis with task state
            await self.update_task_state(task_id, "assigned", {
                "agent": task["agent"],
                "priority": task["priority"]
            })

class ContentCreatorAgent(BaseMarketingAgent):
    """
    Agent responsible for creating engaging content strategies and materials
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Content Creator", 
            system_prompt="Specialize in creating compelling, trend-aware content across multiple platforms.",
            *args, **kwargs
        )

    async def process_task(self, task: Dict[str, Any]):
        """
        Process content creation tasks
        """
        task_id = task.get('task_id', 'unknown_task')
        client_request = task.get('client_request', '')
        
        # Perform web search for context
        search_results = await self.toolkit.web_search(client_request)
        
        # Generate content strategy prompt
        prompt = f"""
        Content Creation Task for Client Request: {client_request}
        
        Web Search Insights:
        {json.dumps(search_results, indent=2)}
        
        Create a comprehensive content strategy that includes:
        1. Content pillars and themes
        2. Recommended content types (blog, social media, video)
        3. Tone and style guidelines
        4. Potential content formats
        5. Suggested posting frequency
        """
        
        # Generate content strategy
        content_strategy = await self.generate_response(prompt)
        
        # Update task state
        await self.update_task_state(
            task_id, 
            "completed", 
            {
                "content_strategy": content_strategy,
                "hashtags": self.toolkit.generate_hashtags(client_request)
            }
        )
        
        # Visualize results
        strategy_panel = Panel(
            Text(content_strategy, style="bold white"),
            title=f"[bold green]Content Strategy for: {client_request}[/bold green]",
            border_style="green"
        )
        console.print(strategy_panel)

class SocialMediaManagerAgent(BaseMarketingAgent):
    """
    Agent responsible for social media strategy and platform-specific content planning
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Social Media Manager", 
            system_prompt="Expert in creating platform-specific social media strategies and content plans.",
            *args, **kwargs
        )

    async def process_task(self, task: Dict[str, Any]):
        """
        Process social media content planning tasks
        """
        task_id = task.get('task_id', 'unknown_task')
        client_request = task.get('client_request', '')
        
        # Analyze platform-specific trends
        platform_trends = await self.toolkit.web_search(f"Social media trends for {client_request}")
        
        # Generate social media strategy prompt
        prompt = f"""
        Social Media Strategy for: {client_request}
        
        Platform Trend Insights:
        {json.dumps(platform_trends, indent=2)}
        
        Develop a comprehensive social media strategy:
        1. Platform selection and prioritization
        2. Content mix (Stories, Reels, Posts)
        3. Engagement tactics
        4. Posting schedule
        5. Audience targeting recommendations
        """
        
        # Generate social media strategy
        social_strategy = await self.generate_response(prompt)
        
        # Update task state
        await self.update_task_state(
            task_id, 
            "completed", 
            {
                "social_media_strategy": social_strategy,
                "recommended_platforms": ["Instagram", "TikTok", "LinkedIn"]
            }
        )
        
        # Visualize results
        strategy_panel = Panel(
            Text(social_strategy, style="bold white"),
            title=f"[bold blue]Social Media Strategy for: {client_request}[/bold blue]",
            border_style="blue"
        )
        console.print(strategy_panel)

class MarketResearchAgent(BaseMarketingAgent):
    """
    Agent responsible for market analysis, trend identification, and competitive research
    """
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="Market Researcher", 
            system_prompt="Specialize in comprehensive market analysis, trend identification, and competitive intelligence.",
            *args, **kwargs
        )

    async def process_task(self, task: Dict[str, Any]):
        """
        Process market research tasks
        """
        task_id = task.get('task_id', 'unknown_task')
        client_request = task.get('client_request', '')
        
        # Perform in-depth market research
        market_insights = await self.toolkit.web_search(f"Market trends and analysis for {client_request}")
        competitive_research = await self.toolkit.web_search(f"Competitive landscape for {client_request}")
        
        # Generate market research report prompt
        prompt = f"""
        Market Research Report for: {client_request}
        
        Market Insights:
        {json.dumps(market_insights, indent=2)}
        
        Competitive Landscape:
        {json.dumps(competitive_research, indent=2)}
        
        Provide a comprehensive market research report:
        1. Current market trends
        2. Target audience analysis
        3. Competitive landscape overview
        4. Potential growth opportunities
        5. Strategic recommendations
        """
        
        # Generate market research report
        market_report = await self.generate_response(prompt)
        
        # Update task state
        await self.update_task_state(
            task_id, 
            "completed", 
            {
                "market_research_report": market_report,
                "key_insights": market_insights[:3]
            }
        )
        
        # Visualize results
        report_panel = Panel(
            Text(market_report, style="bold white"),
            title=f"[bold magenta]Market Research for: {client_request}[/bold magenta]",
            border_style="magenta"
        )
        console.print(report_panel)

async def main():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Initialize and start the Digital Marketing Agency
    agency = DigitalMarketingAgency()
    await agency.start_agency_interaction()

if __name__ == "__main__":
    asyncio.run(main())
