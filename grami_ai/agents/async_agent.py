"""
Asynchronous Agent Implementation for GRAMI AI.

This module provides an asynchronous agent implementation that extends the BaseAgent
with async capabilities for non-blocking operations.
"""

from typing import Any, Dict, List, Optional, Union
import asyncio

from grami_ai.agents.base_agent import BaseAgent
from grami_ai.memory import AbstractMemory
from grami_ai.tools.base_tools import AbstractTool
from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.core.logging import logger
from grami_ai.llms.role import Role  # Import Role enum


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
        llm_provider: Optional[BaseLLMProvider] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize AsyncAgent.
        
        Args:
            tools: List of tools available to the agent
            memory: Memory backend for conversation history
            llm_provider: Required LLM provider for agent interactions
            **kwargs: Additional configuration options
        
        Raises:
            ValueError: If no LLM provider is specified
        """
        if llm_provider is None:
            raise ValueError("An LLM provider must be explicitly specified during AsyncAgent initialization.")
        
        # Initialize tools
        self.tools = tools or []
        
        # Initialize LLM provider
        self.llm = llm_provider
        
        # Call parent initialization
        super().__init__(
            tools=self.tools,
            memory=memory,
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
    
    async def _execute_task_async(self, task: Dict[str, Any]) -> Optional[str]:
        """
        Asynchronously execute a task with tools and LLM.
        
        Args:
            task (Dict[str, Any]): Task configuration
        
        Returns:
            Optional[str]: Task execution result
        """
        # Validate task structure
        if not isinstance(task, dict):
            raise ValueError("Task must be a dictionary")
        
        # Ensure required keys are present
        required_keys = ['objective', 'content']
        for key in required_keys:
            if key not in task:
                raise ValueError(f"Task is missing required key: {key}")
        
        # Prepare messages for LLM
        messages = [
            {
                'role': Role.SYSTEM,
                'content': f"Objective: {task.get('objective', 'Perform task')}"
            },
            {
                'role': Role.USER,
                'content': task['content']
            }
        ]
        
        # Execute tools if present
        if 'tools' in task:
            for tool_config in task['tools']:
                try:
                    tool_name = tool_config.get('name')
                    method = tool_config.get('method')
                    args = tool_config.get('args', [])
                    
                    # Find the tool by name
                    tool = next((t for t in self.tools if t.name == tool_name), None)
                    
                    if tool:
                        # Execute tool method
                        result = await tool.run(method, *args)
                        
                        # Add tool result to messages
                        messages.append({
                            'role': Role.TOOL,
                            'content': f"Tool {tool_name} result: {result}"
                        })
                except Exception as e:
                    # Log tool execution error
                    messages.append({
                        'role': Role.TOOL,
                        'content': f"Tool {tool_name} execution failed: {str(e)}"
                    })
        
        # Start a new chat session
        conversation = await self.llm.start_chat()
        
        # Combine messages into a single message
        combined_message = "\n".join([
            msg['content'] for msg in messages
        ])
        
        # Send combined message
        response = await self.llm.send_message(conversation, combined_message)
        
        # Process and return result
        return self._process_response(response)
    
    def _process_response(self, response: Union[str, Dict[str, Any]]) -> str:
        """
        Process the LLM response.
        
        Args:
            response: Raw response from the LLM
        
        Returns:
            Processed response as a string
        """
        # If response is a dictionary, extract text content
        if isinstance(response, dict):
            response = response.get('content', str(response))
        
        # Ensure response is a string
        return str(response).strip()
    
    def _validate_task(self, task: Dict[str, Any]) -> None:
        """
        Validate the task dictionary to ensure it has required fields.
        
        Args:
            task: Task specification to validate
        
        Raises:
            ValueError: If task is missing required fields or has invalid format
        """
        if not isinstance(task, dict):
            raise ValueError("Task must be a dictionary")
        
        required_keys = ['objective', 'input']
        for key in required_keys:
            if key not in task:
                raise ValueError(f"Task is missing required key: {key}")
        
        if not isinstance(task.get('objective'), str):
            raise ValueError("Task 'objective' must be a string")
        
        if not isinstance(task.get('input'), (str, dict, list)):
            raise ValueError("Task 'input' must be a string, dictionary, or list")
        
        # Optional constraints validation
        if 'constraints' in task:
            constraints = task.get('constraints')
            if not isinstance(constraints, list):
                raise ValueError("Task 'constraints' must be a list of strings")
            
            if not all(isinstance(constraint, str) for constraint in constraints):
                raise ValueError("All task constraints must be strings")

    def _initialize_conversation(self, task: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Initialize conversation messages for task execution.
        
        Args:
            task: Task specification dictionary
        
        Returns:
            List of conversation messages
        """
        messages = [
            {
                "role": "system", 
                "content": "You are a privacy-focused AI assistant designed to process tasks securely and efficiently."
            },
            {
                "role": "user", 
                "content": task.get('objective', 'Process task')
            }
        ]
        
        # Add input to the conversation
        messages.append({
            "role": "user", 
            "content": str(task.get('input', ''))
        })
        
        # Incorporate constraints if provided
        if 'constraints' in task:
            constraints_str = "Please adhere to the following constraints:\n" + "\n".join(task['constraints'])
            messages.append({
                "role": "user", 
                "content": constraints_str
            })
        
        return messages
