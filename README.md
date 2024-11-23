# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.121-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## Overview

GRAMI-AI is a cutting-edge, async-first AI agent framework designed to solve complex computational challenges through intelligent, collaborative agent interactions. Built with unprecedented flexibility, this library empowers developers to create sophisticated, context-aware AI systems that can adapt, learn, and collaborate across diverse domains.

## Key Features

- Async AI Agent Creation
- Multi-LLM Support (Gemini, OpenAI, Anthropic, Ollama)
- Extensible Tool Ecosystem
- Multiple Communication Interfaces
- Flexible Memory Management
- Secure and Scalable Architecture

## Installation

### Using pip

```bash
pip install grami-ai
```

### From Source

```bash
git clone https://github.com/YAFATEK/grami-ai.git
cd grami-ai
pip install -e .
```

## Quick Start

### Basic Async Agent Creation

```python
import asyncio
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

async def main():
    # Initialize a Gemini-powered Async Agent
    agent = AsyncAgent(
        name="AssistantAI",
        llm=GeminiProvider(api_key="YOUR_API_KEY"),
        system_instructions="You are a helpful digital assistant."
    )

    # Send an async message
    response = await agent.send_message("Hello, how can you help me today?")
    print(response)

    # Stream a response
    async for token in agent.stream_message("Tell me a story"):
        print(token, end='', flush=True)

asyncio.run(main())
```

## Example Configurations

### 1. Async Agent with Memory and Streaming
```python
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

agent = AsyncAgent(
    name="MemoryStreamingAgent",
    llm=provider,
    memory=LRUMemory(capacity=100),
    system_instructions="You are a storyteller."
)
```

### 2. Async Agent without Memory
```python
agent = AsyncAgent(
    name="NoMemoryAgent",
    llm=provider,
    memory=None,
    system_instructions="You are a concise assistant."
)
```

### 3. Async Agent with Streaming Disabled
```python
response = await agent.send_message("Tell me about AI")
```

### 4. Async Agent with Streaming Enabled
```python
async for token in agent.stream_message("Explain quantum computing"):
    print(token, end='', flush=True)
```

## Roadmap and TODO

### Core Framework
- [x] Async-first design
- [x] Multi-provider support
- [x] Dynamic agent creation
- [x] Flexible memory management

### Memory and State Management
- [x] Pluggable memory providers
  - [x] In-memory state storage
  - [x] LRU Memory implementation
- [x] Async memory operations
- [ ] Persistent memory storage
- [ ] Advanced memory indexing

### Provider Integrations
- [x] Gemini Provider
- [ ] OpenAI Provider
- [ ] Anthropic Provider
- [ ] Ollama Provider

### Security and Performance
- [ ] Enhanced encryption for API keys
- [ ] Rate limiting mechanisms
- [ ] Secure communication protocols
- [ ] Performance optimization for large-scale deployments

## Contributing

Contributions are welcome! Please check our [GitHub repository](https://github.com/YAFATEK/grami-ai) for guidelines.

## Support

- **Email**: support@yafatek.dev
- **GitHub**: [GRAMI-AI Issues](https://github.com/YAFATEK/grami-ai/issues)

---

 2024 YAFATEK. All Rights Reserved.