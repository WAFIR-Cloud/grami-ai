# 🚀 GRAMI AI Examples

This directory contains examples demonstrating how to use GRAMI AI framework, with a focus on private and hybrid AI deployments.

## 🔐 Private AI Deployment

### Using Ollama (Recommended for Full Privacy)

[`ollama_agent.py`](ollama_agent.py) shows how to deploy GRAMI with Ollama for complete privacy:

```python
from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import CalculatorTool

async def main():
    # Initialize agent with Ollama
    agent = AsyncAgent(
        tools=[CalculatorTool()],
        memory=InMemoryAbstractMemory(),
        model="ollama/llama2",  # Local Llama 2 model
        provider_config={
            "base_url": "http://localhost:11434"
        }
    )
    
    # Process tasks privately
    result = await agent.execute_task({
        "objective": "Data analysis",
        "input": "Analyze this financial data while keeping it private..."
    })
```

### Using Google Gemini (Hybrid Option)

[`basic_gemini_agent.py`](basic_gemini_agent.py) demonstrates using Google's Gemini for a balance of privacy and performance:

```python
from grami_ai.agent import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.tools import WebScraperTool

async def main():
    # Initialize agent with Gemini
    agent = AsyncAgent(
        tools=[WebScraperTool()],
        memory=InMemoryAbstractMemory(),
        model="gemini-pro",
        provider_config={
            "api_key": "your-google-api-key"
        }
    )
    
    # Execute tasks with enterprise-grade privacy
    result = await agent.execute_task({
        "objective": "Market research",
        "input": "Analyze public market trends for AI companies"
    })
```

## 🎯 Example Categories

### Core Examples
- [`basic_agent.py`](basic_agent.py): Simple agent setup with essential tools
- [`advanced_agent.py`](advanced_agent.py): Advanced features like event handling and Redis memory

### Privacy-Focused Examples
- [`ollama_agent.py`](ollama_agent.py): Full private deployment with Ollama
- [`basic_gemini_agent.py`](basic_gemini_agent.py): Enterprise deployment with Gemini

### Optional Provider Examples
- [`openai_agent.py`](openai_agent.py): OpenAI integration example
- [`anthropic_agent.py`](anthropic_agent.py): Anthropic Claude example

## 🛠️ Setup

1. Install GRAMI with your chosen provider:
```bash
# For private deployment (recommended)
pip install grami-ai[ollama]

# For hybrid deployment
pip install grami-ai[gemini]

# For all providers
pip install grami-ai[all]
```

2. Set up your environment:
```bash
# For Ollama (local deployment)
export OLLAMA_BASE_URL=http://localhost:11434

# For Gemini
export GOOGLE_API_KEY=your-key-here

# Optional providers
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here
```

## 🚀 Running Examples

### Private Deployment
```bash
# Run Ollama example (ensure Ollama is running)
python -m examples.ollama_agent

# Run Gemini example
python -m examples.basic_gemini_agent
```

### Other Examples
```bash
python -m examples.basic_agent
python -m examples.advanced_agent
```

## 🔒 Privacy Considerations

1. **Ollama Deployment**:
   - All data stays within your infrastructure
   - No external API calls
   - Full control over model selection

2. **Gemini Integration**:
   - Enterprise-grade privacy controls
   - Data residency options
   - Configurable data retention

## 📚 Additional Resources

- [Full Documentation](https://docs.grami-ai.org)
- [Security Guide](https://docs.grami-ai.org/security)
- [Provider Setup](https://docs.grami-ai.org/providers)
- [API Reference](https://docs.grami-ai.org/api)
