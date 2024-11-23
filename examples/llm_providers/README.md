# LLM Providers Examples

This directory contains examples demonstrating different Language Model Providers in the GRAMI-AI framework.

## Gemini Provider Examples

- `async_gemini_no_memory_no_streaming.py`: Basic agent interaction without memory or streaming
- `async_gemini_no_memory_streaming.py`: Agent interaction with response streaming
- `async_gemini_redis_memory.py`: Agent with Redis-based memory storage
- `async_gemini_stream_memory_example.py`: Streaming with memory support

## Running Examples

```bash
# Example of running a Gemini provider example
python -m examples.llm_providers.gemini.async_gemini_no_memory_no_streaming
```

## Key Concepts

- Different LLM provider configurations
- Memory management
- Response streaming
- Tool integration
