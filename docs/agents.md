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
async for token in async_agent.stream_message("Explain photosynthesis"):
    print(token, end='', flush=True)
```

## Common Parameters

Both agent types share these common parameters:

- `name`: Unique identifier for the agent
- `role`: The agent's primary function or purpose
- `llm_provider`: Language model provider (e.g., GeminiProvider)
- `memory_provider`: Optional memory management system
- `communication_provider`: Optional communication interface
- `tools`: Optional list of tools/functions
- `initial_context`: Initial conversation context
- `config`: Additional configuration parameters

## Key Features

### Message Handling
- `send_message()`: Send a message and get a complete response
- `stream_message()`: Get a streaming response token by token

### Tool Integration
- `add_tool()`: Add new tools to the agent's capabilities
- Support for custom tool development

### Context Management
- `initialize_conversation()`: Set up initial conversation context
- Support for conversation history tracking

### Memory Management
- Optional memory provider integration
- Conversation state persistence

## Best Practices

1. **Choose the Right Agent Type**
   - Use `Agent` for simple interactions
   - Use `AsyncAgent` for streaming and complex interactions

2. **Context Management**
   - Always provide clear initial context
   - Use system messages to define behavior

3. **Error Handling**
   - Implement try-catch blocks for async operations
   - Handle potential API errors gracefully

4. **Resource Management**
   - Use async context managers when appropriate
   - Clean up resources after use

5. **Security**
   - Store API keys in environment variables
   - Never expose sensitive information in code

## Examples

Check out our example implementations in the `examples/` directory:
- `simple_agent_example.py`: Basic Agent usage
- `simple_async_agent.py`: AsyncAgent implementation
- More complex examples in the examples directory
