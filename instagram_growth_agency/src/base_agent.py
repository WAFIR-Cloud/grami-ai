import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AgentConfig(BaseModel):
    """Configuration for digital marketing agents."""
    name: str
    description: str
    model: str = "gpt-4"
    temperature: float = 0.7

class BaseDigitalMarketingAgent(ABC):
    """Abstract base class for digital marketing agents."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{config.name}")
        self.logger.setLevel(logging.INFO)
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a specific task for the agent.
        
        Args:
            task (Dict[str, Any]): Task details to be processed
        
        Returns:
            Dict[str, Any]: Processed task result
        """
        pass
    
    async def communicate(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Simulate agent communication with potential LLM integration.
        
        Args:
            message (str): Message to process
            context (Optional[Dict[str, Any]], optional): Additional context. Defaults to None.
        
        Returns:
            str: Response from the agent
        """
        # Placeholder for LLM interaction
        return f"Agent {self.config.name} received: {message}"
    
    def log_task(self, task: Dict[str, Any], status: str):
        """
        Log task processing details.
        
        Args:
            task (Dict[str, Any]): Task details
            status (str): Processing status
        """
        self.logger.info(f"Task {task.get('id', 'Unknown')} - Status: {status}")

class AgentError(Exception):
    """Custom exception for agent-related errors."""
    pass
