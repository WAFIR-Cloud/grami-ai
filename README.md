# Grami AI: The Modern Async AI Agent Framework

[![Documentation Status](https://readthedocs.org/projects/grami-ai/badge/?version=latest)](https://grami-ai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/grami-ai.svg)](https://badge.fury.io/py/grami-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
