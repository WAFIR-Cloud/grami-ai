"""
Grami AI Core Constants Module

This module defines constants, enums, and static values used across the framework.
"""

from enum import Enum, auto
from typing import Final

# Environment constants
class Environment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

# Memory constants
class MemoryBackend(str, Enum):
    """Supported memory backend types."""
    REDIS = "redis"
    IN_MEMORY = "in_memory"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"

# Event constants
class EventType(str, Enum):
    """Event types for the event system."""
    TASK_CREATED = "task.created"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    AGENT_STARTED = "agent.started"
    AGENT_STOPPED = "agent.stopped"
    MEMORY_UPDATED = "memory.updated"
    CONFIG_CHANGED = "config.changed"

# Resource constants
class ResourceType(str, Enum):
    """Resource types for resource management."""
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"

# Status constants
class Status(str, Enum):
    """Common status values."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

# Priority constants
class Priority(int, Enum):
    """Task priority levels."""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

# LLM Provider constants
class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"

# Time constants
SECOND: Final[int] = 1
MINUTE: Final[int] = 60 * SECOND
HOUR: Final[int] = 60 * MINUTE
DAY: Final[int] = 24 * HOUR
WEEK: Final[int] = 7 * DAY

# Size constants
KB: Final[int] = 1024
MB: Final[int] = 1024 * KB
GB: Final[int] = 1024 * MB

# Default timeouts
DEFAULT_TIMEOUT: Final[float] = 30.0  # seconds
EXTENDED_TIMEOUT: Final[float] = 300.0  # seconds
INFINITE_TIMEOUT: Final[float] = -1.0

# Default retry settings
DEFAULT_MAX_RETRIES: Final[int] = 3
DEFAULT_RETRY_DELAY: Final[float] = 1.0  # seconds
MAX_RETRY_DELAY: Final[float] = 60.0  # seconds

# Default batch sizes
DEFAULT_BATCH_SIZE: Final[int] = 100
MAX_BATCH_SIZE: Final[int] = 1000

# Default resource limits
DEFAULT_MEMORY_LIMIT: Final[int] = 512 * MB
DEFAULT_STORAGE_LIMIT: Final[int] = 1 * GB
DEFAULT_CONCURRENT_TASKS: Final[int] = 10

# Cache settings
DEFAULT_CACHE_TTL: Final[int] = 1 * HOUR
MAX_CACHE_SIZE: Final[int] = 1000

# API settings
DEFAULT_PAGE_SIZE: Final[int] = 50
MAX_PAGE_SIZE: Final[int] = 200
DEFAULT_RATE_LIMIT: Final[int] = 100  # requests per minute

# Security constants
TOKEN_EXPIRY: Final[int] = 24 * HOUR  # seconds
REFRESH_TOKEN_EXPIRY: Final[int] = 7 * DAY  # seconds
PASSWORD_MIN_LENGTH: Final[int] = 8
MAX_LOGIN_ATTEMPTS: Final[int] = 5

# Logging constants
class LogLevel(str, Enum):
    """Log levels for the logging system."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# File system constants
MAX_FILE_SIZE: Final[int] = 100 * MB
ALLOWED_FILE_TYPES: Final[tuple] = (".txt", ".json", ".yaml", ".yml")

# Database constants
DEFAULT_DB_POOL_SIZE: Final[int] = 10
MAX_DB_CONNECTIONS: Final[int] = 100
DB_CONNECTION_TIMEOUT: Final[float] = 5.0  # seconds
DB_COMMAND_TIMEOUT: Final[float] = 30.0  # seconds

# Message queue constants
MAX_MESSAGE_SIZE: Final[int] = 1 * MB
MESSAGE_RETENTION: Final[int] = 7 * DAY  # seconds
QUEUE_MAX_LENGTH: Final[int] = 10000

# HTTP constants
HTTP_TIMEOUT: Final[float] = 30.0  # seconds
MAX_REDIRECTS: Final[int] = 5
USER_AGENT: Final[str] = "grami-ai/1.0"

# Role constants
class Role(str, Enum):
    """Conversation role types."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
