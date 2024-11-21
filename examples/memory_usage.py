import asyncio
from grami_ai.memory import AsyncInMemoryMemory, AsyncRedisMemory

async def demonstrate_memory_usage():
    # In-Memory Memory Example
    print("🔹 In-Memory Memory Example:")
    in_memory = AsyncInMemoryMemory(max_size=3)
    
    conversation_id = "user_chat_123"
    
    # Add conversation items
    await in_memory.add_item(conversation_id, {"role": "user", "content": "Hello"})
    await in_memory.add_item(conversation_id, {"role": "assistant", "content": "Hi there!"})
    await in_memory.add_item(conversation_id, {"role": "user", "content": "How are you?"})
    
    # Retrieve items
    items = await in_memory.get_items(conversation_id)
    for item in items:
        print(f"📝 {item['role']}: {item['content']}")
    
    # Clear conversation
    await in_memory.clear_conversation(conversation_id)
    
    # Redis Memory Example (commented out, requires Redis server)
    # print("\n🔹 Redis Memory Example:")
    # redis_memory = AsyncRedisMemory()
    # await redis_memory.add_item(conversation_id, {"role": "user", "content": "Redis test"})
    # redis_items = await redis_memory.get_items(conversation_id)
    # for item in redis_items:
    #     print(f"📝 {item['role']}: {item['content']}")

if __name__ == "__main__":
    asyncio.run(demonstrate_memory_usage())
