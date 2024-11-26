# GRAMI-AI Framework

A dynamic and flexible AI agent framework for building intelligent, multi-modal AI agents. GRAMI-AI provides a simple yet powerful interface for creating AI agents that can interact with various LLM providers, maintain conversation history, and handle both streaming and non-streaming responses.

## 🚀 Features

- 🤖 Multiple LLM Provider Support (Gemini, OpenAI, Anthropic)
- 📝 Streaming and Non-streaming Response Handling
- 💾 Built-in Memory Management (LRU Cache)
- 🔄 Asynchronous Operation Support
- 🛠️ Configurable Generation Parameters
- 🔍 Error Handling and Recovery
- 📦 Easy Integration and Setup

## 📦 Installation

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

## 🛠️ Configuration Options

### Generation Configuration

You can customize the behavior of the language model by adjusting the generation configuration:

```python
generation_config = {
    "temperature": 0.9,      # Controls response creativity (0.0 to 1.0)
    "top_p": 0.9,           # Nucleus sampling parameter
    "top_k": 40,            # Top-k sampling parameter
    "max_output_tokens": 1000,  # Maximum response length
    "candidate_count": 1     # Number of response candidates
}
```

### Memory Configuration

Configure the memory capacity to control how many messages are retained:

```python
memory = LRUMemory(capacity=5)  # Stores last 5 messages
```

## 🔄 Streaming vs Non-streaming

GRAMI-AI supports both streaming and non-streaming responses:

```python
# Streaming response
async for chunk in agent.stream_message("Tell me a story"):
    print(chunk, end="", flush=True)

# Non-streaming response
response = await agent.send_message("What's 2+2?")
```

## 🚨 Error Handling

GRAMI-AI includes built-in error handling for common issues:

- Automatic retry for RECITATION errors
- Connection error handling
- Invalid API key detection
- Rate limit handling

## 📚 Examples

Check out more examples in the [examples](./examples) directory:

- Basic agent usage
- Custom provider implementation
- Memory management
- Advanced configurations

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