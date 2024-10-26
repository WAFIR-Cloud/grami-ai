import asyncio
import json
import os
from typing import Any, Optional, List
import redis.asyncio as aioredis
from redis.exceptions import RedisError  # Import RedisError from redis.exceptions

# Configuration using environment variable
REDIS_URL = os.environ.get("GRAMI_REDIS_URL", "redis://localhost")


class RedisState:
    """
    A wrapper around aioredis to provide a convenient interface for
    managing shared state in Redis.
    """

    def __init__(self, redis_url: str = REDIS_URL):
        """
        Initializes the RedisState with the provided Redis connection URL.

        Args:
            redis_url: The URL for connecting to the Redis server.
                       Defaults to the REDIS_URL constant.
        """
        self.redis_url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def connect(self):
        """Establishes a connection to the Redis server if not already connected."""
        try:
            if self._redis is None:
                self._redis = await aioredis.from_url(self.redis_url)
        except RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    async def close(self):
        """Closes the connection to the Redis server."""
        if self._redis is not None:
            try:
                await self._redis.aclose()
            except RedisError as e:
                raise ConnectionError(f"Failed to close Redis connection: {e}")
            finally:
                self._redis = None

    async def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value associated with a key.

        Args:
            key: The key to retrieve.
            default: The value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if the key is not found.

        Raises:
            ValueError: If the key is not found and no default value is provided.
            RedisError: If there is an error communicating with Redis.
        """
        try:
            await self.connect()
            value = await self._redis.get(key)
            if value is None:
                if default is not None:
                    return default
                else:
                    raise ValueError(f"Key '{key}' not found in Redis.")
            return json.loads(value.decode())  # Deserialize JSON data
        except RedisError as e:
            raise RedisError(f"Failed to get value for key '{key}': {e}")

    async def set(self, key: str, value: Any, expire: int = None) -> None:
        """
        Sets the value associated with a key.

        Args:
            key: The key to set.
            value: The value to set.
            expire: Optional expiration time in seconds.

        Raises:
            RedisError: If there is an error communicating with Redis.
        """
        try:
            await self.connect()
            serialized_value = json.dumps(value).encode()  # Serialize data to JSON
            if expire:
                await self._redis.set(key, serialized_value, ex=expire)
            else:
                await self._redis.set(key, serialized_value)
        except RedisError as e:
            raise RedisError(f"Failed to set value for key '{key}': {e}")

    async def delete(self, key: str) -> None:
        """
        Deletes a key from Redis.

        Args:
            key: The key to delete.

        Raises:
            RedisError: If there is an error communicating with Redis.
        """
        try:
            await self.connect()
            await self._redis.delete(key)
        except RedisError as e:
            raise RedisError(f"Failed to delete key '{key}': {e}")

    async def exists(self, key: str) -> bool:
        """
        Checks if a key exists in Redis.

        Args:
            key: The key to check.

        Returns:
            True if the key exists, False otherwise.

        Raises:
            RedisError: If there is an error communicating with Redis.
        """
        try:
            await self.connect()
            return await self._redis.exists(key) > 0
        except RedisError as e:
            raise RedisError(f"Failed to check existence of key '{key}': {e}")

    async def lpush(self, key: str, value: Any) -> None:
        """Pushes a value to the beginning of a list in Redis."""
        await self.connect()
        await self._redis.lpush(key, value)

    async def lrange(self, key: str, start: int, end: int) -> List[Any]:
        """Retrieves a range of items from a list in Redis."""
        await self.connect()
        return await self._redis.lrange(key, start, end)

    async def ltrim(self, key: str, start: int, end: int) -> None:
        """Trims a list to only include items within a specified range."""
        await self.connect()
        await self._redis.ltrim(key, start, end)

# Create a global instance of RedisState
state = RedisState()


async def main():
    """Tests the functionality of the RedisState class."""

    try:
        # Test set and get
        await state.set("test_key", {"name": "Test User", "age": 30})
        value = await state.get("test_key")
        print(f"Retrieved value: {value}")

        # Test exists
        exists = await state.exists("test_key")
        print(f"Key exists: {exists}")

        # Test delete
        await state.delete("test_key")
        exists = await state.exists("test_key")
        print(f"Key exists after delete: {exists}")

    except RedisError as e:
        print(f"Redis error: {e}")
    finally:
        # Explicitly close the Redis connection
        await state.close()


if __name__ == '__main__':
    asyncio.run(main())
