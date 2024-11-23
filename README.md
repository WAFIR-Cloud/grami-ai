# GRAMI-AI: Intelligent Agent Framework

<div align="center">
    <img src="https://img.shields.io/badge/version-0.3.107-blue.svg" alt="Version">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Versions">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/github/stars/YAFATEK/grami-ai?style=social" alt="GitHub Stars">
</div>

## Overview

GRAMI-AI is a cutting-edge, async-first AI agent framework designed to solve complex computational challenges through intelligent, collaborative agent interactions. Built with unprecedented flexibility, this library empowers developers to create sophisticated, context-aware AI systems that can adapt, learn, and collaborate across diverse domains.

## Key Features

- **Async-First Architecture**: Designed for high-performance, non-blocking operations
- **Multi-Modal Agent Interactions**: Seamless collaboration between specialized AI agents
- **Flexible LLM Integration**: Support for multiple language models (Gemini, OpenAI, Anthropic)
- **Dynamic Tool Ecosystem**: Easily extensible with custom tools and capabilities
- **Context-Aware Agents**: Intelligent agents that maintain and leverage conversation context

## Installation

```bash
pip install grami-ai
```

## Quick Start

```python
import asyncio
from grami.agent import Agent
from grami.providers import GeminiProvider
from grami.tools import CalculatorTool

async def main():
    # Create an intelligent math agent
    math_agent = Agent(
        name="MathTutor",
        role="Mathematical Problem Solver",
        llm_provider=GeminiProvider(api_key="your_api_key"),
        tools=[CalculatorTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a helpful math assistant who explains solutions step by step."
            }
        ]
    )

    # Solve a mathematical problem
    response = await math_agent.send_message(
        "Calculate the area of a circle with radius 5 and explain your reasoning"
    )
    print(response)

asyncio.run(main())
```

## Core Concepts

### Agents
Intelligent, configurable entities capable of:
- Specialized role-based interactions
- Autonomous tool utilization
- Contextual learning and adaptation

### Providers
Seamless integration with:
- Google Gemini
- OpenAI GPT
- Anthropic Claude

### Tools
Extensible capabilities including:
- Mathematical calculations
- Web search
- Weather information retrieval
- Custom tool development

## Supported Platforms

- Python 3.8+
- Linux
- macOS
- Windows

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Ways to Contribute
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About YAFATEK Solutions

GRAMI-AI is developed by YAFATEK Solutions, a technology innovation company dedicated to pushing the boundaries of artificial intelligence and software engineering.

## Contact & Support

- **Email**: support@yafatek.dev
- **GitHub Issues**: [Report an Issue](https://github.com/YAFATEK/grami-ai/issues)
- **Website**: [YAFATEK Solutions](https://yafatek.dev)

---

**Star ⭐ the project if you find it useful!**