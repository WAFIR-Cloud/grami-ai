"""
Grami AI Core Agent Module

Comprehensive async agent framework for intelligent, context-aware agents.
"""

import asyncio
import uuid
from enum import Enum

from pydantic import BaseModel, Field

from grami_ai.core.interfaces import AgentInterface, WebSocketInterface
from grami_ai.core.tools import AsyncBaseTool
from grami_ai.core.prompt import AgentPrompt
from grami_ai.core.logger import logger
from grami_ai.core.memory import AsyncMemory, AsyncInMemoryMemory
from grami_ai.core.config import Settings
from grami_ai.llms.base import BaseLLMProvider

class AgentType(Enum):
    """Predefined agent types"""
    CONVERSATIONAL = 1
    TASK_ORIENTED = 2
    RESEARCH = 3
    CREATIVE = 4

class AgentConfig(BaseModel):
    """Comprehensive agent configuration"""
    model_config = Field(arbitrary_types_allowed=True)
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(default="GramiAgent")
    type: AgentType = Field(default=AgentType.CONVERSATIONAL)
    
    # LLM Configuration
    llm_provider: BaseLLMProvider
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=1500)
    
    # Memory Configuration
    memory: AsyncMemory = Field(default_factory=AsyncInMemoryMemory)
    memory_retention_window: int = Field(default=10)
    
    # Goal and Prompt Configuration
    goals: list = Field(default_factory=list)
    prompt_config: dict = Field(default_factory=dict)
    prompt: dict
    
    # Interface Configuration
    interface: AgentInterface = Field(default_factory=WebSocketInterface)
    
    # Tool Configuration
    tools: list = Field(default_factory=list)
    
    def __init__(self, **data):
        if 'prompt' in data and 'prompt_config' not in data:
            data['prompt_config'] = data.pop('prompt')
        super().__init__(**data)

class AsyncAgent:
    """
    Advanced Async Agent with comprehensive capabilities
    
    Features:
    - Multi-modal goal tracking
    - Sophisticated memory management
    - Flexible communication interfaces
    - Dynamic tool integration
    - Configurable LLM interaction
    """
    
    def __init__(
        self, 
        config: AgentConfig
    ):
        """
        Initialize a sophisticated async agent
        
        Args:
            config: Comprehensive agent configuration
        """
        # Use default configuration if not provided
        self.config = config
        
        # Setup core components
        self.id = self.config.id
        self.name = self.config.name
        
        # Initialize LLM
        self.llm = self.config.llm_provider
        
        # Initialize memory
        self.memory = self.config.memory
        
        # Initialize interface
        self.interface = self.config.interface
        
        # Initialize tools
        self.tools = self.config.tools
        
        # Configure logging
        self.logger = logger.bind(
            agent_id=self.id,
            agent_name=self.name
        )
    
    async def initialize(self):
        """
        Comprehensive agent initialization routine
        
        Performs:
        - Memory warm-up
        - Interface setup
        - Tool validation
        """
        # Initialize memory
        await self.memory.initialize()
        
        # Setup interface
        await self.interface.initialize(self)
        
        # Validate and prepare tools
        for tool in self.tools:
            await tool.validate()
    
    async def process_goal(
        self, 
        goal: dict
    ) -> dict:
        """
        Process and track agent goals
        
        Args:
            goal: Goal description or dict instance
        
        Returns:
            Goal processing result
        """
        # Prepare goal processing prompt
        prompt = self._construct_goal_prompt(goal)
        
        # Generate goal strategy
        strategy = await self.llm.generate(
            prompt, 
            temperature=self.config.temperature
        )
        
        # Store goal in memory
        await self.memory.store_goal(goal, strategy)
        
        return {
            "goal": goal,
            "strategy": strategy
        }
    
    def _construct_goal_prompt(self, goal: dict) -> str:
        """
        Construct a comprehensive prompt for goal processing
        
        Args:
            goal: Agent goal to process
        
        Returns:
            Constructed prompt
        """
        base_prompt = f"""
        Goal Processing for Agent: {self.name}
        
        Goal Description: {goal.get("description", "Not specified")}
        Priority: {goal.get("priority", "Not specified")}
        Success Criteria: {goal.get("success_criteria", "Not specified")}
        
        Tasks:
        1. Develop a comprehensive strategy
        2. Break down the goal into actionable steps
        3. Identify potential challenges
        4. Propose mitigation strategies
        
        Provide a detailed, structured response.
        """
        
        return base_prompt
    
    async def communicate(
        self, 
        message: str, 
        context: dict = {}
    ):
        """
        Communicate through the agent's interface
        
        Args:
            message: Message to communicate
            context: Additional context
        
        Yields:
            Response chunks
        """
        # Retrieve relevant memory
        relevant_memory = await self.memory.retrieve(message)
        
        # Construct communication prompt
        prompt = self._construct_communication_prompt(
            message, 
            context, 
            relevant_memory
        )
        
        # Stream response through interface
        async for chunk in self.llm.stream(prompt):
            yield chunk
            
            # Optionally store in memory
            await self.memory.store_interaction(
                message, 
                chunk, 
                context
            )
    
    def _construct_communication_prompt(
        self, 
        message: str, 
        context: dict,
        memory: list
    ) -> str:
        """
        Construct a comprehensive communication prompt
        
        Args:
            message: Incoming message
            context: Communication context
            memory: Relevant memory entries
        
        Returns:
            Constructed prompt
        """
        base_prompt = f"""
        Agent: {self.name}
        Communication Context:
        
        Incoming Message: {message}
        Context Details: {context}
        
        Relevant Memory:
        {memory}
        
        Respond thoughtfully, considering context and past interactions.
        """
        
        return base_prompt
    
    async def add_tool(self, tool):
        """
        Dynamically add a tool to the agent
        
        Args:
            tool: Tool to add
        """
        await tool.validate()
        self.tools.append(tool)
    
    async def close(self):
        """
        Gracefully close agent resources
        """
        await self.memory.close()
        await self.interface.close()
