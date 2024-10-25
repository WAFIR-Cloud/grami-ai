import asyncio
import redis.asyncio as aioredis
import pytest
from grami_ai.state import RedisState
from redis.exceptions import RedisError  # Import RedisError for exception handling

# Update fixture to use async for to retrieve the actual RedisState instance
@pytest.fixture
async def redis_state():
    """Fixture to create and clean up a RedisState instance for each test."""
    state = RedisState()
    await state.connect()
    yield state
    await state.close()


@pytest.mark.asyncio
async def test_get_set_delete(redis_state):
    """Tests basic get, set, and delete operations."""
    await redis_state.set("test_key", "test_value")
    assert await redis_state.get("test_key") == "test_value"
    await redis_state.delete("test_key")
    assert await redis_state.get("test_key") is None

@pytest.mark.asyncio
async def test_get_with_default(redis_state):
    """Tests retrieving a key with a default value."""
    assert await redis_state.get("nonexistent_key", "default_value") == "default_value"

@pytest.mark.asyncio
async def test_get_key_not_found(redis_state):
    """Tests retrieving a nonexistent key without a default value."""
    with pytest.raises(ValueError) as excinfo:
        await redis_state.get("nonexistent_key")
    assert str(excinfo.value) == "Key 'nonexistent_key' not found in Redis."

@pytest.mark.asyncio
async def test_set_with_expire(redis_state):
    """Tests setting a key with an expiration time."""
    await redis_state.set("test_key", "test_value", expire=1)
    assert await redis_state.get("test_key") == "test_value"
    await asyncio.sleep(1.1)  # Wait for the key to expire
    assert await redis_state.get("test_key") is None

@pytest.mark.asyncio
async def test_connection_error(monkeypatch):
    """Simulates a connection error."""
    async def mock_from_url(*args, **kwargs):
        raise RedisError("Mock connection error")

    monkeypatch.setattr(aioredis, "from_url", mock_from_url)

    state = RedisState()
    with pytest.raises(ConnectionError) as excinfo:
        await state.connect()
    assert str(excinfo.value) == "Failed to connect to Redis: Mock connection error"

@pytest.mark.asyncio
async def test_redis_error(redis_state, monkeypatch):
    """Simulates a Redis error during an operation."""
    async def mock_get(*args, **kwargs):
        raise RedisError("Mock Redis error")

    # Access redis_state._redis only after ensuring the connection is established
    await redis_state.connect()  # Ensure redis_state._redis is initialized
    monkeypatch.setattr(redis_state._redis, "get", mock_get)

    with pytest.raises(RedisError) as excinfo:
        await redis_state.get("test_key")
    assert str(excinfo.value) == "Failed to get value for key 'test_key': Mock Redis error"
