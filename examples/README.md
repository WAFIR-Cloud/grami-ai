# Grami AI Agent Examples

## Overview
These examples demonstrate the flexibility of the Grami AI Agent system, showcasing different ways to use the BaseAgent with various Language Model providers.

## Prerequisites
- Python 3.8+
- Install required dependencies: `pip install grami-ai`
- For Gemini LLM examples, set the `GOOGLE_AI_API_KEY` environment variable

## Example Scripts

### 1. `basic_gemini_agent.py`
- Demonstrates basic usage of BaseAgent with Gemini LLM
- Shows how to create an agent with a configuration dictionary
- Illustrates conversation history persistence using in-memory storage

### 2. `custom_llm_provider.py`
- Shows how to create a custom LLM provider by implementing the `BaseLLMProvider` interface
- Provides a mock implementation for testing and demonstration purposes
- Demonstrates the flexibility of the agent system

### 3. `advanced_agent_usage.py`
- Showcases advanced features like:
  - Adding custom tools to the agent
  - Using tools within the conversation
  - Maintaining conversation context
- Includes a simple calculator tool example

## Running the Examples
```bash
# Set your Google AI API key (for Gemini examples)
export GOOGLE_AI_API_KEY='your_api_key_here'

# Run each example
python basic_gemini_agent.py
python custom_llm_provider.py
python advanced_agent_usage.py
```

## Notes
- Replace `'your_api_key_here'` with your actual Google AI API key
- Ensure you have the latest version of the `grami-ai` package installed
- These examples are meant to demonstrate usage and may require adaptation to your specific use case

## Contributing
Feel free to submit pull requests with additional example use cases or improvements!
