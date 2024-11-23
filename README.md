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

## Development Checklist

### Core Framework Design
- [x] Implement `AsyncAgent` base class with dynamic configuration
- [x] Create flexible system instruction definition mechanism
- [x] Design abstract LLM provider interface
- [x] Develop dynamic role and persona assignment system
- [x] Comprehensive async example configurations
  - [x] Memory with streaming
  - [x] Memory without streaming
  - [x] No memory with streaming
  - [x] No memory without streaming
- [ ] Implement multi-modal agent capabilities (text, image, video)

### LLM Provider Abstraction
- [x] Unified interface for diverse LLM providers
  - [x] Google Gemini integration (start_chat(), send_message())
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
- [x] Dynamic prompt engineering support
- [x] Provider-specific configuration handling

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
  - [ ] Redis distributed memory
  - [ ] DynamoDB scalable storage
  - [ ] S3 content storage
- [x] Conversation and task history tracking
- [ ] Global state management for agent crews
- [ ] Persistent task and interaction logs
- [ ] Advanced memory indexing
- [ ] Memory compression techniques

### Tool and Function Ecosystem
- [x] Extensible tool integration framework
- [x] Default utility tools
  - [ ] Kafka message publisher
  - [ ] Web search utility
  - [ ] Content analysis tool
- [ ] Provider-specific function calling support
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
- [x] Example use case implementations
- [ ] Contribution guidelines
- [ ] Community tool submission process
- [ ] Regular maintenance and updates

### Future Roadmap
- [ ] Payment integration solutions
- [ ] Advanced agent collaboration patterns
- [ ] Specialized industry-specific agents
- [ ] Enhanced security features
- [ ] Extended provider support

## Contributing

Contributions are welcome! Please check our [GitHub repository](https://github.com/YAFATEK/grami-ai) for guidelines.

## Support

- **Email**: support@yafatek.dev
- **GitHub**: [GRAMI-AI Issues](https://github.com/YAFATEK/grami-ai/issues)

---

 2024 YAFATEK. All Rights Reserved.