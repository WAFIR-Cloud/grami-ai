"""
Grami AI Core Configuration Module

This module provides centralized configuration management for the Grami AI framework.
It handles:
- Environment variables
- Framework settings
- Security configurations
- Integration settings
- Resource limits
"""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import os
from pydantic import BaseSettings, Field, validator
from pydantic.networks import PostgresDsn, RedisDsn, AmqpDsn

class SecuritySettings(BaseSettings):
    """Security-related settings."""
    
    SECRET_KEY: str = Field(default_factory=lambda: os.urandom(32).hex())
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_prefix = "GRAMI_SECURITY_"

class DatabaseSettings(BaseSettings):
    """Database connection settings."""
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "grami"
    ASYNC_DATABASE_URL: Optional[str] = None
    
    @validator("ASYNC_DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_HOST"],
            port=values["POSTGRES_PORT"],
            path=f"/{values['POSTGRES_DB']}",
        )
    
    class Config:
        env_prefix = "GRAMI_DB_"

class CacheSettings(BaseSettings):
    """Redis cache settings."""
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: Optional[str] = None
    
    @validator("REDIS_URL", pre=True)
    def assemble_redis_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if v:
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values["REDIS_HOST"],
            port=str(values["REDIS_PORT"]),
            path=f"/{values['REDIS_DB']}",
        )
    
    class Config:
        env_prefix = "GRAMI_CACHE_"

class MessageQueueSettings(BaseSettings):
    """Message queue settings."""
    
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_CONSUMER_GROUP: str = "grami_consumers"
    RABBITMQ_URL: Optional[str] = None
    
    @validator("RABBITMQ_URL", pre=True)
    def assemble_rabbitmq_url(cls, v: Optional[str]) -> str:
        if v:
            return v
        return AmqpDsn.build(
            scheme="amqp",
            host="localhost",
            port="5672",
            user="guest",
            password="guest",
        )
    
    class Config:
        env_prefix = "GRAMI_MQ_"

class LLMSettings(BaseSettings):
    """LLM provider settings."""
    
    PROVIDER: str = "gemini"  # gemini, openai, anthropic, ollama
    MODEL: str = "gemini-pro"
    API_KEY: Optional[str] = None
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    class Config:
        env_prefix = "GRAMI_LLM_"

class ResourceLimits(BaseSettings):
    """Resource limits and constraints."""
    
    MAX_CONCURRENT_TASKS: int = 100
    MAX_MEMORY_MB: int = 1024
    MAX_STORAGE_GB: int = 10
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW_MINUTES: int = 60
    
    class Config:
        env_prefix = "GRAMI_LIMITS_"

class LoggingSettings(BaseSettings):
    """Logging configuration."""
    
    LEVEL: str = "INFO"
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE_PATH: Optional[Path] = None
    ENABLE_TELEMETRY: bool = True
    
    class Config:
        env_prefix = "GRAMI_LOG_"

class Settings(BaseSettings):
    """Main configuration class combining all settings."""
    
    # Basic settings
    ENV: str = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Grami AI Framework"
    VERSION: str = "0.2.0"
    
    # Component settings
    security: SecuritySettings = SecuritySettings()
    database: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    queue: MessageQueueSettings = MessageQueueSettings()
    llm: LLMSettings = LLMSettings()
    limits: ResourceLimits = ResourceLimits()
    logging: LoggingSettings = LoggingSettings()
    
    class Config:
        env_prefix = "GRAMI_"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Environment-specific settings
def get_settings() -> Settings:
    """Get settings instance based on environment."""
    env = os.getenv("GRAMI_ENV", "development")
    
    if env == "test":
        return Settings(
            ENV="test",
            DEBUG=True,
            database=DatabaseSettings(POSTGRES_DB="grami_test"),
            cache=CacheSettings(REDIS_DB=1),
        )
    
    if env == "production":
        return Settings(
            ENV="production",
            DEBUG=False,
            security=SecuritySettings(
                ACCESS_TOKEN_EXPIRE_MINUTES=15,
                REFRESH_TOKEN_EXPIRE_DAYS=1,
            ),
            limits=ResourceLimits(
                MAX_CONCURRENT_TASKS=500,
                MAX_MEMORY_MB=4096,
            ),
        )
    
    return settings  # development settings
