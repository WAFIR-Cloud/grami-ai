# GRAMI-AI: Growth and Relationship AI Management Infrastructure

## 🚀 Overview

GRAMI-AI is an advanced, async-first AI agent framework designed to revolutionize collaborative marketing solutions. Built with flexibility, modularity, and scalability in mind, this library empowers developers to create intelligent, context-aware AI agents.

## 🌟 Key Features

### 1. Async-First Architecture
- High-performance, non-blocking agent interactions
- Designed for scalable, concurrent AI operations

### 2. Modular Design
- Easily extensible components for:
  - Language Models (LLMs)
  - Memory Providers
  - Tools and Interfaces
  - Event Streaming

### 3. Multi-Provider Support
- LLM Providers:
  - Google Gemini
  - OpenAI
  - Anthropic
  - Ollama

### 4. Flexible Memory Management
- In-Memory Storage
- Redis Backend
- Customizable Memory Providers

### 5. Advanced Tooling
- Content Generation
- Web Search
- Social Media Analytics
- API Interactions

## 📦 Installation

```bash
pip install grami-ai
```

## 🚀 Quick Start

### Basic Agent Creation

```python
from grami_ai.core.agent import AsyncAgent
from grami_ai.llms.gemini_llm import GeminiLLMProvider

# Create an AI agent for marketing
async def main():
    agent = await AsyncAgent.create(
        name="MarketingAssistant",
        llm="gemini",
        tools=["content_generation", "web_search"]
    )

    # Generate marketing content
    response = await agent.process({
        "type": "content_request",
        "platform": "instagram",
        "niche": "tech",
        "content_type": "post"
    })
    print(response)

# Run the agent
asyncio.run(main())
```

## 🛠 Core Components

### Agent
- Orchestrates LLM, memory, tools, and interfaces
- Async message processing
- Dynamic tool selection

### Tools
- Extensible async tool base class
- Metadata-driven tool configuration
- Support for various tool categories

### Memory
- Async memory providers
- In-memory and Redis backends
- Conversation and state management

### Logging
- Async logging with structured output
- Configurable log levels
- Context-aware logging

## 🔧 Configuration

GRAMI-AI supports environment-based configuration:
- Development
- Testing
- Production

```python
from grami_ai.core.config import get_settings

# Get environment-specific settings
settings = get_settings()
```

## 📡 Interfaces

- WebSocket
- Kafka Consumer
- Custom Interface Support

## 🔒 Security

- Environment variable management
- Configurable token expiration
- Resource limits

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

MIT License, Copyright (c) 2024 WAFIR-Cloud

## 📞 Contact

For support, collaboration, or inquiries:
- Email: contact@wafir-cloud.com
- GitHub: [WAFIR-Cloud/grami-ai](https://github.com/WAFIR-Cloud/grami-ai)

## Repository Information

**Repository:** [WAFIR-Cloud/grami-ai](https://github.com/WAFIR-Cloud/grami-ai)
**Issues:** [GitHub Issues](https://github.com/WAFIR-Cloud/grami-ai/issues)
**Documentation:** [README](https://github.com/WAFIR-Cloud/grami-ai/blob/main/README.md)

## Python Compatibility

- **Supported Python Versions:** 3.10 - 3.12
- **Recommended Python Version:** 3.11

## 🌐 Roadmap

- [ ] Enhanced LLM Provider Support
- [ ] Advanced Tool Ecosystem
- [ ] Comprehensive Documentation
- [ ] Performance Benchmarking
- [ ] Community Extensions

## 🏆 Acknowledgements

Built with ❤️ by WAFIR-Cloud, pushing the boundaries of AI-powered solutions.