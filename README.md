# 🚀 Grami AI: Flexible LLM Agent Framework

## 🎯 Project Overview
Grami AI is a cutting-edge Python library for building intelligent, flexible AI agents with seamless Language Model integration.

## ✨ Key Features
- **LLM-Agnostic Design**: Easily switch between different Language Models
- **Dynamic Agent Configuration**: Plug-and-play LLM providers
- **Async Communication**: Non-blocking, high-performance interactions
- **Modular Architecture**: Extensible and customizable

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip

### Install via pip
```bash
pip install grami-ai
```

### Optional Dependencies
- For Gemini Integration: `pip install grami-ai[gemini]`
- For OLLAMA/LLAMA: `pip install grami-ai[ollama]`

## 🌐 Supported LLM Providers
- Google Gemini
- OLLAMA/LLAMA
- Easy to add custom providers!

## 💻 Comprehensive Usage Guide

### 1. Basic Agent Creation
```python
import asyncio
from grami_ai.agents.BaseAgent import BaseAgent
from grami_ai.llms.gemini_llm import GeminiLLMProvider
from grami_ai.memory.memory import InMemoryAbstractMemory

async def main():
    # Create memory and LLM provider
    memory = InMemoryAbstractMemory()
    gemini_provider = GeminiLLMProvider(
        api_key='YOUR_GOOGLE_AI_API_KEY',
        model_name='gemini-pro'
    )

    # Initialize agent
    agent = BaseAgent(
        llm_provider=gemini_provider,
        memory=memory
    )

    # Send a message
    response = await agent.send_message("Hello, how are you?")
    print(response)

asyncio.run(main())
```

### 2. Advanced Agent Configuration
```python
# Custom configuration with generation parameters
agent = BaseAgent(
    llm_provider=gemini_provider,
    memory=memory,
    tools=[CustomTool1(), CustomTool2()],
    generation_config={
        'temperature': 0.7,
        'max_tokens': 1024,
        'top_p': 0.9
    }
)
```

### 3. Creating a Custom LLM Provider
```python
from grami_ai.llms.base_llm import BaseLLMProvider

class MyCustomLLMProvider(BaseLLMProvider):
    async def start_chat(self, system_instruction=None):
        # Initialize your custom LLM connection
        pass

    async def send_message(self, message):
        # Implement message sending logic
        pass

    async def format_history(self, conversation_history):
        # Custom history formatting
        pass
```

## 🚀 Implementation Strategies

### Dependency Injection
```python
# Inject different components dynamically
memory_strategy = RedisMemory() if use_redis else InMemoryAbstractMemory()
llm_provider = select_llm_provider(provider_type)

agent = BaseAgent(
    llm_provider=llm_provider,
    memory=memory_strategy
)
```

### Tool Integration
```python
class CalculatorTool:
    def calculate(self, expression):
        # Implement calculation logic
        return eval(expression)

# Add tool to agent
agent.add_tool(CalculatorTool())
```

## 🔬 Advanced Techniques

### Conversation Context Management
```python
# Persist and retrieve conversation context
conversation_id = 'unique_conversation_123'
await memory.add_item(conversation_id, {'role': 'user', 'content': 'Hello'})
history = await memory.get_items(conversation_id)
```

## 🚧 Future Development Roadmap

### Planned Features
1. 🌈 More LLM Provider Integrations
   - OpenAI GPT
   - Anthropic Claude
   - Mistral AI
   - Local model support expansion

2. 🛠 Enhanced Tool Ecosystem
   - Pre-built tools for common tasks
   - Enhanced tool discovery and management
   - Better tool composition and chaining

3. 🧠 Advanced Memory Backends
   - Distributed memory storage
   - Persistent memory solutions
   - Machine learning-enhanced memory retrieval

4. 📊 Monitoring and Observability
   - Conversation analytics
   - Performance tracking
   - Detailed logging and tracing

5. 🔒 Security Enhancements
   - Advanced input sanitization
   - Configurable safety filters
   - Comprehensive error handling

### Research Directions
- Multi-modal agent interactions
- Reinforcement learning for agent behavior
- Cross-language model collaboration
- Ethical AI development practices

## 🤝 Contributing

### Ways to Contribute
1. Report Bugs
2. Suggest Enhancements
3. Submit Pull Requests
4. Improve Documentation
5. Create Example Use Cases

### Contribution Guidelines
- Follow PEP 8 Style Guide
- Write Comprehensive Tests
- Document New Features
- Maintain Backward Compatibility

## 📄 License
MIT License - Empowering Open-Source AI Innovation

## 🌟 Star the Project!
If you find Grami AI useful, please give us a star on GitHub!
