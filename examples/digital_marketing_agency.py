import os
import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid

import redis
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from grami_ai.agents import AsyncAgent
from grami_ai.memory import RedisMemory
# from grami_ai.communication import KafkaCommunicationBus
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
        redis_client: redis.Redis = None, 
        kafka_bus: None = None,
        system_prompt: str = ""
    ):
        self.name = name
        self.redis_client = redis_client or redis.Redis()
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
        Update task state in Redis
        """
        state = {
            "status": status,
            "updated_at": datetime.now().isoformat()
        }
        
        if details:
            state.update(details)
        
        # Update Redis
        self.redis_client.hset(f"task:{task_id}", mapping=state)

    async def process_task(self, task: Dict[str, Any]):
        """
        Base task processing method to be overridden by specific agents
        """
        pass

class DigitalMarketingAgency:
    def __init__(self):
        # Redis connection for global state management
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )

        # Kafka communication bus
        # self.kafka_bus = KafkaCommunicationBus(
        #     bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        # )

        # Initialize agency agents
        self.growth_manager = GrowthManagerAgent(
            name="Growth Manager",
            redis_client=self.redis_client,
            kafka_bus=None
        )
        
        self.content_creator = ContentCreatorAgent(
            name="Content Creator",
            redis_client=self.redis_client,
            kafka_bus=None
        )
        
        self.social_media_manager = SocialMediaManagerAgent(
            name="Social Media Manager",
            redis_client=self.redis_client,
            kafka_bus=None
        )
        
        self.market_researcher = MarketResearchAgent(
            name="Market Researcher",
            redis_client=self.redis_client,
            kafka_bus=None
        )

    async def start_agency_interaction(self, client_request: str):
        """
        Interactive chat-based service discovery workflow
        """
        console.print(Panel(
            Text(" GRAMI Digital Marketing Agency AI - Interactive Discovery", style="bold green"),
            border_style="green"
        ))
        
        # Initial greeting and context setting
        console.print("\n[bold blue]Growth Manager:[/bold blue] Hello! I'm excited to help you discover the right digital marketing services for your business.")
        console.print(f"[bold green]Client's Initial Request:[/bold green] {client_request}\n")

        # Conversation flow with predefined and dynamic questions
        conversation_stages = [
            {
                "stage": "Business Overview",
                "questions": [
                    "Can you tell me more about your business and what you do?",
                    "What makes your business unique in the market?",
                    "What are your primary business goals?"
                ]
            },
            {
                "stage": "Target Audience",
                "questions": [
                    "Who is your ideal customer?",
                    "What age group, demographics, or interests do they have?",
                    "How do you currently reach your target audience?"
                ]
            },
            {
                "stage": "Current Marketing Efforts",
                "questions": [
                    "What marketing channels are you currently using?",
                    "What has worked well for you so far?",
                    "What challenges are you facing with your current marketing?"
                ]
            },
            {
                "stage": "Service Needs",
                "questions": [
                    "What specific digital marketing services are you most interested in?",
                    "Are you looking for comprehensive marketing or specific services?",
                    "Do you have a budget in mind for marketing services?"
                ]
            }
        ]

        # Store conversation details
        detailed_client_info = {
            "initial_request": client_request,
            "conversation_details": {}
        }

        # Interactive conversation
        for stage in conversation_stages:
            console.print(f"\n[bold magenta]--- {stage['stage']} ---[/bold magenta]")
            
            stage_responses = []
            for question in stage['questions']:
                # Simulate an interactive conversation
                console.print(f"\n[bold blue]Growth Manager:[/bold blue] {question}")
                
                # Use LLM to generate a mock client response
                mock_response = await self.growth_manager.generate_mock_client_response(question, detailed_client_info)
                
                console.print(f"[bold green]Client:[/bold green] {mock_response}")
                
                stage_responses.append({
                    "question": question,
                    "response": mock_response
                })
            
            detailed_client_info["conversation_details"][stage['stage']] = stage_responses

        # Generate tasks based on the conversation
        tasks = await self.growth_manager.generate_comprehensive_tasks(detailed_client_info)
        
        # Distribute tasks to team members
        console.print("\n[bold magenta]Task Allocation:[/bold magenta]")
        for task in tasks:
            assigned_agent = self.assign_task_to_agent(task)
            console.print(f"[bold cyan]Task:[/bold cyan] {task}")
            console.print(f"[bold green]Assigned to:[/bold green] {assigned_agent}\n")
        
        # Generate a comprehensive project summary
        project_summary = await self.growth_manager.generate_detailed_project_summary(detailed_client_info, tasks)
        
        console.print(Panel(
            Text(project_summary, style="bold white"),
            title="[bold blue]Comprehensive Project Discovery[/bold blue]",
            border_style="blue"
        ))
        
        return project_summary

    def assign_task_to_agent(self, task: str) -> str:
        """
        Assign a task to an appropriate team member
        """
        # Simple task assignment logic based on keywords
        if any(keyword in task.lower() for keyword in ['seo', 'search', 'ranking']):
            return "Market Researcher"
        elif any(keyword in task.lower() for keyword in ['content', 'blog', 'writing']):
            return "Copywriter"
        elif any(keyword in task.lower() for keyword in ['social', 'instagram', 'facebook', 'twitter']):
            return "Social Media Manager"
        elif any(keyword in task.lower() for keyword in ['design', 'visual', 'graphics']):
            return "Designer"
        else:
            return "Growth Manager"

    async def monitor_project_progress(self, project_id: str):
        """
        Monitor project progress and manage task completion
        """
        # Implementation of project progress tracking
        pass

class GrowthManagerAgent(BaseMarketingAgent):
    def __init__(
        self, 
        name: str = "Growth Manager",
        redis_client: redis.Redis = None,
        kafka_bus: None = None
    ):
        super().__init__(
            name=name, 
            redis_client=redis_client, 
            kafka_bus=kafka_bus, 
            system_prompt="Specialize in strategic client interaction and task delegation."
        )
        
        # Team members
        self.team = {
            "Copywriter": TeamMember(
                name="Copywriter", 
                role="Content Writing", 
                skills=["copywriting", "brand messaging"],
                communication_bus=None
            ),
            "Content Planner": TeamMember(
                name="Content Planner", 
                role="Content Strategy", 
                skills=["content planning", "editorial calendars"],
                communication_bus=None
            ),
            "Social Media Manager": TeamMember(
                name="Social Media Manager", 
                role="Social Media Strategy", 
                skills=["social media marketing", "platform management"],
                communication_bus=None
            ),
            "Designer": TeamMember(
                name="Designer", 
                role="Visual Content", 
                skills=["graphic design", "visual branding"],
                communication_bus=None
            ),
            "Market Researcher": TeamMember(
                name="Market Researcher", 
                role="Research & Insights", 
                skills=["market analysis", "trend research"],
                communication_bus=None
            )
        }

    async def process_client_request(self, client_request: str) -> Dict[str, Any]:
        """
        Process client request and delegate tasks to team members
        
        Args:
            client_request (str): Initial client communication
        
        Returns:
            Dict containing project details and task assignments
        """
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Use LLM to generate task breakdown
        task_breakdown_prompt = f"""
        As a Growth Manager, analyze the following client request and break it down into specific, actionable marketing tasks.
        Format your response EXACTLY as a JSON object with the following structure:

        {{
            "project_name": "Brief descriptive name for the project",
            "tasks": [
                {{
                    "task_id": "Generate a UUID here",
                    "description": "Detailed task description",
                    "assigned_to": "One of: Market Researcher, Content Creator, Social Media Manager, Designer, Copywriter, Content Planner",
                    "priority": "high/medium/low",
                    "estimated_hours": "Estimated hours as a number",
                    "dependencies": ["task_ids of any dependent tasks"]
                }}
            ]
        }}

        Important:
        - Ensure response is valid JSON
        - Only use team member names from the list above
        - Include at least 3 tasks
        - Make task descriptions specific and actionable
        - Set realistic time estimates

        Client Request: {client_request}
        """
        
        try:
            # Start a chat session with clear JSON formatting instruction
            chat = await self.llm_provider.start_chat()
            
            # Get task breakdown
            task_breakdown_response = await self.llm_provider.send_message(
                chat, 
                task_breakdown_prompt + "\nRemember to ONLY return a valid JSON object."
            )
            
            # Clean the response and parse JSON
            cleaned_response = task_breakdown_response.strip()
            # Remove any markdown code block markers if present
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
            
            try:
                parsed_response = json.loads(cleaned_response)
                tasks = parsed_response.get("tasks", [])
                
                # Validate tasks
                if not tasks:
                    logger.warning("No tasks found in LLM response. Using fallback.")
                    tasks = self.fallback_task_breakdown(client_request)
                else:
                    # Validate each task has required fields
                    for task in tasks:
                        if not all(k in task for k in ["task_id", "description", "assigned_to", "priority"]):
                            logger.warning("Invalid task format. Using fallback.")
                            tasks = self.fallback_task_breakdown(client_request)
                            break
                        
                        # Ensure assigned_to is valid
                        if task["assigned_to"] not in self.team:
                            task["assigned_to"] = "Market Researcher"
                            logger.warning(f"Invalid team member. Reassigning task to Market Researcher")
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse LLM response as JSON: {e}. Using fallback.")
                tasks = self.fallback_task_breakdown(client_request)
            
            # Delegate tasks to team members
            await self.delegate_tasks(project_id, tasks)
            
            # Store project metadata in Redis
            project_metadata = {
                "project_id": project_id,
                "client_request": client_request,
                "status": "in_progress",
                "tasks": json.dumps(tasks)
            }
            for key, value in project_metadata.items():
                self.redis_client.hset(f"project:{project_id}", key, value)
            
            # Prepare client response
            response = f"""
            Thank you for your request. We've initiated a comprehensive digital marketing strategy.
            
            Project ID: {project_id}
            Status: Tasks assigned and in progress
            
            Our team will work diligently to develop a tailored marketing solution. 
            We'll update you soon with our initial findings and strategy recommendations.
            """
            
            return {
                "project_id": project_id,
                "response": response,
                "tasks": tasks
            }
        
        except Exception as e:
            logger.error(f"Error in task breakdown generation: {e}")
            tasks = self.fallback_task_breakdown(client_request)
            return {
                "project_id": project_id,
                "response": "Internal error occurred. Using fallback task breakdown.",
                "tasks": tasks
            }

    def fallback_task_breakdown(self, client_request: str) -> List[Dict[str, Any]]:
        """
        Fallback method to generate tasks if LLM parsing fails
        """
        return [
            {
                "task_id": str(uuid.uuid4()),
                "description": f"Initial analysis for: {client_request}",
                "assigned_to": "Market Researcher",
                "priority": "high"
            }
        ]

    async def delegate_tasks(self, project_id: str, tasks: List[Dict[str, Any]]):
        """
        Delegate tasks to appropriate team members
        """
        for task in tasks:
            assigned_member = self.team.get(task.get('assigned_to'))
            if assigned_member:
                # Add task to team member's queue
                await assigned_member.task_queue.put(task)
            else:
                logger.warning(f"No team member found for task: {task}")

    async def monitor_project_progress(self, project_id: str):
        """
        Monitor project progress and manage task completion
        """
        # Implementation of project progress tracking
        pass

    async def process_client_interaction(self, user_input: str) -> str:
        """
        Process client interaction and delegate tasks
        """
        # Use Gemini to analyze client needs and generate response
        interaction_prompt = f"""
        As a Digital Agency Growth Manager, analyze the following client interaction 
        and provide a strategic, empathetic, and actionable response:

        Client Message: {user_input}

        Your response should:
        1. Demonstrate deep understanding of the client's needs
        2. Highlight potential marketing opportunities
        3. Outline initial strategic approach
        4. Show enthusiasm and professionalism
        5. Provide clear next steps

        Response Format:
        {{
            "initial_assessment": "Brief summary of client's core needs",
            "strategic_approach": "High-level marketing strategy overview",
            "key_opportunities": ["Opportunity 1", "Opportunity 2"],
            "next_steps": ["Step 1", "Step 2"],
            "response_text": "Conversational response to the client"
        }}
        """
        
        try:
            # Start a chat session
            chat = await self.llm_provider.start_chat()
            
            # Get strategic response
            interaction_response = await self.llm_provider.send_message(
                chat, 
                interaction_prompt + "\nRespond ONLY with a valid JSON object."
            )
            
            # Clean and parse the response
            cleaned_response = interaction_response.strip()
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
            
            try:
                parsed_response = json.loads(cleaned_response)
                
                # Trigger task generation based on the interaction
                project_result = await self.process_client_request(user_input)
                
                # Combine LLM insights with task generation
                full_response = (
                    f"{parsed_response.get('response_text', 'Thank you for reaching out!')}\n\n"
                    f"Initial Strategic Approach: {parsed_response.get('strategic_approach', 'Comprehensive marketing strategy')}\n\n"
                    f"Key Opportunities:\n" + 
                    "\n".join(f"- {opp}" for opp in parsed_response.get('key_opportunities', [])) + 
                    f"\n\nProject ID: {project_result['project_id']}"
                )
                
                return full_response
            
            except json.JSONDecodeError:
                # Fallback to a generic response
                return (
                    "Thank you for reaching out! Our team is excited to help you with your marketing needs. "
                    "We'll conduct a thorough analysis and develop a tailored strategy for your business."
                )
        
        except Exception as e:
            logger.error(f"Error in client interaction processing: {e}")
            return (
                "We apologize for the technical difficulty. Our team is ready to assist you. "
                "We'll review your request and get back to you shortly."
            )

    async def create_agency_tasks(self, client_request: str):
        """
        Create and distribute tasks to different agents
        """
        task_id = f"task_{hash(client_request)}"
        
        # Distribute tasks to different agents
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
            # Update Redis with task state
            await self.update_task_state(
                task_id, 
                "assigned", 
                {
                    "agent": task["agent"],
                    "priority": task["priority"]
                }
            )

    async def generate_discovery_response(self, question: str, client_request: str) -> str:
        """
        Generate a discovery response for the given question
        """
        discovery_prompt = f"""
        As a Growth Manager, respond to the following discovery question:

        Question: {question}
        Client Request: {client_request}

        Your response should:
        1. Address the question directly
        2. Provide additional context or insights
        3. Show enthusiasm and professionalism

        Response Format:
        A conversational response to the client
        """
        
        try:
            # Start a chat session
            chat = await self.llm_provider.start_chat()
            
            # Get discovery response
            discovery_response = await self.llm_provider.send_message(
                chat, 
                discovery_prompt + "\nRespond with a conversational response."
            )
            
            return discovery_response.strip()
        
        except Exception as e:
            logger.error(f"Error in discovery response generation: {e}")
            return (
                "Thank you for sharing more about your business. We're excited to help you with your marketing needs."
            )

    async def generate_team_tasks(self, client_info: Dict[str, Any]) -> List[str]:
        """
        Generate tasks for the team based on the client information
        """
        tasks = []
        
        # Use LLM to generate tasks
        task_generation_prompt = f"""
        As a Growth Manager, analyze the following client information and generate tasks for the team:

        Client Information:
        {json.dumps(client_info, indent=2)}

        Your tasks should:
        1. Address specific client needs or pain points
        2. Be actionable and measurable
        3. Align with the client's goals and objectives

        Task Format:
        A list of task descriptions
        """
        
        try:
            # Start a chat session
            chat = await self.llm_provider.start_chat()
            
            # Get task generation response
            task_generation_response = await self.llm_provider.send_message(
                chat, 
                task_generation_prompt + "\nRespond with a list of task descriptions."
            )
            
            # Clean and parse the response
            cleaned_response = task_generation_response.strip()
            tasks = cleaned_response.splitlines()
            
            return tasks
        
        except Exception as e:
            logger.error(f"Error in task generation: {e}")
            return [
                "Conduct market research to understand the client's target audience",
                "Develop a comprehensive content strategy",
                "Create a social media content plan"
            ]

    async def generate_project_summary(self, client_info: Dict[str, Any], tasks: List[str]) -> str:
        """
        Generate a project summary based on the client information and tasks
        """
        project_summary = f"""
        Project Summary:

        Client Request: {client_info["initial_request"]}

        Discovery Responses:
        {json.dumps(client_info["discovery_responses"], indent=2)}

        Tasks:
        {json.dumps(tasks, indent=2)}
        """
        
        return project_summary

    async def generate_mock_client_response(self, question: str, client_info: Dict[str, Any]) -> str:
        """
        Generate a mock client response for the given question
        """
        mock_response_prompt = f"""
        As a client, respond to the following question:

        Question: {question}
        Client Information:
        {json.dumps(client_info, indent=2)}

        Your response should:
        1. Address the question directly
        2. Provide additional context or insights
        3. Show enthusiasm and professionalism

        Response Format:
        A conversational response
        """
        
        try:
            # Start a chat session
            chat = await self.llm_provider.start_chat()
            
            # Get mock client response
            mock_response = await self.llm_provider.send_message(
                chat, 
                mock_response_prompt + "\nRespond with a conversational response."
            )
            
            return mock_response.strip()
        
        except Exception as e:
            logger.error(f"Error in mock client response generation: {e}")
            return (
                "Thank you for asking! I'm excited to share more about my business."
            )

    async def generate_comprehensive_tasks(self, client_info: Dict[str, Any]) -> List[str]:
        """
        Generate comprehensive tasks based on the client information
        """
        tasks = []
        
        # Use LLM to generate tasks
        task_generation_prompt = f"""
        As a Growth Manager, analyze the following client information and generate comprehensive tasks:

        Client Information:
        {json.dumps(client_info, indent=2)}

        Your tasks should:
        1. Address specific client needs or pain points
        2. Be actionable and measurable
        3. Align with the client's goals and objectives

        Task Format:
        A list of task descriptions
        """
        
        try:
            # Start a chat session
            chat = await self.llm_provider.start_chat()
            
            # Get task generation response
            task_generation_response = await self.llm_provider.send_message(
                chat, 
                task_generation_prompt + "\nRespond with a list of task descriptions."
            )
            
            # Clean and parse the response
            cleaned_response = task_generation_response.strip()
            tasks = cleaned_response.splitlines()
            
            return tasks
        
        except Exception as e:
            logger.error(f"Error in task generation: {e}")
            return [
                "Conduct market research to understand the client's target audience",
                "Develop a comprehensive content strategy",
                "Create a social media content plan"
            ]

    async def generate_detailed_project_summary(self, client_info: Dict[str, Any], tasks: List[str]) -> str:
        """
        Generate a detailed project summary based on the client information and tasks
        """
        project_summary = f"""
        Project Summary:

        Client Request: {client_info["initial_request"]}

        Conversation Details:
        {json.dumps(client_info["conversation_details"], indent=2)}

        Tasks:
        {json.dumps(tasks, indent=2)}
        """
        
        return project_summary

class TeamMember:
    """
    Represents a team member in the digital agency
    """
    def __init__(
        self, 
        name: str, 
        role: str, 
        skills: List[str], 
        communication_bus: None
    ):
        self.name = name
        self.role = role
        self.skills = skills
        self.communication_bus = communication_bus
        self.task_queue = asyncio.Queue()

    async def process_task(self, task: Dict[str, Any]):
        """
        Process assigned task
        """
        logger.info(f"{self.name} processing task: {task.get('description', 'No description')}")
        
        # Simulate task processing
        await asyncio.sleep(1)  # Simulated work time
        
        # Notify task completion
        pass

class ContentCreatorAgent(BaseMarketingAgent):
    """
    Agent responsible for creating engaging content strategies and materials
    """
    def __init__(
        self, 
        name: str = "Content Creator",
        redis_client: redis.Redis = None,
        kafka_bus: None = None
    ):
        super().__init__(
            name=name, 
            redis_client=redis_client, 
            kafka_bus=kafka_bus, 
            system_prompt="Specialize in creating compelling, trend-aware content across multiple platforms."
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
    def __init__(
        self, 
        name: str = "Social Media Manager",
        redis_client: redis.Redis = None,
        kafka_bus: None = None
    ):
        super().__init__(
            name=name, 
            redis_client=redis_client, 
            kafka_bus=kafka_bus, 
            system_prompt="Expert in creating platform-specific social media strategies and content plans."
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
    def __init__(
        self, 
        name: str = "Market Researcher",
        redis_client: redis.Redis = None,
        kafka_bus: None = None
    ):
        super().__init__(
            name=name, 
            redis_client=redis_client, 
            kafka_bus=kafka_bus, 
            system_prompt="Specialize in comprehensive market analysis, trend identification, and competitive intelligence."
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

def main():
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('/Users/ferasalawadi/PycharmProjects/grami-ai/.env')

    # Validate Gemini API key
    import os
    import google.generativeai as genai
    import asyncio

    if not os.getenv('GOOGLE_GEMINI_API_KEY'):
        print("Error: GOOGLE_GEMINI_API_KEY is not set.")
        return

    # Configure Gemini API
    genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))

    # Redirect stdout to a file
    with open('/Users/ferasalawadi/PycharmProjects/grami-ai/digital_marketing_agency_output.txt', 'w') as output_file:
        # Temporarily redirect stdout to the file
        import sys
        original_stdout = sys.stdout
        sys.stdout = output_file

        try:
            # Your existing main logic
            print("Digital Marketing Agency AI - Execution Output")
            print("=============================================\n")

            # Initialize the agency
            agency = DigitalMarketingAgency()

            # Predefined client requests
            client_requests = [
                "I want to discover digital marketing services for my new sustainable fashion e-commerce startup.",
                "Looking to expand my local bakery's online presence and attract more customers through digital marketing.",
                "Develop a marketing plan for a tech startup offering AI-powered productivity tools."
            ]

            # Create a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Process each client request
            for i, client_request in enumerate(client_requests, 1):
                print(f"Predefined Client Request {i}: {['Sustainable Fashion E-commerce Startup', 'Local Bakery Online Presence', 'Tech Startup AI Productivity Tools'][i-1]}")
                print("-" * 65)
                print(f"Processing Client Request: {client_request}\n")
                
                # Process the client request
                loop.run_until_complete(agency.start_agency_interaction(client_request))
                
                print("\n" + "=" * 50 + "\n")

            # Close the event loop
            loop.close()

        finally:
            # Restore stdout
            sys.stdout = original_stdout

    print("Output has been written to digital_marketing_agency_output.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(Panel(
            Text("Agency interaction terminated.", style="bold yellow"),
            title="Shutdown"
        ))
    except Exception as e:
        console.print(Panel(
            Text(f"An unexpected error occurred: {e}", style="bold red"),
            title="Error"
        ))
        import traceback
        traceback.print_exc()
