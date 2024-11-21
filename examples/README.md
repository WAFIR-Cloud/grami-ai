# 📚 GRAMI AI Examples

This directory contains various examples demonstrating how to use the GRAMI AI framework. Each example is designed to showcase different features and use cases.

## 🚀 Getting Started

1. Make sure you have GRAMI AI installed:
```bash
pip install grami-ai
```

2. Install additional dependencies for examples:
```bash
pip install -e ".[examples]"
```

## 📂 Example Categories

### Basic Examples
- [`basic_gemini_agent.py`](basic_gemini_agent.py): Simple agent using Google's Gemini model
- [`memory_usage.py`](memory_usage.py): Basic memory operations and persistence
- [`tools_usage.py`](tools_usage.py): Working with built-in and custom tools

### Advanced Examples
- [`advanced_agent_usage.py`](advanced_agent_usage.py): Complex agent patterns and configurations
- [`advanced_tools.py`](advanced_tools.py): Creating sophisticated custom tools
- [`multi_tool_workflow.py`](multi_tool_workflow.py): Orchestrating multiple tools in a workflow

### Real-World Applications
- [`ai_research_assistant.py`](ai_research_assistant.py): AI-powered research assistant
- [`data_analysis_pipeline.py`](data_analysis_pipeline.py): Data processing and analysis pipeline
- [`custom_llm_provider.py`](custom_llm_provider.py): Integrating custom LLM providers

## 🎯 Common Use Cases

### 1. Creating a Basic Agent
```python
from grami_ai import BaseAgent
from grami_ai.core.config import settings

class SimpleAgent(BaseAgent):
    async def initialize(self):
        self.memory = Memory(backend="redis")
        self.tools = [WebSearchTool(), CalculatorTool()]
    
    async def execute_task(self, task):
        return await self.process_with_tools(task)

# Usage
agent = SimpleAgent()
result = await agent.execute_task({"query": "What is 2+2?"})
```

### 2. Using Memory
```python
from grami_ai.memory import RedisMemory

# Initialize memory
memory = RedisMemory(
    host=settings.redis.host,
    port=settings.redis.port
)

# Store and retrieve data
await memory.store("key1", {"data": "value1"})
data = await memory.retrieve("key1")
```

### 3. Creating Custom Tools
```python
from grami_ai.tools import BaseTool

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "A custom tool example"
    
    async def _execute(self, **kwargs):
        # Tool implementation
        return {"result": "Custom tool output"}

# Usage with agent
agent.add_tool(CustomTool())
```

### 4. Event Handling
```python
from grami_ai.events import EventHandler
from grami_ai.core.constants import EventType

class MyEventHandler(EventHandler):
    async def handle_event(self, event):
        if event.type == EventType.TASK_COMPLETED:
            await self.process_completion(event.data)

# Usage
handler = MyEventHandler()
await handler.subscribe("task_events")
```

## 🔄 Running Examples

Each example can be run directly:
```bash
python -m examples.basic_gemini_agent
```

Or imported and used in your code:
```python
from examples.basic_gemini_agent import GeminiAgent

agent = GeminiAgent()
result = await agent.run()
```

## 📝 Notes

- Examples assume you have configured environment variables (see `.env.example`)
- Some examples require additional dependencies (specified in `setup.py`)
- For production use, implement proper error handling and logging
- See inline comments for detailed explanations

## 🤝 Contributing

Feel free to contribute your own examples! Please follow these guidelines:
1. Include clear documentation and comments
2. Follow the project's coding style
3. Add any required dependencies to `setup.py`
4. Update this README with your example

## 🔗 Related Resources

- [Full Documentation](https://docs.grami-ai.org)
- [API Reference](https://docs.grami-ai.org/api)
- [Contributing Guide](https://docs.grami-ai.org/contributing)
