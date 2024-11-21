# GRAMI AI: The Modern Async AI Agent Framework

[![Documentation Status](https://readthedocs.org/projects/grami-ai/badge/?version=latest)](https://grami-ai.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/grami-ai.svg)](https://badge.fury.io/py/grami-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 🤖 GRAMI AI Framework

GRAMI is an advanced, privacy-focused async AI agent framework designed for enterprise applications. It provides a flexible, modular architecture for building AI agents with support for both private and cloud-based LLM providers.

## 🔐 Privacy-First Design

GRAMI prioritizes data privacy and security:
- **Local LLM Support**: First-class support for Ollama, enabling fully private AI deployments
- **Hybrid Options**: Use Google's Gemini for a balance of privacy and performance
- **Flexible Architecture**: Easy integration of any LLM provider, cloud or local

## 🚀 Quick Start

1. Install GRAMI:
```bash
pip install grami-ai
```

2. Choose your LLM provider:

```python
from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool

# For private deployment with Ollama
agent = AsyncAgent(
    tools=[CalculatorTool()],
    memory=InMemoryAbstractMemory(),
    model="ollama/llama2",  # or other Ollama models
    provider_config={
        "base_url": "http://localhost:11434"
    }
)

# For Google's Gemini
agent = AsyncAgent(
    tools=[CalculatorTool()],
    memory=InMemoryAbstractMemory(),
    model="gemini-pro",
    provider_config={
        "api_key": "your-google-api-key"
    }
)

# Execute tasks
result = await agent.execute_task({
    "objective": "Calculate compound interest",
    "input": "What is 5% interest compounded annually on $1000 for 3 years?"
})
```

## 🛠️ Features

- **Async-First**: Built for high-performance async operations
- **Provider Agnostic**: Support for multiple LLM providers:
  - 🏠 **Ollama**: Local deployment with models like Llama 2
  - 🌐 **Google Gemini**: Enterprise-grade cloud provider
  - ☁️ **OpenAI**: GPT-3.5/4 integration (optional)
  - 🤖 **Anthropic**: Claude models (optional)
- **Memory Systems**: Flexible memory backends
- **Tool Integration**: Extensible tool system
- **Type Safety**: Full type hints and validation
- **Enterprise Ready**: Built for production workloads

## 📚 Examples

See the [examples](examples/) directory for:
- Private AI deployment with Ollama
- Hybrid deployment with Google Gemini
- Advanced agent configurations
- Custom tool integration
- Memory system usage

## 🔧 Installation Options

```bash
# Core installation
pip install grami-ai

# With Gemini support
pip install grami-ai[gemini]

# With Ollama support (recommended for private deployment)
pip install grami-ai[ollama]

# With all providers
pip install grami-ai[all]
```

## 🔒 Security

GRAMI is designed with security in mind:
- No data leaves your infrastructure with local LLM deployment
- Secure API key handling
- Configurable safety settings
- Rate limiting and retry mechanisms

## 📖 Documentation

- [Full Documentation](https://docs.grami-ai.org)
- [API Reference](https://docs.grami-ai.org/api)
- [Security Guide](https://docs.grami-ai.org/security)
- [Provider Setup](https://docs.grami-ai.org/providers)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

GRAMI is licensed under MIT - see [LICENSE](LICENSE) for details.

---
Made with ❤️ by YAFATEK Solutions

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

# Optional features
pip install grami-ai[gemini]    # For Google Gemini support
pip install grami-ai[ollama]    # For Ollama support
pip install grami-ai[dev]       # For development tools
```

2. Create your first agent:
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
    
    # Execute a task
    result = await agent.execute_task({
        "objective": "Calculate and explain",
        "input": "What is 25 * 48?"
    })
    
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
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

## 🔐 API Configuration

### Environment Variables

To use GRAMI AI with external services, you'll need to set up environment variables:

1. Copy `.env.example` to `.env`
2. Fill in your API credentials

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

#### Required Environment Variables
- `GOOGLE_SEARCH_API_KEY`: Google Custom Search API Key
- `GOOGLE_GEMINI_API_KEY`: Google Gemini API Key
- `GOOGLE_SEARCH_ENGINE_ID`: Google Custom Search Engine ID

#### Security Best Practices
- Never commit `.env` to version control
- Use a `.gitignore` file to exclude sensitive files
- Rotate API keys regularly
- Use environment-specific configurations

### API Key Management

```python
# Secure API key retrieval
api_key = os.environ.get('YOUR_API_KEY')
if not api_key:
    raise ValueError("API key not found. Set the environment variable.")
```

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

- YAFATEK Solutions - The company behind GRAMI AI
- The amazing open-source community
- All our contributors and users

## Vision

Grami AI is designed to revolutionize how developers build AI agents by providing a modern, async-first framework that emphasizes:

- **Asynchronous by Default**: Built from the ground up for high-performance, non-blocking operations
- **Modular Architecture**: Plug-and-play components for tools, memory, and LLM providers
- **Type Safety**: Comprehensive type hints and protocol-based interfaces
- **Production Ready**: Built for reliability and scalability in real-world applications

## 🚀 Advanced Example: Digital Marketing Agency AI

### 🌐 Multi-Agent Digital Marketing System

GRAMI introduces a cutting-edge Digital Marketing Agency AI that demonstrates:
- Real-time client interaction
- Distributed task management
- AI-powered strategy generation
- Kafka-based inter-agent communication
- Redis-backed global state management

#### Key Components
- **Growth Manager**: Client interaction and task delegation
- **Market Researcher**: Trend and market analysis
- **Content Creator**: Strategic content generation
- **Social Media Manager**: Platform-specific content planning

#### Example Usage

```python
from examples.digital_marketing_agency import DigitalMarketingAgency

async def main():
    agency = DigitalMarketingAgency()
    await agency.start_agency_interaction()
```

#### Features
- Asynchronous agent communication
- Intelligent task distribution
- Gemini-powered natural language processing
- Scalable microservice architecture

### 🔧 Prerequisites
- Redis server running
- Kafka broker configured
- Google Gemini API key

### 📦 Dependencies
```bash
pip install grami-ai[kafka,redis]
```

### 🛡️ Security & Privacy
- Environment-based configuration
- Secure API key management
- Minimal data persistence

## 🚀 Advanced Use Cases

### 🎨 Instagram Content Creation Agent

GRAMI introduces a cutting-edge Instagram Content Creation Agent that leverages multi-stage web search and AI-driven content generation:

```python
from grami_ai.examples import InstagramContentAgent

# Create content for sustainable fashion
content_brief = {
    'topic': 'Sustainable Fashion',
    'target_audience': 'Millennials & Gen Z',
    'tone': 'Inspirational and Authentic'
}

agent = InstagramContentAgent()
content = await agent.create_instagram_content(content_brief)
```

**Key Features:**
- Multi-stage web search for trend insights
- AI-powered content generation
- Platform-specific content variations
- Comprehensive hashtag ecosystem
- Interactive content strategies

## 🛠 Supported Platforms
- Instagram
- TikTok (Coming Soon)
- YouTube Shorts (Coming Soon)

## 📊 Analytics & Insights
- Trend tracking
- Engagement prediction
- Content performance analysis

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
