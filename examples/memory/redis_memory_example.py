import asyncio
import logging
from grami.memory import RedisMemory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def redis_memory_demo():
    """
    Demonstrate the capabilities of RedisMemory with various operations.
    
    This example showcases:
    1. Adding items to memory
    2. Retrieving items
    3. Capacity management
    4. Retrieving recent items
    5. Removing items
    6. Clearing memory
    """
    # Initialize Redis Memory with custom configuration
    async with RedisMemory(
        host='localhost',       # Redis server host
        port=6379,              # Redis server port
        db=0,                   # Redis database number
        capacity=5,             # Maximum number of items to store
        provider_id='demo_memory'  # Optional provider identifier
    ) as memory:
        
        # Demonstrate adding items
        logger.info("Adding items to memory...")
        await memory.add('user_1', {'name': 'Alice', 'age': 30})
        await memory.add('user_2', {'name': 'Bob', 'age': 25})
        await memory.add('user_3', {'name': 'Charlie', 'age': 35})
        await memory.add('user_4', {'name': 'David', 'age': 40})
        await memory.add('user_5', {'name': 'Eve', 'age': 28})
        
        # Demonstrate capacity management
        # This will remove the oldest item (user_1) since capacity is 5
        await memory.add('user_6', {'name': 'Frank', 'age': 45})
        
        # Retrieve and print recent items
        logger.info("Retrieving recent items...")
        recent_items = await memory.get_recent_items(limit=3)
        for item in recent_items:
            logger.info(f"Recent Item - Key: {item['key']}, Value: {item['value']}, Timestamp: {item['timestamp']}")
        
        # Retrieve a specific item
        logger.info("Retrieving a specific item...")
        user_4 = await memory.get('user_4')
        logger.info(f"User 4: {user_4}")
        
        # Remove an item
        logger.info("Removing an item...")
        remove_result = await memory.remove('user_2')
        logger.info(f"Item 'user_2' removed: {remove_result}")
        
        # Verify item removal
        removed_user = await memory.get('user_2')
        logger.info(f"Removed user exists: {removed_user is not None}")
        
        # Clear all memory
        logger.info("Clearing all memory...")
        await memory.clear()
        
        # Verify memory is cleared
        recent_after_clear = await memory.get_recent_items()
        logger.info(f"Items after clear: {len(recent_after_clear)}")

async def main():
    """Main function to run the Redis memory demonstration."""
    try:
        await redis_memory_demo()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# Note: This example requires a Redis server running on localhost:6379
# Ensure Redis is installed and running before executing this script
