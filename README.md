# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.130-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Example Configurations](#-example-configurations)
- [Memory Providers](#-memory-providers)
- [Working with Tools](#-working-with-tools)
- [Development Roadmap](#-development-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

GRAMI-AI is a cutting-edge, async-first AI agent framework designed to solve complex computational challenges through intelligent, collaborative agent interactions. Built with unprecedented flexibility, this library empowers developers to create sophisticated, context-aware AI systems that can adapt, learn, and collaborate across diverse domains.

## 🚀 Key Features

- Async AI Agent Creation
- Multi-LLM Support (Gemini, OpenAI, Anthropic, Ollama)
- Extensible Tool Ecosystem
- Multiple Communication Interfaces
- Flexible Memory Management
- Secure and Scalable Architecture

## 💻 Installation

### Using pip

```bash
pip install grami-ai==0.3.130
```

### From Source

```bash
git clone https://github.com/YAFATEK/grami-ai.git
cd grami-ai
pip install -e .
```

## 🎬 Quick Start

```python
import asyncio
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider

async def main():
    agent = AsyncAgent(
        name="AssistantAI",
        llm=GeminiProvider(api_key="YOUR_API_KEY"),
        system_instructions="You are a helpful digital assistant."
    )

    response = await agent.send_message("Hello, how can you help me today?")
    print(response)

asyncio.run(main())
```

## 🔧 Example Configurations

### 1. Async Agent with Memory
```python
from grami.memory.lru import LRUMemory

agent = AsyncAgent(
    name="MemoryAgent",
    llm=provider,
    memory=LRUMemory(capacity=100)
)
```

### 2. Async Agent with Streaming
```python
async for token in agent.stream_message("Tell me a story"):
    print(token, end='', flush=True)
```

## 💾 Memory Providers

GRAMI-AI supports multiple memory providers:

1. **LRU Memory**: Local in-memory cache
2. **Redis Memory**: Distributed memory storage

### LRU Memory Example
```python
from grami.memory import LRUMemory

memory = LRUMemory(capacity=50)
```

### Redis Memory Example
```python
from grami.memory import RedisMemory

memory = RedisMemory(
    host='localhost',
    port=6379,
    capacity=100
)
```

## 🛠 Working with Tools

### Creating Tools

Tools are simple Python functions used by AI agents:

```python
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_age(birth_year: int) -> int:
    current_year = datetime.now().year
    return current_year - birth_year
```

### Adding Tools to AsyncAgent

```python
agent = AsyncAgent(
    name="ToolsAgent",
    llm=gemini_provider,
    tools=[get_current_time, calculate_age]
)
```

## 🗺 Development Roadmap

- [ ] Enhanced Multi-Agent Collaboration
- [ ] Advanced Workflow Delegation
- [ ] Improved Context Management
- [ ] Expanded LLM Provider Support

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct.

## 📄 License

This project is licensed under the MIT License.