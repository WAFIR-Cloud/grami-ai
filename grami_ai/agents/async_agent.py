"""
Asynchronous Agent Implementation for GRAMI AI.

This module provides an asynchronous agent implementation that extends the BaseAgent
with async capabilities for non-blocking operations.
"""

from typing import Any, Dict, List, Optional

from grami_ai.agents.base_agent import BaseAgent
from grami_ai.memory import AbstractMemory
from grami_ai.tools import AbstractTool


class AsyncAgent(BaseAgent):
    """
    Asynchronous Agent that extends BaseAgent with async capabilities.
    
    This agent is designed for high-performance, non-blocking operations in
    enterprise environments. It supports all the features of BaseAgent while
    providing async execution capabilities.
    """
    
    def __init__(
        self,
        tools: Optional[List[AbstractTool]] = None,
        memory: Optional[AbstractMemory] = None,
        model: str = "gpt-3.5-turbo",
        provider_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize AsyncAgent.
        
        Args:
            tools: List of tools available to the agent
            memory: Memory backend for conversation history
            model: Model identifier to use
            provider_config: Provider-specific configuration
            **kwargs: Additional configuration options
        """
        super().__init__(
            tools=tools,
            memory=memory,
            model=model,
            provider_config=provider_config,
            **kwargs
        )
    
    async def execute_task(self, task: Dict[str, Any]) -> Any:
        """
        Execute a task asynchronously.
        
        Args:
            task: Task specification including objective and input
            
        Returns:
            Task execution result
        """
        return await self._execute_task_async(task)
    
    async def _execute_task_async(self, task: Dict[str, Any]) -> Any:
        """
        Internal method for async task execution.
        
        Args:
            task: Task specification
            
        Returns:
            Task execution result
        """
        # Validate task format
        self._validate_task(task)
        
        # Initialize conversation with system message
        messages = self._initialize_conversation(task)
        
        # Get response from LLM
        response = await self.llm.send_message(messages)
        
        # Process and return result
        return self._process_response(response)
