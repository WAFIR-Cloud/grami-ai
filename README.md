# GRAMI-AI: Dynamic AI Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.117-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## Overview

GRAMI-AI is a cutting-edge, async-first AI agent framework designed to solve complex computational challenges through intelligent, collaborative agent interactions. Built with unprecedented flexibility, this library empowers developers to create sophisticated, context-aware AI systems that can adapt, learn, and collaborate across diverse domains.

## Key Features

- Dynamic AI Agent Creation
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

## Examples

We provide a variety of example implementations to help you get started:

### Basic Agents
- `examples/simple_agent_example.py`: Basic mathematical calculation agent
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
- [ ] Implement `AsyncAgent` base class with dynamic configuration
- [ ] Create flexible system instruction definition mechanism
- [ ] Design abstract LLM provider interface
- [ ] Develop dynamic role and persona assignment system
- [ ] Implement multi-modal agent capabilities (text, image, video)

### LLM Provider Abstraction
- [ ] Unified interface for diverse LLM providers
  - [ ] Google Gemini integration (start_chat(), send_message())
  - [ ] OpenAI ChatGPT integration
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
- [ ] Pluggable memory providers
  - [ ] In-memory state storage
  - [ ] Redis distributed memory
  - [ ] DynamoDB scalable storage
  - [ ] S3 content storage
- [ ] Conversation and task history tracking
- [ ] Global state management for agent crews
- [ ] Persistent task and interaction logs

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
- [ ] Async-first design
- [ ] Horizontal scaling support
- [ ] Performance benchmarking
- [ ] Resource optimization

### Testing and Quality
- [ ] Comprehensive unit testing
- [ ] Integration testing for agent interactions
- [ ] Mocking frameworks for LLM providers
- [ ] Continuous integration setup

### Documentation and Community
- [ ] Detailed API documentation
- [ ] Comprehensive developer guides
- [ ] Example use case implementations
- [ ] Contribution guidelines
- [ ] Community tool submission process
- [ ] Regular maintenance and updates

### Future Roadmap
- [ ] Payment integration solutions
- [ ] Advanced context understanding
- [ ] Multi-language support
- [ ] Enterprise-grade security features
- [ ] AI agent marketplace

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