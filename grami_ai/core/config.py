"""
Configuration management for GRAMI AI.

This module handles configuration settings for the GRAMI AI framework,
including API keys, model settings, and environment variables.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import Field, validator
from pydantic_settings import BaseSettings

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
        return f"postgresql+asyncpg://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}/{values['POSTGRES_DB']}"
    
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
        return f"redis://{values['REDIS_HOST']}:{values['REDIS_PORT']}/{values['REDIS_DB']}"
    
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
        return f"amqp://guest:guest@localhost:5672"
    
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
    """
    Configuration settings for GRAMI AI.
    
    Handles:
    - API keys for different providers
    - Model configurations
    - Environment settings
    """
    
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
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, env='OPENAI_API_KEY')
    google_api_key: Optional[str] = Field(None, env='GOOGLE_API_KEY')
    anthropic_api_key: Optional[str] = Field(None, env='ANTHROPIC_API_KEY')
    
    # Ollama Settings
    ollama_base_url: str = Field("http://localhost:11434", env='OLLAMA_BASE_URL')
    
    # Logging
    log_level: str = Field("INFO", env='LOG_LEVEL')
    
    # Model Defaults
    default_model: str = Field("gpt-3.5-turbo", env='DEFAULT_MODEL')
    
    # Generation Config
    generation_config: Dict[str, Any] = Field(
        default={
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2000
        }
    )
    
    @validator('log_level')
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return upper_v
    
    def configure(self, **kwargs: Any) -> None:
        """
        Update configuration settings.
        
        Args:
            **kwargs: Configuration key-value pairs
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

    class Config:
        env_prefix = "GRAMI_"
        case_sensitive = True

# Global settings instance
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
