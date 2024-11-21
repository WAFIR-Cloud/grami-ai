# 🚀 GRAMI AI Quickstart Guide

This guide will help you get started with GRAMI AI quickly. We'll cover installation, basic setup, and common usage patterns.

## 📦 Installation

1. Install GRAMI AI using pip:
```bash
pip install grami-ai
```

2. For development with additional tools:
```bash
pip install -e ".[dev,docs,test]"
```

## 🔧 Basic Setup

1. Create a `.env` file in your project root:
```env
GRAMI_ENV=development
GRAMI_LOG_LEVEL=INFO
GRAMI_MEMORY_BACKEND=redis
GRAMI_REDIS_HOST=localhost
GRAMI_REDIS_PORT=6379
```

2. Initialize your project:
```python
from grami_ai.core.config import settings
from grami_ai.core.utils import setup_logging

# Setup logging
setup_logging()

# Verify configuration
print(f"Environment: {settings.env}")
print(f"Memory Backend: {settings.memory.backend}")
```

## 🤖 Creating Your First Agent

1. Create a basic agent:
```python
from grami_ai import BaseAgent
from grami_ai.memory import RedisMemory
from grami_ai.tools import WebSearchTool, CalculatorTool

class MyFirstAgent(BaseAgent):
    async def initialize(self):
        # Setup memory
        self.memory = RedisMemory(
            host=settings.redis.host,
            port=settings.redis.port
        )
        
        # Add tools
        self.tools = [
            WebSearchTool(),
            CalculatorTool()
        ]
    
    async def execute_task(self, task):
        # Process task with tools
        result = await self.process_with_tools(task)
        
        # Store result in memory
        await self.memory.store(
            f"task_{task['id']}", 
            result
        )
        
        return result

# Create and run agent
agent = MyFirstAgent()
await agent.start()
```

2. Use your agent:
```python
# Create a task
task = {
    "id": "task_001",
    "objective": "Calculate the square root of 16 and search for its history",
    "tools_needed": ["calculator", "web_search"]
}

# Execute task
result = await agent.execute_task(task)
print(result)
```

## 🧰 Working with Tools

1. Create a custom tool:
```python
from grami_ai.tools import BaseTool
from typing import Dict, Any

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "A custom tool for specific tasks"
    
    async def _execute(self, **kwargs) -> Dict[str, Any]:
        # Implement tool logic
        input_data = kwargs.get("input")
        processed_result = await self.process_data(input_data)
        return {"result": processed_result}
    
    async def process_data(self, data):
        # Custom processing logic
        return f"Processed: {data}"
```

2. Use multiple tools in a workflow:
```python
from grami_ai.tools import ToolChain

# Create tool chain
chain = ToolChain([
    WebSearchTool(),
    CustomTool(),
    CalculatorTool()
])

# Execute chain
result = await chain.execute({
    "search": "quantum computing",
    "process": "search_results",
    "calculate": "result_metrics"
})
```

## 📝 Working with Memory

1. Basic memory operations:
```python
from grami_ai.memory import RedisMemory

# Initialize memory
memory = RedisMemory()

# Store data
await memory.store("key1", {"data": "value1"})

# Retrieve data
data = await memory.retrieve("key1")

# Search data
results = await memory.search({"data": "value1"})

# Delete data
await memory.delete("key1")
```

2. Using memory filters:
```python
# Get all entries from last hour
from datetime import datetime, timedelta
results = await memory.filter(
    created_after=datetime.now() - timedelta(hours=1)
)

# Get entries by type
results = await memory.filter(
    entry_type="task_result"
)
```

## 🎯 Event Handling

1. Create an event handler:
```python
from grami_ai.events import EventHandler
from grami_ai.core.constants import EventType

class TaskEventHandler(EventHandler):
    async def handle_event(self, event):
        if event.type == EventType.TASK_COMPLETED:
            await self.process_completion(event.data)
        elif event.type == EventType.TASK_FAILED:
            await self.handle_failure(event.data)
    
    async def process_completion(self, data):
        # Handle task completion
        pass
    
    async def handle_failure(self, data):
        # Handle task failure
        pass
```

2. Use events in your agent:
```python
# Create handler
handler = TaskEventHandler()

# Subscribe to events
await handler.subscribe("task_events")

# Emit events
await agent.emit_event(
    EventType.TASK_COMPLETED,
    {"task_id": "001", "result": "success"}
)
```

## 🔍 Monitoring and Logging

1. Configure logging:
```python
from grami_ai.core.utils import setup_logging
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Use logger
logger.info("Agent started")
logger.error("Task failed", extra={"task_id": "001"})
```

2. Monitor agent status:
```python
# Get agent status
status = await agent.get_status()
print(f"Active Tasks: {status['active_tasks']}")
print(f"Memory Usage: {status['memory_usage']}")
print(f"Tool Stats: {status['tool_stats']}")
```

## 🚨 Error Handling

1. Use built-in exceptions:
```python
from grami_ai.core.exceptions import (
    GramiError,
    ValidationError,
    ResourceError
)

try:
    result = await agent.execute_task(task)
except ValidationError as e:
    logger.error(f"Invalid task: {e}")
except ResourceError as e:
    logger.error(f"Resource unavailable: {e}")
except GramiError as e:
    logger.error(f"General error: {e}")
```

## 📚 Next Steps

- Explore the [full documentation](https://docs.grami-ai.org)
- Check out [example projects](https://github.com/yourusername/grami-ai/tree/main/examples)
- Join our [community](https://discord.gg/grami-ai)
- Contribute to the [project](https://github.com/yourusername/grami-ai)

## 🤝 Getting Help

- Read the [FAQ](https://docs.grami-ai.org/faq)
- Join our [Discord](https://discord.gg/grami-ai)
- Open an [issue](https://github.com/yourusername/grami-ai/issues)
- Check [Stack Overflow](https://stackoverflow.com/questions/tagged/grami-ai)
