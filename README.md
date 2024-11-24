# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.133-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Provider Examples](#-provider-examples)
- [Memory Management](#-memory-management)
- [Streaming Capabilities](#-streaming-capabilities)
- [Development Roadmap](#-development-roadmap)
- [TODO List](#-todo-list)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

GRAMI-AI is a cutting-edge, async-first AI agent framework designed for building sophisticated AI applications. With support for multiple LLM providers, advanced memory management, and streaming capabilities, GRAMI-AI enables developers to create powerful, context-aware AI systems.

### Why GRAMI-AI?

- **Async-First**: Built for high-performance asynchronous operations
- **Provider Agnostic**: Support for Gemini, OpenAI, Anthropic, and Ollama
- **Advanced Memory**: LRU and Redis-based memory management
- **Streaming Support**: Efficient token-by-token streaming responses
- **Enterprise Ready**: Production-grade security and scalability

## 🚀 Key Features

### LLM Providers
- Gemini (Google's latest LLM)
- OpenAI (GPT models)
- Anthropic (Claude)
- Ollama (Local models)

### Memory Management
- LRU Memory (In-memory caching)
- Redis Memory (Distributed caching)
- Custom memory providers

### Communication
- Synchronous messaging
- Asynchronous streaming
- WebSocket support
- Custom interfaces

## 💻 Installation

```bash
pip install grami-ai==0.3.133
```

## 🎬 Quick Start

### Basic Usage

```python
import asyncio
from grami.agents import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

async def main():
    # Initialize provider
    provider = GeminiProvider(api_key="YOUR_API_KEY")
    
    # Create agent
    agent = AsyncAgent(
        name="AssistantAI",
        llm=provider,
        system_instructions="You are a helpful digital assistant."
    )

    # Send a message
    response = await agent.send_message("Hello!")
    print(response)

asyncio.run(main())
```

## 📚 Provider Examples

### Gemini Provider

```python
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Initialize with memory
provider = GeminiProvider(
    api_key="YOUR_API_KEY",
    model="gemini-pro",  # Optional, defaults to gemini-pro
    generation_config={   # Optional
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40
    }
)

# Add memory provider
memory = LRUMemory(capacity=100)
provider.set_memory_provider(memory)

# Regular message
response = await provider.send_message("What is AI?")

# Streaming response
async for chunk in provider.stream_message("Tell me a story"):
    print(chunk, end="", flush=True)
```

## 🧠 Memory Management

### LRU Memory

```python
from grami.memory.lru import LRUMemory

# Initialize with capacity
memory = LRUMemory(capacity=100)

# Add to agent
agent = AsyncAgent(
    name="MemoryAgent",
    llm=provider,
    memory=memory
)
```

### Redis Memory

```python
from grami.memory.redis import RedisMemory

# Initialize Redis memory
memory = RedisMemory(
    host="localhost",
    port=6379,
    capacity=1000
)

# Add to provider
provider.set_memory_provider(memory)
```

## 🌊 Streaming Capabilities

### Basic Streaming

```python
async def stream_example():
    async for chunk in provider.stream_message("Generate a story"):
        print(chunk, end="", flush=True)
```

### Streaming with Memory

```python
async def stream_with_memory():
    # First message
    response = await provider.send_message("My name is Alice")
    
    # Stream follow-up (will remember context)
    async for chunk in provider.stream_message("What's my name?"):
        print(chunk, end="", flush=True)
```

## 🛠️ Development Roadmap

- [x] Multi-provider support
- [x] Memory management
- [x] Streaming capabilities
- [ ] Advanced tool integration
- [ ] Enhanced security features
- [ ] Performance optimizations

## 📝 TODO List

- [ ] Add support for more LLM providers (Claude, Llama, etc.)
- [ ] Implement advanced caching strategies
- [ ] Add WebSocket support for real-time communication
- [ ] Create comprehensive test suite
- [ ] Add support for function calling
- [ ] Implement conversation branching
- [ ] Add support for multi-modal inputs
- [ ] Enhance error handling and logging
- [ ] Add rate limiting and quota management
- [ ] Create detailed API documentation
- [ ] Add support for custom prompt templates
- [ ] Implement conversation summarization

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

GRAMI-AI is released under the MIT License. See the [LICENSE](LICENSE) file for details.