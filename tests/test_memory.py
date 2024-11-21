import asyncio
import pytest

from grami_ai.memory import (
    AbstractMemory, 
    InMemoryAbstractMemory, 
    RedisMemory, 
    AsyncRedisMemory, 
    AsyncInMemoryMemory
)

@pytest.mark.asyncio
class TestMemoryProviders:
    async def test_in_memory_memory(self):
        memory = InMemoryAbstractMemory()
        conversation_id = "test_conversation"
        test_item = {"role": "user", "content": "Hello"}
        
        await memory.add_item(conversation_id, test_item)
        items = await memory.get_items(conversation_id)
        
        assert len(items) == 1
        assert items[0] == test_item
        
        await memory.clear_conversation(conversation_id)
        items = await memory.get_items(conversation_id)
        assert len(items) == 0

    @pytest.mark.skip(reason="Requires Redis server")
    async def test_redis_memory(self):
        memory = RedisMemory()
        conversation_id = "test_conversation"
        test_item = {"role": "user", "content": "Hello"}
        
        await memory.add_item(conversation_id, test_item)
        items = await memory.get_items(conversation_id)
        
        assert len(items) == 1
        assert items[0] == test_item
        
        await memory.clear_items(conversation_id)
        items = await memory.get_items(conversation_id)
        assert len(items) == 0

    async def test_async_in_memory_memory(self):
        memory = AsyncInMemoryMemory(max_size=2)
        conversation_id = "test_conversation"
        
        # Test adding items
        await memory.add_item(conversation_id, {"content": "First"})
        await memory.add_item(conversation_id, {"content": "Second"})
        await memory.add_item(conversation_id, {"content": "Third"})
        
        # Check max size
        items = await memory.get_items(conversation_id)
        assert len(items) == 2
        assert items[0]["content"] == "Second"
        assert items[1]["content"] == "Third"
        
        # Test clearing
        await memory.clear_conversation(conversation_id)
        items = await memory.get_items(conversation_id)
        assert len(items) == 0

    @pytest.mark.skip(reason="Requires Redis server")
    async def test_async_redis_memory(self):
        memory = AsyncRedisMemory()
        conversation_id = "test_conversation"
        
        # Test adding items
        await memory.add_item(conversation_id, {"content": "First"})
        await memory.add_item(conversation_id, {"content": "Second"})
        
        # Retrieve items
        items = await memory.get_items(conversation_id)
        assert len(items) == 2
        
        # Test clearing
        await memory.clear_conversation(conversation_id)
        items = await memory.get_items(conversation_id)
        assert len(items) == 0
