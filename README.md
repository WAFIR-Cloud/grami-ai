# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.132-blue.svg" alt="Version">
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
- [Communication Interfaces](#-communication-interfaces)
- [AsyncAgent Configuration](#-asyncagent-configuration)
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
pip install grami-ai==0.3.132
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

## 🌐 Communication Interfaces

GRAMI-AI supports multiple communication interfaces, including WebSocket for real-time, bidirectional communication between agents.

### WebSocket Communication

Create a WebSocket-enabled agent using the built-in `setup_communication()` method:

```python
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Create an agent with WebSocket communication
agent = AsyncAgent(
    name="ToolsAgent", 
    llm=GeminiProvider(api_key=os.getenv('GEMINI_API_KEY')),
    memory=LRUMemory(capacity=100),
    tools=[calculate_area, generate_fibonacci]
)

# Setup WebSocket communication
communication_interface = await agent.setup_communication(
    host='localhost', 
    port=0  # Dynamic port selection
)
```

#### Key Features of WebSocket Communication
- Real-time bidirectional messaging
- Dynamic port allocation
- Seamless tool and LLM interaction
- Secure communication channel

#### Example Use Cases
- Distributed AI systems
- Real-time collaborative agents
- Interactive tool-based services
- Event-driven agent communication

## 🤖 AsyncAgent Configuration

The `AsyncAgent` class is the core component of GRAMI-AI, providing a flexible and powerful way to create AI agents. Here's a detailed breakdown of its parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | str | Yes | - | Unique identifier for the agent instance |
| `llm` | BaseLLMProvider | Yes | - | Language model provider (e.g., GeminiProvider, OpenAIProvider) |
| `memory` | BaseMemoryProvider | No | None | Memory provider for conversation history management |
| `system_instructions` | str | No | None | System-level instructions to guide the model's behavior |
| `tools` | List[Callable] | No | None | List of functions the agent can use during interactions |
| `communication_interface` | Any | No | None | Interface for agent communication (e.g., WebSocket) |

### Example Usage with Parameters

```python
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Create an agent with all parameters
agent = AsyncAgent(
    name="AssistantAI",
    llm=GeminiProvider(api_key="YOUR_API_KEY"),
    memory=LRUMemory(capacity=100),
    system_instructions="You are a helpful AI assistant focused on technical tasks.",
    tools=[calculate_area, generate_fibonacci],
    communication_interface=None  # Will be set up later if needed
)
```

## 🗺 Development Roadmap

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
- [x] WebSocket real-time communication
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

## 🤝 Contributing

We welcome contributions to GRAMI-AI! Here's how you can help:

### Ways to Contribute

1. **Bug Reports**: Open detailed issues on GitHub
2. **Feature Requests**: Share your ideas for new features
3. **Code Contributions**: Submit pull requests with improvements
4. **Documentation**: Help improve our docs and examples
5. **Testing**: Add test cases and improve coverage

### Development Setup

1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```

### Pull Request Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.