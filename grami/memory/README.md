# Grami AI Memory Providers

## Redis Memory Provider

### Overview
The Redis Memory Provider offers a distributed, scalable memory solution for Grami AI agents. It leverages Redis as a backend to store and manage memory items with configurable capacity and provider-specific namespacing.

### Features
- Async implementation with full support for concurrent operations
- Configurable Redis connection parameters
- Least Recently Used (LRU) capacity management
- Timestamped memory items
- Async context manager support
- Multiple method interfaces (`add`/`store`, `get`/`retrieve`)
- Unique chat/provider ID support

### Installation Requirements
- Redis server (version 5.0+)
- Python 3.8+
- redis library (async)

### Installation
```bash
pip install grami-ai[redis]
```

### Basic Usage

```python
import asyncio
from grami.memory import RedisMemory

async def example():
    # Initialize Redis Memory with a unique chat ID
    memory = RedisMemory(
        host='localhost',       # Redis server host
        port=6379,              # Redis server port
        db=0,                   # Redis database number
        capacity=100,           # Maximum number of items to store
        provider_id='chat_123'  # Unique identifier for this conversation
    )
    
    # Store conversation items
    await memory.store('user_query_1', 'Hello, tell me a story')
    await memory.store('agent_response_1', 'Once upon a time...')
    
    # Retrieve specific memory items
    query = await memory.retrieve('user_query_1')
    
    # List all memory contents
    contents = await memory.list_contents()
    
    # Get recent items
    recent_items = await memory.get_recent_items(limit=5)
    
    # Clear memory when done
    await memory.clear()

asyncio.run(example())
```

### Configuration Options
- `host`: Redis server hostname (default: 'localhost')
- `port`: Redis server port (default: 6379)
- `db`: Redis database number (default: 0)
- `capacity`: Maximum number of memory items (default: 100)
- `provider_id`: Unique identifier for memory namespace (optional)

### Performance Considerations
- Redis provides fast, in-memory storage with optional persistence
- Async implementation ensures non-blocking memory operations
- LRU capacity management prevents unbounded memory growth

### Troubleshooting
- Ensure Redis server is running before initializing memory
- Check network connectivity and Redis configuration
- Use unique `provider_id` to prevent memory key collisions

### Error Handling
```python
try:
    await memory.store('key', 'value')
except Exception as e:
    print(f"Memory storage error: {e}")
```

### License
MIT License

### Contributing
Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.
