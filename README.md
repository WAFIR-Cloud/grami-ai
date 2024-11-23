# Grami AI Framework

## Overview

Grami is a dynamic and flexible AI agent framework designed to create powerful, customizable AI agents with ease. The framework provides a comprehensive set of abstractions for building AI-powered applications across various domains.

## Key Features

- **Dynamic Agent Creation**: Define AI agents with specific roles and capabilities
- **Multi-LLM Support**: Compatible with multiple Language Models (OpenAI, Gemini, Anthropic, etc.)
- **Flexible Communication**: Supports various communication interfaces (WebSocket, REST, Kafka)
- **Extensible Memory Management**: Pluggable memory providers (In-Memory, Redis, DynamoDB)
- **Tool Customization**: Easily add and manage tools for agent functionality
- **Streaming Responses**: Support for streaming token-by-token responses
- **Asynchronous Design**: Built with modern Python async/await paradigms

## Quick Start

### Installation

```bash
pip install grami-ai
```

### Basic Usage

```python
from grami.agent import Agent
from grami.providers import GeminiProvider
from grami.tools import CalculatorTool

async def main():
    # Create an AI agent with a specific role and tool
    math_agent = Agent(
        name="MathAssistant",
        role="Mathematical Problem Solver",
        llm_provider=GeminiProvider(api_key="your_api_key"),
        tools=[CalculatorTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a helpful math assistant."
            }
        ]
    )

    # Send a message and get a response
    response = await math_agent.send_message("Calculate the area of a circle with radius 5")
    print(response)

    # Stream a detailed explanation
    async for token in math_agent.stream_message("Explain circle area calculation"):
        print(token, end='', flush=True)
```

## Supported Language Models

- Google Gemini
- OpenAI GPT
- Anthropic Claude (Coming Soon)

## Tools and Extensibility

Grami supports custom tools that agents can use to enhance their capabilities:

- Calculator Tool
- Web Search Tool
- Weather Information Tool
- Custom Tool Development Support

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Add more LLM providers
- [ ] Enhance tool ecosystem
- [ ] Improve documentation
- [ ] Add comprehensive test suite

## Contact

For questions, support, or collaboration, please open an issue on our GitHub repository.

.. image:: https://img.shields.io/badge/version-0.3.107-blue.svg
   :target: https://github.com/your-username/grami-ai
   :alt: Version