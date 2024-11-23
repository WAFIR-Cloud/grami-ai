import asyncio
import pytest
import json
from grami.memory import RedisMemory

@pytest.mark.asyncio
async def test_redis_memory_basic_operations():
    """Test basic add, get, and remove operations."""
    memory = RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  # Use a test database 
        capacity=10
    )
    
    # Add an item
    await memory.add('test_key', 'test_value')
    
    # Retrieve the item
    retrieved_value = await memory.get('test_key')
    assert retrieved_value == 'test_value'
    
    # Remove the item
    remove_result = await memory.remove('test_key')
    assert remove_result is True
    
    # Verify item is removed
    non_existent = await memory.get('test_key')
    assert non_existent is None

@pytest.mark.asyncio
async def test_redis_memory_capacity():
    """Test memory capacity and LRU behavior."""
    memory = RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  
        capacity=3
    )
    
    # Add more items than capacity
    await memory.add('key1', 'value1')
    await memory.add('key2', 'value2')
    await memory.add('key3', 'value3')
    await memory.add('key4', 'value4')
    
    # Retrieve recent items
    recent_items = await memory.get_recent_items(limit=3)
    
    # Check that only the last 3 items are present
    assert len(recent_items) == 3
    assert any(item['key'] == 'key2' for item in recent_items)
    assert any(item['key'] == 'key3' for item in recent_items)
    assert any(item['key'] == 'key4' for item in recent_items)
    
    # Verify first key is removed
    first_key_exists = await memory.get('key1')
    assert first_key_exists is None

@pytest.mark.asyncio
async def test_redis_memory_clear():
    """Test clearing all memory items."""
    memory = RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  
        capacity=10
    )
    
    # Add some items
    await memory.add('key1', 'value1')
    await memory.add('key2', 'value2')
    
    # Clear memory
    await memory.clear()
    
    # Verify items are removed
    assert await memory.get('key1') is None
    assert await memory.get('key2') is None

@pytest.mark.asyncio
async def test_redis_memory_context_manager():
    """Test async context manager functionality."""
    async with RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  
        capacity=10
    ) as memory:
        await memory.add('context_key', 'context_value')
        retrieved_value = await memory.get('context_key')
        assert retrieved_value == 'context_value'
    
    # After context manager exit, memory should still work
    async with RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  
        capacity=10
    ) as memory:
        retrieved_value = await memory.get('context_key')
        assert retrieved_value == 'context_value'

@pytest.mark.asyncio
async def test_redis_memory_timestamp():
    """Test that timestamps are correctly added and retrieved."""
    memory = RedisMemory(
        host='localhost', 
        port=6379, 
        db=1,  
        capacity=10
    )
    
    # Add an item
    await memory.add('timestamp_key', 'timestamp_value')
    
    # Get recent items and check timestamp
    recent_items = await memory.get_recent_items(limit=1)
    
    assert len(recent_items) == 1
    assert 'timestamp' in recent_items[0]
    assert 'key' in recent_items[0]
    assert 'value' in recent_items[0]
    assert recent_items[0]['key'] == 'timestamp_key'
    assert recent_items[0]['value'] == 'timestamp_value'

# Note: These tests require a Redis server running on localhost:6379
# You may need to adjust the connection parameters based on your Redis setup
