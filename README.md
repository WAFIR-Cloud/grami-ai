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

## 🗺 Development Roadmap

### Core Framework Design
- [ ] Implement AsyncAgent base class with dynamic configuration
- [ ] Create flexible system instruction definition mechanism
- [ ] Design abstract LLM provider interface
- [ ] Develop dynamic role and persona assignment system
- [ ] Comprehensive async example configurations
  - [ ] Memory with streaming
  - [ ] Memory without streaming
  - [ ] No memory with streaming
  - [ ] No memory without streaming
- [ ] Implement multi-modal agent capabilities (text, image, video)

### LLM Provider Abstraction
- [ ] Unified interface for diverse LLM providers
- [ ] Google Gemini integration
  - [x] Basic message sending
  - [x] Streaming support
  - [x] Memory integration
- [ ] OpenAI ChatGPT integration
  - [ ] Basic message sending
  - [ ] Streaming implementation
  - [ ] Memory support
- [ ] Anthropic Claude integration
- [ ] Ollama local LLM support
- [ ] Standardize function/tool calling across providers
- [ ] Dynamic prompt engineering support
- [ ] Provider-specific configuration handling

### Communication Interfaces
- [ ] WebSocket real-time communication
- [ ] REST API endpoint design
- [ ] Kafka inter-agent communication
- [ ] gRPC support
- [ ] Event-driven agent notification system
- [ ] Secure communication protocols

### Memory and State Management
- [x] Pluggable memory providers
- [x] In-memory state storage
- [x] Redis distributed memory
- [ ] DynamoDB scalable storage
- [ ] S3 content storage
- [ ] Conversation and task history tracking
- [ ] Global state management for agent crews
- [ ] Persistent task and interaction logs
- [ ] Advanced memory indexing
- [ ] Memory compression techniques

### Tool and Function Ecosystem
- [ ] Extensible tool integration framework
- [ ] Default utility tools
  - [ ] Kafka message publisher
  - [ ] Web search utility
  - [ ] Content analysis tool
- [ ] Provider-specific function calling support
- [ ] Community tool marketplace
- [ ] Easy custom tool development

### Agent Crew Collaboration
- [ ] Inter-agent communication protocol
- [ ] Workflow and task delegation mechanisms
- [ ] Approval and review workflows
- [ ] Notification and escalation systems
- [ ] Dynamic team composition
- [ ] Shared context and memory management

### Use Case Implementations
- [ ] Digital Agency workflow template
  - [ ] Growth Manager agent
  - [ ] Content Creator agent
  - [ ] Trend Researcher agent
  - [ ] Media Creation agent
- [ ] Customer interaction management
- [ ] Approval and revision cycles

### Security and Compliance
- [ ] Secure credential management
- [ ] Role-based access control
- [ ] Audit logging
- [ ] Compliance with data protection regulations

### Performance and Scalability
- [x] Async-first design
- [ ] Horizontal scaling support
- [ ] Performance benchmarking
- [ ] Resource optimization

### Testing and Quality
- [ ] Comprehensive unit testing
- [ ] Integration testing for agent interactions
- [ ] Mocking frameworks for LLM providers
- [ ] Continuous integration setup

### Documentation and Community
- [x] Detailed API documentation
- [x] Comprehensive developer guides
- [ ] Example use case implementations
- [x] Contribution guidelines
- [ ] Community tool submission process
- [ ] Regular maintenance and updates

### Future Roadmap
- [ ] Payment integration solutions
- [ ] Advanced agent collaboration patterns
- [ ] Specialized industry-specific agents
- [ ] Enhanced security features
- [ ] Extended provider support

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
- [ ] Add support for multiple languages
- [ ] Implement fine-tuning capabilities
- [ ] Add support for model quantization
- [ ] Create a web-based demo
- [ ] Add support for batch processing
- [ ] Implement conversation history export/import
- [ ] Add support for custom model hosting
- [ ] Create visualization tools for conversation flows
- [ ] Implement automated testing pipeline
- [ ] Add support for conversation analytics
- [ ] Create deployment guides for various platforms
- [ ] Implement automated documentation generation
- [ ] Add support for model performance monitoring
- [ ] Create benchmarking tools
- [ ] Implement A/B testing capabilities
- [ ] Add support for custom tokenizers
- [ ] Create model evaluation tools
- [ ] Implement conversation templates
- [ ] Add support for conversation routing
- [ ] Create debugging tools
- [ ] Implement conversation validation
- [ ] Add support for custom memory backends
- [ ] Create conversation backup/restore features
- [ ] Implement conversation filtering
- [ ] Add support for conversation tagging
- [ ] Create conversation search capabilities
- [ ] Implement conversation versioning
- [ ] Add support for conversation merging
- [ ] Create conversation export formats
- [ ] Implement conversation import validation
- [ ] Add support for conversation scheduling
- [ ] Create conversation monitoring tools
- [ ] Implement conversation archiving
- [ ] Add support for conversation encryption
- [ ] Create conversation access control
- [ ] Implement conversation rate limiting
- [ ] Add support for conversation quotas
- [ ] Create conversation usage analytics
- [ ] Implement conversation cost tracking
- [ ] Add support for conversation billing
- [ ] Create conversation audit logs
- [ ] Implement conversation compliance checks
- [ ] Add support for conversation retention policies
- [ ] Create conversation backup strategies
- [ ] Implement conversation recovery procedures
- [ ] Add support for conversation migration
- [ ] Create conversation optimization tools
- [ ] Implement conversation caching strategies
- [ ] Add support for conversation compression
- [ ] Create conversation performance metrics
- [ ] Implement conversation health checks
- [ ] Add support for conversation monitoring
- [ ] Create conversation alerting system
- [ ] Implement conversation debugging tools
- [ ] Add support for conversation profiling
- [ ] Create conversation testing framework
- [ ] Implement conversation documentation
- [ ] Add support for conversation examples
- [ ] Create conversation tutorials
- [ ] Implement conversation guides
- [ ] Add support for conversation best practices
- [ ] Create conversation security guidelines

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

GRAMI-AI is released under the MIT License. See the [LICENSE](LICENSE) file for details.