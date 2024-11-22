# 🚀 GRAMI AI: Your Social Media Growth AI Agent

## 🌟 Overview

GRAMI AI is an advanced, async-first AI framework designed to revolutionize social media marketing and content creation. Leveraging cutting-edge AI technologies, GRAMI provides intelligent, context-aware agents that can help businesses grow their online presence.

## 🔥 Key Features

- 🤖 **Intelligent Agents**: Async-first design with dynamic tool integration
- 🛠 **Extensible Tools**: Easily create and integrate custom AI-powered tools
- 💬 **Multi-Provider Support**: Work with various LLM providers seamlessly
- 🔒 **Secure Configuration**: Environment-based settings and secure key management
- 📊 **Comprehensive Logging**: Advanced async logging with context awareness

## 📦 Installation

```bash
pip install grami-ai
```

## 🚀 Quick Start

### Basic Agent Creation

```python
import asyncio
from grami_ai.core.agent import AsyncAgent

async def main():
    # Create a marketing assistant agent
    agent = await AsyncAgent.create(
        name="MarketingAssistant",
        llm="gemini",  # Use Gemini LLM
        tools=["content_generation", "web_search"],
        system_instruction="Help small businesses improve their social media marketing"
    )

    # Generate Instagram content
    response = await agent.process({
        "type": "content_request",
        "platform": "instagram",
        "niche": "coffee shop",
        "content_type": "post"
    })

    print(response)

# Run the agent
asyncio.run(main())
```

### Custom Tool Example

```python
from grami_ai.tools.base import AsyncBaseTool

class ImageGenerationTool(AsyncBaseTool):
    def __init__(self):
        super().__init__()
        self.metadata.name = "generate_images"
        self.metadata.description = "Generate marketing images"

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        # Implement image generation logic
        return {
            'status': 'success',
            'images': [f"generated_image_{i+1}.jpg" for i in range(context.get('number_of_images', 1))]
        }

    def get_parameters(self):
        return {
            "query": {
                "type": "string",
                "description": "Image generation prompt"
            },
            "number_of_images": {
                "type": "integer",
                "description": "Number of images to generate",
                "default": 1
            }
        }
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

Built with ❤️ by YAFATek Solutions, pushing the boundaries of AI-powered solutions.