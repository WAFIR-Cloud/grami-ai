"""
Grami AI Core Utilities Module

This module provides common utility functions and helpers used across the framework.
It includes:
- Async helpers
- Type conversion
- Data validation
- Error handling
- Resource management
"""

import asyncio
import functools
import inspect
import logging
from datetime import datetime, timezone
from typing import (
    Any, Callable, Coroutine, Dict, List, Optional, 
    TypeVar, Union, overload, cast
)
from contextlib import asynccontextmanager
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    RetryError
)

from .config import settings

# Type variables
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """Configure logging based on settings."""
    logging.basicConfig(
        level=getattr(logging, settings.logging.LEVEL),
        format=settings.logging.FORMAT,
        filename=settings.logging.FILE_PATH
    )

def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)

@overload
def to_async(func: Callable[..., T]) -> Callable[..., Coroutine[Any, Any, T]]: ...

@overload
def to_async(*, timeout: float) -> Callable[[F], F]: ...

def to_async(
    func: Optional[Callable[..., T]] = None,
    *,
    timeout: Optional[float] = None
) -> Union[
    Callable[..., Coroutine[Any, Any, T]],
    Callable[[F], F]
]:
    """Convert a synchronous function to asynchronous.
    
    Args:
        func: Function to convert
        timeout: Optional timeout in seconds
        
    Returns:
        Async version of the function
        
    Example:
        @to_async
        def cpu_intensive() -> int:
            # Heavy computation
            return 42
            
        @to_async(timeout=5.0)
        def network_call() -> str:
            # Network request
            return "response"
    """
    def decorator(f: Callable[..., T]) -> Callable[..., Coroutine[Any, Any, T]]:
        @functools.wraps(f)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            loop = asyncio.get_running_loop()
            if timeout:
                return await asyncio.wait_for(
                    loop.run_in_executor(None, lambda: f(*args, **kwargs)),
                    timeout=timeout
                )
            return await loop.run_in_executor(None, lambda: f(*args, **kwargs))
        return wrapper
    
    if func is None:
        return cast(Callable[[F], F], decorator)
    return decorator(func)

@asynccontextmanager
async def resource_limiter():
    """Context manager for resource limiting."""
    try:
        # Check resource limits
        if settings.limits.MAX_CONCURRENT_TASKS <= 0:
            raise ValueError("No tasks available")
        
        # Acquire resources
        settings.limits.MAX_CONCURRENT_TASKS -= 1
        yield
        
    finally:
        # Release resources
        settings.limits.MAX_CONCURRENT_TASKS += 1

async def run_with_retry(
    func: Callable[..., Coroutine[Any, Any, T]],
    *args: Any,
    max_attempts: int = 3,
    **kwargs: Any
) -> T:
    """Run an async function with retry logic.
    
    Args:
        func: Async function to run
        *args: Positional arguments for func
        max_attempts: Maximum number of retry attempts
        **kwargs: Keyword arguments for func
        
    Returns:
        Result from the function
        
    Raises:
        RetryError: If all retries fail
    """
    @retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _run() -> T:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Retry attempt failed: {str(e)}")
            raise
    
    try:
        return await _run()
    except RetryError as e:
        logger.error(f"All retry attempts failed: {str(e)}")
        raise

class AsyncIteratorWrapper:
    """Helper class to wrap sync iterators for async usage."""
    
    def __init__(self, obj: Any, **kwargs: Any):
        self._it = iter(obj)
        self._kwargs = kwargs
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            value = next(self._it)
            if inspect.isawaitable(value):
                return await value
            return value
        except StopIteration:
            raise StopAsyncIteration

def async_iterator(obj: Any) -> AsyncIteratorWrapper:
    """Convert a sync iterator to async iterator."""
    return AsyncIteratorWrapper(obj)

def validate_json(data: Dict[str, Any]) -> bool:
    """Validate if a dictionary is JSON serializable."""
    try:
        import json
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False

def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge multiple dictionaries."""
    result: Dict[str, Any] = {}
    for d in dicts:
        for k, v in d.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = merge_dicts(result[k], v)
            else:
                result[k] = v
    return result

def chunks(lst: List[T], n: int) -> List[List[T]]:
    """Split a list into n-sized chunks."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]
