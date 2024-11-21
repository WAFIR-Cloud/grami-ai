# Grami AI: Flexible AI Agent Framework

**grami-ai** is an advanced, modular Python library for building intelligent AI agents with unprecedented flexibility and extensibility.

## 🌟 Key Features

### 🤖 Flexible LLM Integration
- **LLM-Agnostic Architecture**: Easily integrate any Language Model provider
- **Plug-and-Play Design**: Create custom LLM providers with minimal effort
- **Built-in Gemini Support**: Seamless integration with Google's Gemini AI

### 🧠 Intelligent Agent Framework
- **Abstract Base Agent**: Standardized interface for AI agent interactions
- **Conversation Memory**: Persistent conversation tracking
- **Dynamic Tool Integration**: Extend agent capabilities with custom tools

### 🔧 Core Components
- **BaseLLMProvider**: Abstract base class for Language Model providers
- **BaseAgent**: Flexible agent implementation supporting multiple LLM backends
- **Memory Abstraction**: Pluggable memory systems (Redis, In-Memory)

## 📦 Installation

```bash
pip install grami-ai
```

## 🚀 Quick Start

### Basic Gemini LLM Usage
```python
import asyncio
from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.memory.memory import InMemoryAbstractMemory

async def main():
    # Create an agent with Gemini LLM
    agent = BaseAgent(
        llm_provider={
            'api_key': 'YOUR_GOOGLE_AI_API_KEY',
            'model_name': 'models/gemini-1.5-flash',
            'system_instruction': 'You are a helpful AI assistant.'
        },
        memory=InMemoryAbstractMemory()
    )

    # Send a message and get a response
    response = await agent.send_message("Tell me a joke about programming")
    print(response)

asyncio.run(main())
```

### Custom LLM Provider
```python
from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.agents.BaseAgent import BaseAgent

class CustomLLMProvider(BaseLLMProvider):
    # Implement abstract methods for your specific LLM
    ...

# Use your custom LLM provider
agent = BaseAgent(llm_provider=CustomLLMProvider(...))
```

## 🎯 Project Goals

Grami AI aims to revolutionize AI agent development by providing:
- Unparalleled flexibility in LLM integration
- Robust, extensible agent architecture
- Easy-to-use tools for building intelligent applications

## 📚 Documentation

### LLM Provider Interface
- Implement `BaseLLMProvider` to create custom LLM integrations
- Required methods:
  - `__init__`: Initialize LLM configuration
  - `start_chat`: Begin a new conversation
  - `send_message`: Process messages
  - `format_history`: Convert conversation history

### BaseAgent Features
- Supports multiple memory backends
- Extensible with custom tools
- Asynchronous message handling
- Conversation context preservation

## 🛠 Advanced Usage

Check out the [Examples](Examples/) directory for more detailed use cases:
- Basic Gemini LLM usage
- Custom LLM provider implementation
- Advanced agent configuration with tools

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📋 Roadmap
- [ ] Add more LLM provider integrations
- [ ] Enhance tool integration capabilities
- [ ] Develop comprehensive documentation
- [ ] Create more advanced example use cases

## 📄 License
MIT License

Copyright (c) 2024 WAFIR Cloud LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
