# GRAMI-AI Agents Documentation

GRAMI-AI provides two main types of agents: `Agent` and `AsyncAgent`. Both types share similar capabilities but are designed for different use cases.

## Agent Types

### Agent

The `Agent` class is the core implementation that provides synchronous operations with async support. It's ideal for simple interactions and when you need straightforward request-response patterns.

```python
from grami.agent import Agent
from grami.providers import GeminiProvider

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

### AsyncAgent

The `AsyncAgent` class is designed for fully asynchronous operations and streaming responses. It's particularly useful for:
- Long-running conversations
- Streaming responses
- Complex multi-turn interactions
- Scientific explanations and detailed responses

```python
from grami.agent import AsyncAgent
from grami.providers import GeminiProvider

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
async for chunk in async_agent.stream_message("Describe the evolution of stars"):
    print(chunk, end="", flush=True)
```

## LLM Providers

### GeminiProvider

The `GeminiProvider` class offers integration with Google's Gemini model, supporting both synchronous and asynchronous operations.

```python
from grami.providers import GeminiProvider

provider = GeminiProvider(api_key="YOUR_API_KEY")

# Direct content generation
content = await provider.generate_content("What are the three laws of robotics?")
print(content)

# Use with AsyncAgent for advanced features
agent = AsyncAgent(
    name="GeminiAI",
    role="AI Assistant",
    llm_provider=provider
)
```

Key features:
- Native async support with `generate_content`, `send_message`, and `stream_message`
- Context maintenance across conversations
- Streaming capability for real-time responses
- Tool integration support

## Common Parameters

Both agent types share these common parameters:

- `name`: The agent's name (string)
- `role`: The agent's role or purpose (string)
- `llm_provider`: The LLM provider instance (BaseProvider)
- `tools`: Optional list of tools the agent can use (List[BaseTool])
- `initial_context`: Optional initial conversation context (List[Dict])
- `max_tokens`: Maximum tokens per response (Optional[int])
- `temperature`: Response randomness (Optional[float])

## Best Practices

1. **Provider Selection**: Choose the appropriate provider based on your needs:
   - Use `GeminiProvider` for advanced AI capabilities and streaming support
   - Consider rate limits and API quotas when making provider decisions

2. **Agent Type Selection**:
   - Use `AsyncAgent` for complex, streaming, or long-running interactions
   - Use `Agent` for simple, synchronous operations

3. **Context Management**:
   - Provide clear roles and initial context for better responses
   - Monitor conversation length to avoid token limits
   - Use tools appropriately to extend agent capabilities

4. **Error Handling**:
   - Always implement proper error handling for API calls
   - Consider rate limiting and retry strategies
   - Handle streaming interruptions gracefully

## Examples

Check out our [examples directory](../examples) for complete implementation examples, including:
- Basic agent usage
- Async streaming
- Tool integration
- Multi-turn conversations
- Provider-specific features
