from typing import List, Dict, Any, Optional
from ..core.interfaces import AsyncTool, AsyncMemoryProvider, AsyncKafkaIntegration
from ..memory import InMemoryAbstractMemory
from ..events import KafkaEvents

class BaseAgent:
    """Base agent class for GRAMI's AI crew members.
    
    This class provides the foundation for all specialized agents in the GRAMI ecosystem,
    including memory management, event handling, and tool execution capabilities.
    
    Key Features:
    - Async-first design for high performance
    - Integrated Redis-based memory management
    - Kafka event publishing and subscription
    - Modular tool system
    - Error handling and logging
    """
    
    def __init__(
        self,
        tools: Optional[List[AsyncTool]] = None,
        memory: Optional[AsyncMemoryProvider] = None,
        kafka: Optional[AsyncKafkaIntegration] = None,
        model: str = "gemini-pro",
        **kwargs: Dict[str, Any]
    ):
        """Initialize a new agent.
        
        Args:
            tools: List of async tools available to this agent
            memory: Memory provider for context management (defaults to Redis)
            kafka: Kafka integration for event handling
            model: LLM model to use (default: gemini-pro)
            **kwargs: Additional configuration options
        """
        self.tools = tools or []
        self.memory = memory or InMemoryAbstractMemory()
        self.kafka = kafka or KafkaEvents()
        self.model = model
        self.config = kwargs
        
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task using available tools and memory.
        
        Args:
            task: Task description or command
            context: Additional context for task execution
            
        Returns:
            Dict containing task results and any relevant metadata
        """
        # Store task in memory
        task_id = await self._store_task(task, context)
        
        try:
            # Publish task started event
            await self.kafka.publish(
                "task_events",
                {
                    "task_id": task_id,
                    "agent": self.__class__.__name__,
                    "status": "started",
                    "task": task
                }
            )
            
            # Execute task using appropriate tools
            results = {}
            for tool in self.tools:
                if tool.can_handle(task):
                    result = await tool.execute(task, context=context)
                    results[tool.__class__.__name__] = result
            
            # Store results in memory
            await self._store_results(task_id, results)
            
            # Publish task completed event
            await self.kafka.publish(
                "task_events",
                {
                    "task_id": task_id,
                    "agent": self.__class__.__name__,
                    "status": "completed",
                    "results": results
                }
            )
            
            return {
                "task_id": task_id,
                "status": "success",
                "results": results,
                "model": self.model
            }
            
        except Exception as e:
            # Handle errors and publish error event
            error_data = {
                "task_id": task_id,
                "agent": self.__class__.__name__,
                "status": "failed",
                "error": str(e)
            }
            await self._store_error(task_id, error_data)
            await self.kafka.publish("error_events", error_data)
            raise
    
    async def _store_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Store task details in memory and return task ID."""
        task_data = {
            "task": task,
            "status": "started",
            "context": context or {},
            "agent": self.__class__.__name__
        }
        task_id = await self.memory.add_item("tasks", task_data)
        return task_id
    
    async def _store_results(self, task_id: str, results: Dict[str, Any]) -> None:
        """Store task results in memory."""
        await self.memory.add_item(
            f"results:{task_id}",
            {
                "status": "completed",
                "results": results,
                "timestamp": "utc_timestamp_here"
            }
        )
    
    async def _store_error(self, task_id: str, error_data: Dict[str, Any]) -> None:
        """Store error information in memory."""
        await self.memory.add_item(
            f"errors:{task_id}",
            error_data
        )
    
    async def get_history(
        self,
        key: str = "tasks",
        filter_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve agent's task history with optional filtering.
        
        Args:
            key: Memory key to retrieve (default: "tasks")
            filter_params: Optional parameters to filter results
            
        Returns:
            List of historical tasks and their results
        """
        return await self.memory.get_items(key, filter_params)
    
    def add_tool(self, tool: AsyncTool) -> None:
        """Add a new tool to the agent's toolkit."""
        self.tools.append(tool)
    
    def remove_tool(self, tool_name: str) -> None:
        """Remove a tool from the agent's toolkit."""
        self.tools = [t for t in self.tools if t.__class__.__name__ != tool_name]
    
    async def subscribe_to_events(self, topic: str, callback: callable) -> None:
        """Subscribe to Kafka events on a specific topic."""
        await self.kafka.subscribe(topic, callback)
