"""Tests for GRAMI AI core functionality."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from grami_ai.core.utils import (
    to_async,
    resource_limiter,
    run_with_retry,
    merge_dicts,
    chunks
)
from grami_ai.core.exceptions import (
    GramiError,
    ValidationError,
    ResourceError,
    handle_exception,
    format_error,
    is_retryable_error
)
from grami_ai.core.constants import (
    Environment,
    MemoryBackend,
    EventType,
    Priority
)

# Utility tests
@pytest.mark.asyncio
async def test_to_async_decorator():
    """Test the to_async decorator."""
    def sync_func(x: int) -> int:
        return x * 2
    
    async_func = to_async(sync_func)
    result = await async_func(5)
    assert result == 10

@pytest.mark.asyncio
async def test_to_async_with_timeout():
    """Test the to_async decorator with timeout."""
    def slow_func() -> str:
        import time
        time.sleep(0.1)
        return "done"
    
    async_func = to_async(slow_func, timeout=0.2)
    result = await async_func()
    assert result == "done"
    
    with pytest.raises(TimeoutError):
        async_func = to_async(slow_func, timeout=0.05)
        await async_func()

@pytest.mark.asyncio
async def test_resource_limiter():
    """Test the resource limiter context manager."""
    from grami_ai.core.config import settings
    
    original_limit = settings.limits.MAX_CONCURRENT_TASKS
    settings.limits.MAX_CONCURRENT_TASKS = 1
    
    async with resource_limiter():
        assert settings.limits.MAX_CONCURRENT_TASKS == 0
    
    assert settings.limits.MAX_CONCURRENT_TASKS == 1
    settings.limits.MAX_CONCURRENT_TASKS = original_limit

@pytest.mark.asyncio
async def test_run_with_retry():
    """Test the retry functionality."""
    call_count = 0
    
    async def failing_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ResourceError("Temporary error")
        return "success"
    
    result = await run_with_retry(failing_func, max_attempts=3)
    assert result == "success"
    assert call_count == 3
    
    with pytest.raises(ResourceError):
        await run_with_retry(failing_func, max_attempts=2)

def test_merge_dicts():
    """Test dictionary merging."""
    dict1 = {"a": 1, "b": {"c": 2}}
    dict2 = {"b": {"d": 3}, "e": 4}
    
    result = merge_dicts(dict1, dict2)
    assert result == {
        "a": 1,
        "b": {"c": 2, "d": 3},
        "e": 4
    }

def test_chunks():
    """Test list chunking."""
    data = list(range(10))
    chunked = chunks(data, 3)
    assert len(chunked) == 4
    assert chunked == [[0,1,2], [3,4,5], [6,7,8], [9]]

# Exception tests
def test_handle_exception():
    """Test exception handling."""
    try:
        raise ValueError("Test error")
    except Exception as e:
        grami_error = handle_exception(
            e,
            "An error occurred",
            ValidationError
        )
        assert isinstance(grami_error, ValidationError)
        assert grami_error.message == "An error occurred"
        assert grami_error.details["type"] == "ValueError"

def test_format_error():
    """Test error formatting."""
    error = GramiError(
        message="Test error",
        code="TEST_ERROR",
        details={"key": "value"}
    )
    
    formatted = format_error(error)
    assert formatted["error"]["code"] == "TEST_ERROR"
    assert formatted["error"]["message"] == "Test error"
    assert formatted["error"]["details"]["key"] == "value"

def test_retryable_error_check():
    """Test retryable error classification."""
    assert is_retryable_error(ResourceError("Test"))
    assert not is_retryable_error(ValidationError("Test"))

# Constants tests
def test_environment_enum():
    """Test environment enum."""
    assert Environment.DEVELOPMENT == "development"
    assert Environment.TESTING == "testing"
    assert Environment.PRODUCTION == "production"

def test_memory_backend_enum():
    """Test memory backend enum."""
    assert MemoryBackend.REDIS == "redis"
    assert MemoryBackend.IN_MEMORY == "in_memory"
    assert MemoryBackend.POSTGRESQL == "postgresql"

def test_event_type_enum():
    """Test event type enum."""
    assert EventType.TASK_CREATED == "task.created"
    assert EventType.TASK_COMPLETED == "task.completed"

def test_priority_enum():
    """Test priority enum."""
    assert Priority.LOW == 0
    assert Priority.HIGH == 2
    assert Priority.CRITICAL == 3
