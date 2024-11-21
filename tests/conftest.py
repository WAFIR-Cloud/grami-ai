"""Test configuration and fixtures for GRAMI AI."""

import os
import pytest
import asyncio
from typing import AsyncGenerator, Generator
import fakeredis.aioredis
from unittest.mock import AsyncMock, patch

from grami_ai.core.config import settings
from grami_ai.memory import RedisMemory
from grami_ai.core.utils import setup_logging

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def env_setup() -> Generator[None, None, None]:
    """Set up test environment variables."""
    original_env = dict(os.environ)
    os.environ.update({
        "GRAMI_ENV": "testing",
        "GRAMI_LOG_LEVEL": "DEBUG",
        "GRAMI_MEMORY_BACKEND": "redis",
        "GRAMI_REDIS_HOST": "localhost",
        "GRAMI_REDIS_PORT": "6379"
    })
    setup_logging()
    yield
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
async def redis_memory() -> AsyncGenerator[RedisMemory, None]:
    """Create a Redis memory instance with fakeredis."""
    fake_redis = fakeredis.aioredis.FakeRedis()
    with patch("grami_ai.memory.redis_memory.aioredis.Redis", return_value=fake_redis):
        memory = RedisMemory(
            host=settings.redis.host,
            port=settings.redis.port
        )
        yield memory
        await fake_redis.flushall()
        await fake_redis.close()

@pytest.fixture
def mock_llm_provider() -> AsyncMock:
    """Create a mock LLM provider."""
    provider = AsyncMock()
    provider.generate.return_value = {
        "text": "Mock LLM response",
        "usage": {"prompt_tokens": 10, "completion_tokens": 20}
    }
    return provider

@pytest.fixture
def mock_tool() -> AsyncMock:
    """Create a mock tool."""
    tool = AsyncMock()
    tool.name = "mock_tool"
    tool.description = "A mock tool for testing"
    tool.execute.return_value = {"result": "Mock tool result"}
    return tool

@pytest.fixture
def mock_event_handler() -> AsyncMock:
    """Create a mock event handler."""
    handler = AsyncMock()
    handler.handle_event.return_value = None
    return handler
