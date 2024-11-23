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

- Dynamic AI Agent Creation (Sync and Async)
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

### Basic Agent Creation

```python
from grami.agent import Agent
from grami.providers import GeminiProvider

# Initialize a Gemini-powered Agent
agent = Agent(
    name="AssistantAI",
    role="Helpful Digital Assistant",
    llm_provider=GeminiProvider(api_key="YOUR_API_KEY"),
    tools=[WebSearchTool(), CalculatorTool()]
)

# Send a message
response = await agent.send_message("Help me plan a trip to Paris")
print(response)
```

### Async Agent Creation

```python
from grami.agent import AsyncAgent
from grami.providers import GeminiProvider

# Initialize a Gemini-powered AsyncAgent
async_agent = AsyncAgent(
    name="ScienceExplainerAI",
    role="Scientific Concept Explainer",
    llm_provider=GeminiProvider(api_key="YOUR_API_KEY"),
    initial_context=[
        {
            "role": "system", 
            "content": "You are an expert at explaining complex scientific concepts clearly."
        }
    ]
)

# Send a message
response = await async_agent.send_message("Explain quantum entanglement")
print(response)

# Stream a response
async for token in async_agent.stream_message("Explain photosynthesis"):
    print(token, end='', flush=True)
```

## Examples

We provide a variety of example implementations to help you get started:

### Basic Agents
- `examples/simple_agent_example.py`: Basic mathematical calculation agent
- `examples/simple_async_agent.py`: Async scientific explanation agent
- `examples/gemini_example.py`: Multi-tool Gemini Agent with various capabilities

### Advanced Scenarios
- `examples/content_creation_agent.py`: AI-Powered Content Creation Agent
  - Generates blog posts
  - Conducts topic research
  - Creates supporting visuals
  - Tailors content to specific audiences

- `examples/web_research_agent.py`: Advanced Web Research and Trend Analysis Agent
  - Performs comprehensive market research
  - Conducts web searches
  - Analyzes sentiment
  - Predicts industry trends
  - Generates detailed reports

### Collaborative Agents
- `examples/agent_crew_example.py`: Multi-Agent Collaboration
  - Demonstrates inter-agent communication
  - Showcases specialized agent roles
  - Enables complex task delegation

### Tool Integration
- `examples/tools.py`: Collection of custom tools
  - Web Search
  - Weather Information
  - Calculator
  - Sentiment Analysis
  - Image Generation

## Environment Variables

### API Key Management

GRAMI-AI uses environment variables to manage sensitive credentials securely. To set up your API keys:

1. Create a `.env` file in the project root directory
2. Add your API keys in the following format:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

**Important**: Never commit your `.env` file to version control. The `.gitignore` is already configured to prevent this.

## Development Checklist

### Core Framework Design
- [x] Implement `AsyncAgent` base class with dynamic configuration
- [x] Create flexible system instruction definition mechanism
- [x] Design abstract LLM provider interface
- [x] Develop dynamic role and persona assignment system
- [ ] Implement multi-modal agent capabilities (text, image, video)

### LLM Provider Abstraction
- [x] Unified interface for diverse LLM providers
  - [x] Google Gemini integration (start_chat(), send_message())
  - [ ] OpenAI ChatGPT integration
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

## Memory Management

GRAMI-AI provides flexible memory management for AI agents, allowing you to store and retrieve conversation context, user information, and agent state.

```python
from grami.agent import AsyncAgent
from grami.providers import GeminiProvider
from grami.memory import LRUMemory

# Initialize memory with a capacity of 1000 items
memory = LRUMemory(capacity=1000)

# Create an agent with memory
agent = AsyncAgent(
    name="MemoryBot",
    role="AI Assistant with memory capabilities",
    llm_provider=GeminiProvider(api_key="YOUR_API_KEY"),
    memory_provider=memory
)

# Conversation with memory tracking
response = await agent.send_message("Hi, I'm Alice and I love chess!")

# Retrieve memory contents
keys = await memory.list_keys()
for key in keys:
    value = await memory.retrieve(key)
    print(f"Memory Entry: {key} - {value}")
```

#### Memory Providers

- `LRUMemory`: Least Recently Used memory with configurable capacity
- Easy to extend with custom memory providers
- Supports storing and retrieving conversation context
- Automatic management of memory capacity

## Documentation

For detailed documentation, visit our [Documentation Website](https://grami-ai.readthedocs.io)

## Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md)

## License

MIT License - Empowering open-source innovation

## About YAFATEK Solutions

Pioneering AI innovation through flexible, powerful frameworks.

## Contact & Support

- **Email**: support@yafatek.dev
- **GitHub**: [GRAMI-AI Issues](https://github.com/YAFATEK/grami-ai/issues)

---

**Star ⭐ the project if you believe in collaborative AI innovation!**