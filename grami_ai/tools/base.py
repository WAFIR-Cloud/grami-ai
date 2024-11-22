import abc
import asyncio
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum, auto

from grami_ai.core.logger import AsyncLogger
from grami_ai.core.exceptions import ToolConfigurationError, ToolExecutionError

class ToolCategory(Enum):
    """
    Comprehensive categorization of tools
    """
    SEARCH = auto()
    COMPUTATION = auto()
    COMMUNICATION = auto()
    DATA_PROCESSING = auto()
    SYSTEM_INTERACTION = auto()
    EXTERNAL_API = auto()
    MACHINE_LEARNING = auto()
    VISUALIZATION = auto()
    CUSTOM = auto()

@dataclass
class ToolMetadata:
    """
    Comprehensive metadata for tools
    """
    name: str
    description: str
    category: ToolCategory
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    performance_score: float = 0.5
    reliability_score: float = 0.5
    required_env_vars: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

class AsyncBaseTool(abc.ABC):
    """
    Abstract base class for async tools in the Grami AI framework
    """
    def __init__(
        self, 
        metadata: Optional[ToolMetadata] = None,
        logger: Optional[AsyncLogger] = None
    ):
        """
        Initialize a base tool
        
        Args:
            metadata: Tool metadata
            logger: Optional custom logger
        """
        self.metadata = metadata or self._generate_default_metadata()
        self.logger = logger or AsyncLogger()
    
    def _generate_default_metadata(self) -> ToolMetadata:
        """
        Generate default metadata based on class information
        
        Returns:
            Generated ToolMetadata instance
        """
        return ToolMetadata(
            name=self.__class__.__name__,
            description=self._generate_default_description(),
            category=ToolCategory.CUSTOM
        )
    
    def _generate_default_description(self) -> str:
        """
        Generate a default description based on class name
        
        Returns:
            Generated description string
        """
        return f"A tool for performing {self.__class__.__name__.replace('Tool', '').lower()} operations"
    
    @abc.abstractmethod
    async def execute(
        self, 
        task: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute the tool asynchronously
        
        Args:
            task: Primary task or query
            context: Additional contextual information
        
        Returns:
            Result of tool execution
        
        Raises:
            ToolExecutionError: If tool execution fails
        """
        pass
    
    @abc.abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """
        Define tool-specific parameters
        
        Returns:
            A dictionary of parameter definitions
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tool metadata to a dictionary
        
        Returns:
            Dictionary representation of tool metadata
        """
        return {
            "name": self.metadata.name,
            "description": self.metadata.description,
            "category": self.metadata.category.name,
            "version": self.metadata.version,
            "performance_score": self.metadata.performance_score,
            "reliability_score": self.metadata.reliability_score
        }

class ToolRegistry:
    """
    Centralized tool management system
    """
    def __init__(self):
        """Initialize tool registry"""
        self._tools: Dict[str, AsyncBaseTool] = {}
        self._category_map: Dict[ToolCategory, List[str]] = {}
    
    def register_tool(self, tool: AsyncBaseTool):
        """
        Register a tool in the registry
        
        Args:
            tool: Tool instance to register
        
        Raises:
            ValueError: If tool with same name already exists
        """
        name = tool.metadata.name
        category = tool.metadata.category
        
        if name in self._tools:
            raise ValueError(f"Tool {name} already registered")
        
        self._tools[name] = tool
        
        # Update category map
        if category not in self._category_map:
            self._category_map[category] = []
        self._category_map[category].append(name)
    
    def get_tool(self, name: str) -> AsyncBaseTool:
        """
        Retrieve a tool by name
        
        Args:
            name: Tool name
        
        Returns:
            Registered tool instance
        
        Raises:
            KeyError: If tool not found
        """
        return self._tools[name]
    
    def list_tools(
        self, 
        category: Optional[ToolCategory] = None
    ) -> List[Dict[str, Any]]:
        """
        List available tools, optionally filtered by category
        
        Args:
            category: Optional tool category to filter
        
        Returns:
            List of tool metadata dictionaries
        """
        if category:
            tool_names = self._category_map.get(category, [])
            return [self._tools[name].to_dict() for name in tool_names]
        
        return [tool.to_dict() for tool in self._tools.values()]
    
    def add_content_generation_tool(self):
        """
        Add a default content generation tool to the registry
        
        Returns:
            ContentGenerationTool instance
        """
        from typing import Optional, List, Dict, Any
        import logging

        class ContentGenerationTool(AsyncBaseTool):
            def __init__(
                self, 
                metadata: Optional[ToolMetadata] = None,
                logger: Optional[AsyncLogger] = None
            ):
                """
                Initialize the Content Generation Tool
                
                Args:
                    metadata: Optional tool metadata
                    logger: Optional logger
                """
                default_metadata = ToolMetadata(
                    name="content_generation",
                    description="Generate social media content for various platforms",
                    category=ToolCategory.CUSTOM,
                    performance_score=0.8,
                    reliability_score=0.7,
                    tags=["social_media", "content", "generation"]
                )
                
                super().__init__(
                    metadata=metadata or default_metadata,
                    logger=logger
                )
                
                self.logger = logger or logging.getLogger(__name__)

            async def generate(
                self, 
                platform: str = 'instagram', 
                niche: str = 'general', 
                content_type: str = 'post',
                **kwargs
            ) -> Dict[str, Any]:
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

        # Create and register the tool
        content_tool = ContentGenerationTool()
        self.register_tool(content_tool)
        return content_tool

# Global tool registry instance
tool_registry = ToolRegistry()
