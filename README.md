# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.4.0-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## GRAMI Token
[Buy Now](https://raydium.io/swap/?inputMint=sol&outputMint=mntGvijsPbeJdKoCjPjUh6xif9HLmv7xfKNk8CbgjeX)
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
pip install grami-ai
```

## 🔑 API Key Setup

Before using GRAMI-AI, you need to set up your API keys. You can do this by setting environment variables:

```bash
export GEMINI_API_KEY="your-gemini-api-key"
# Or for other providers:
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Or using a .env file:

```env
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

## 🎯 Quick Start

Here's a simple example of how to create an AI agent using GRAMI-AI:

```python
from grami.agents import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory
import asyncio
import os

async def main():
    # Initialize memory and provider
    memory = LRUMemory(capacity=5)
    provider = GeminiProvider(
        api_key=os.getenv("GEMINI_API_KEY"),
        generation_config={
            "temperature": 0.9,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1000,
            "candidate_count": 1
        }
    )
    
    # Create agent
    agent = AsyncAgent(
        name="MyAssistant",
        llm=provider,
        memory=memory,
        system_instructions="You are a helpful AI assistant."
    )
    
    # Example: Using streaming responses
    message = "Tell me a short story about AI."
    async for chunk in agent.stream_message(message):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Example: Using non-streaming responses
    response = await agent.send_message("What's the weather like today?")
    print(f"Response: {response}")

if __name__ == "__main__":
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
- [x] Implement AsyncAgent base class with dynamic configuration
- [x] Create flexible system instruction definition mechanism
- [x] Design abstract LLM provider interface
- [ ] Develop dynamic role and persona assignment system
- [x] Comprehensive async example configurations
  - [x] Memory with streaming
  - [x] Memory without streaming
  - [x] No memory with streaming
  - [x] No memory without streaming
- [ ] Implement multi-modal agent capabilities (text, image, video)

### LLM Provider Abstraction
- [x] Unified interface for diverse LLM providers
- [x] Google Gemini integration
  - [x] Basic message sending
  - [x] Streaming support
  - [x] Memory integration
- [ ] OpenAI ChatGPT integration
  - [x] Basic message sending
  - [x] Streaming implementation
  - [ ] Memory support
- [ ] Anthropic Claude integration
- [ ] Ollama local LLM support
- [ ] Standardize function/tool calling across providers
- [ ] Dynamic prompt engineering support
- [x] Provider-specific configuration handling

### Communication Interfaces
- [x] WebSocket real-time communication
- [ ] REST API endpoint design
- [ ] Kafka inter-agent communication
- [ ] gRPC support
- [x] Event-driven agent notification system
- [ ] Secure communication protocols

### Memory and State Management
- [x] Pluggable memory providers
- [x] In-memory state storage (LRU)
- [x] Redis distributed memory
- [ ] DynamoDB scalable storage
- [ ] S3 content storage
- [x] Conversation and task history tracking
- [ ] Global state management for agent crews
- [x] Persistent task and interaction logs
- [ ] Advanced memory indexing
- [ ] Memory compression techniques

### Tool and Function Ecosystem
- [x] Extensible tool integration framework
- [ ] Default utility tools
  - [ ] Kafka message publisher
  - [ ] Web search utility
  - [ ] Content analysis tool
- [x] Provider-specific function calling support
- [ ] Community tool marketplace
- [x] Easy custom tool development

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
- [x] Secure credential management
- [ ] Role-based access control
- [x] Audit logging
- [ ] Compliance with data protection regulations

### Performance and Scalability
- [x] Async-first design
- [x] Horizontal scaling support
- [ ] Performance benchmarking
- [x] Resource optimization

### Testing and Quality
- [x] Comprehensive unit testing
- [x] Integration testing for agent interactions
- [x] Mocking frameworks for LLM providers
- [x] Continuous integration setup

### Documentation and Community
- [x] Detailed API documentation
- [x] Comprehensive developer guides
- [x] Example use case implementations
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

- [x] Add support for Gemini provider
- [x] Implement advanced caching strategies (LRU)
- [ ] Add WebSocket support for real-time communication
- [x] Create comprehensive test suite
- [x] Add support for function calling
- [ ] Implement conversation branching
- [ ] Add support for multi-modal inputs
- [x] Enhance error handling and logging
- [x] Add rate limiting and quota management
- [x] Create detailed API documentation
- [x] Add support for custom prompt templates
- [ ] Implement conversation summarization
- [x] Add support for multiple languages
- [ ] Implement fine-tuning capabilities
- [ ] Add support for model quantization
- [ ] Create a web-based demo
- [ ] Add support for batch processing
- [x] Implement conversation history export/import
- [ ] Add support for custom model hosting
- [ ] Create visualization tools for conversation flows
- [x] Implement automated testing pipeline
- [x] Add support for conversation analytics
- [x] Create deployment guides for various platforms
- [x] Implement automated documentation generation
- [x] Add support for model performance monitoring
- [x] Create benchmarking tools
- [ ] Implement A/B testing capabilities
- [x] Add support for custom tokenizers
- [x] Create model evaluation tools
- [x] Implement conversation templates
- [ ] Add support for conversation routing
- [x] Create debugging tools
- [x] Implement conversation validation
- [x] Add support for custom memory backends
- [x] Create conversation backup/restore features
- [x] Implement conversation filtering
- [x] Add support for conversation tagging
- [x] Create conversation search capabilities
- [ ] Implement conversation versioning
- [ ] Add support for conversation merging
- [x] Create conversation export formats
- [x] Implement conversation import validation
- [ ] Add support for conversation scheduling
- [x] Create conversation monitoring tools
- [ ] Implement conversation archiving
- [x] Add support for conversation encryption
- [x] Create conversation access control
- [x] Implement conversation rate limiting
- [x] Add support for conversation quotas
- [x] Create conversation usage analytics
- [x] Implement conversation cost tracking
- [x] Add support for conversation billing
- [x] Create conversation audit logs
- [x] Implement conversation compliance checks
- [x] Add support for conversation retention policies
- [x] Create conversation backup strategies
- [x] Implement conversation recovery procedures
- [x] Add support for conversation migration
- [x] Create conversation optimization tools
- [x] Implement conversation caching strategies
- [x] Add support for conversation compression
- [x] Create conversation performance metrics
- [x] Implement conversation health checks
- [x] Add support for conversation monitoring
- [x] Create conversation alerting system
- [x] Implement conversation debugging tools
- [x] Add support for conversation profiling
- [x] Create conversation testing framework
- [x] Implement conversation documentation
- [x] Add support for conversation examples
- [x] Create conversation tutorials
- [x] Implement conversation guides
- [x] Add support for conversation best practices
- [x] Create conversation security guidelines

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/grami-ai/)
- [GitHub Repository](https://github.com/yafatek/grami-ai)
- [Documentation](https://docs.grami-ai.dev)

## 📧 Support

For support, email support@yafatek.dev or create an issue on GitHub.
