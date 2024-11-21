# GRAMI AI: The Modern Async AI Agent Framework

[![Documentation Status](https://readthedocs.org/projects/grami-ai/badge/?version=latest)](https://grami-ai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/grami-ai.svg)](https://badge.fury.io/py/grami-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🤖 GRAMI AI Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

GRAMI AI is an open-source, async-first Python framework for building intelligent, modular AI agents. It provides a robust foundation for creating, managing, and orchestrating AI agents with a focus on flexibility, performance, and extensibility.

## 🌟 Features

- **Async-First Architecture**: Built from the ground up for high-performance async operations
- **Modular Design**: Easily extend and customize components
- **Multi-Provider Support**: Works with OpenAI, Anthropic, Cohere, and more
- **Robust Memory Management**: Multiple backend options (Redis, PostgreSQL, MongoDB)
- **Event-Driven**: Real-time updates and communication between agents
- **Type-Safe**: Comprehensive type hints for better IDE support
- **Production-Ready**: Built-in monitoring, logging, and error handling

## 🏗️ Architecture

```
                                GRAMI AI Architecture
                                
┌─────────────────────────────────────────────────────────────────────┐
│                           Client Applications                        │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────┐
│                              API Layer                              │
└───────────────────────────────────┬─────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────┐
│                           Agent Orchestrator                         │
├─────────────┬─────────────┬─────────────┬─────────────┬────────────┤
│  Agent 1    │   Agent 2   │   Agent 3   │   Agent 4   │  Agent N   │
└─────┬───────┴──────┬──────┴──────┬──────┴──────┬──────┴─────┬──────┘
      │              │              │             │            │
┌─────▼──────┬──────▼──────┬───────▼─────┬──────▼─────┬─────▼──────┐
│   Memory   │   Events    │    Tools    │  Providers │  Security  │
└────────────┴────────────┴─────────────┴────────────┴────────────┘
```

## 🚀 Quick Start

1. Install GRAMI AI:
```bash
pip install grami-ai
```

2. Create your first agent:
```python
from grami_ai import BaseAgent, Tool, Memory
from grami_ai.core.config import settings

class MyAgent(BaseAgent):
    async def initialize(self):
        # Set up agent-specific configuration
        self.memory = Memory(backend=settings.memory.backend)
        self.tools = [Tool1(), Tool2()]
    
    async def execute_task(self, task):
        # Implement task execution logic
        result = await self.process_task(task)
        await self.memory.store(result)
        return result

# Create and run agent
agent = MyAgent()
await agent.start()
```

3. Assign tasks to your agent:
```python
from grami_ai.core.constants import Priority

# Create a task
task = {
    "objective": "Analyze this text document",
    "input": "Sample text for analysis",
    "priority": Priority.HIGH
}

# Assign and execute task
result = await agent.execute_task(task)
```

## 📦 Core Components

### 1. Agents
- Base agent class with common functionality
- Customizable behavior and capabilities
- Built-in task queue and priority handling

### 2. Memory
- Multiple backend support (Redis, PostgreSQL, MongoDB)
- Automatic data serialization/deserialization
- Configurable retention and indexing

### 3. Events
- Real-time communication between agents
- Kafka-based event streaming
- Event filtering and routing

### 4. Tools
- Extensible tool interface
- Built-in common tools
- Custom tool development support

### 5. Configuration
- Environment-specific settings
- Secure secrets management
- Dynamic configuration updates

## 🔧 Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grami-ai.git
cd grami-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest tests/
```

## 📖 Documentation

Full documentation is available at [docs.grami-ai.org](https://docs.grami-ai.org)

- [Getting Started Guide](https://docs.grami-ai.org/getting-started)
- [API Reference](https://docs.grami-ai.org/api)
- [Examples](https://docs.grami-ai.org/examples)
- [Contributing Guide](https://docs.grami-ai.org/contributing)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The amazing open-source community
- All our contributors and users

## Vision

Grami AI is designed to revolutionize how developers build AI agents by providing a modern, async-first framework that emphasizes:

- **Asynchronous by Default**: Built from the ground up for high-performance, non-blocking operations
- **Modular Architecture**: Plug-and-play components for tools, memory, and LLM providers
- **Type Safety**: Comprehensive type hints and protocol-based interfaces
- **Production Ready**: Built for reliability and scalability in real-world applications

## Quick Start

```bash
# Install the base package
pip install grami-ai

# Install with optional features
pip install grami-ai[gemini]    # For Google Gemini support
pip install grami-ai[ollama]    # For Ollama support
pip install grami-ai[dev]       # For development tools
```

### Basic Usage

```python
from grami_ai.agent import AsyncAgent
from grami_ai.tools import CalculatorTool, WebScraperTool
from grami_ai.memory import InMemoryAbstractMemory

async def main():
    # Initialize agent with tools and memory
    agent = AsyncAgent(
        tools=[CalculatorTool(), WebScraperTool()],
        memory=InMemoryAbstractMemory(),
        model="gemini-pro"  # or "gpt-3.5-turbo", "ollama/llama2", etc.
    )
    
    # Execute tasks asynchronously
    result = await agent.execute(
        "Calculate the square root of the number of words on example.com"
    )
    print(result)

# Run the async function
import asyncio
asyncio.run(main())
```

## Architecture

Grami AI is built on three core pillars:

### 1. Tools System
- Protocol-based tool definition
- Async execution
- Built-in validation and error handling
- Extensive tool library (web scraping, calculations, file operations, etc.)

```python
from grami_ai.core.interfaces import AsyncTool
from typing import Any, Dict

class MyCustomTool(AsyncTool):
    async def run(self, input_data: str, **kwargs) -> Dict[str, Any]:
        # Your async tool implementation
        return {"result": processed_data}
```

### 2. Memory Management
- Flexible memory backends (In-Memory, Redis, Custom)
- Automatic context management
- Memory size limits and pruning strategies

```python
from grami_ai.memory import RedisMemory

memory = RedisMemory(
    redis_url="redis://localhost:6379",
    max_items=1000,
    ttl=3600  # 1 hour
)
```

### 3. LLM Integration
- Support for multiple LLM providers
- Streaming responses
- Token management
- Retry mechanisms

```python
from grami_ai.llm import GeminiProvider

llm = GeminiProvider(
    api_key="your-api-key",
    model="gemini-pro",
    max_tokens=1000
)
```

## Advanced Features

### Parallel Tool Execution
```python
async def parallel_execution():
    tools = [WebScraperTool(), CalculatorTool(), StringTool()]
    results = await asyncio.gather(*[
        tool.execute(input_data) 
        for tool in tools
    ])
```

### Custom Memory Backend
```python
from grami_ai.core.interfaces import AsyncMemoryProvider

class MyCustomMemory(AsyncMemoryProvider):
    async def add_item(self, key: str, value: dict) -> None:
        # Implementation
        pass

    async def get_items(self, key: str) -> list:
        # Implementation
        pass
```

### Error Handling
```python
from grami_ai.exceptions import ToolExecutionError

try:
    result = await agent.execute("complex task")
except ToolExecutionError as e:
    print(f"Tool execution failed: {e}")
```

## Documentation

Comprehensive documentation is available at [grami-ai.readthedocs.io](https://grami-ai.readthedocs.io/), including:

- Getting Started Guide
- API Reference
- Advanced Usage Examples
- Contributing Guidelines

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Write your changes
4. Write tests for your changes
5. Submit a pull request

```bash
# Development setup
git clone https://github.com/grami-ai/framework.git
cd framework
pip install -e .[dev]
pytest
```

## License

MIT License

Copyright (c) 2024 YAFATEK Solutions

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Links

- [Documentation](https://grami-ai.readthedocs.io/)
- [GitHub Repository](https://github.com/grami-ai/framework)
- [Issue Tracker](https://github.com/grami-ai/framework/issues)
- [PyPI Package](https://pypi.org/project/grami-ai/)
