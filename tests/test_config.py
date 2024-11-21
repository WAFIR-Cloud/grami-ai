"""Tests for GRAMI AI configuration system."""

import os
import pytest
from unittest.mock import patch
from typing import Dict, Any

from grami_ai.core.config import (
    Settings,
    Environment,
    load_config,
    validate_config,
    merge_configs
)
from grami_ai.core.exceptions import ConfigurationError

class TestConfiguration:
    """Test suite for configuration management."""

    @pytest.fixture
    def default_config(self) -> Dict[str, Any]:
        """Default configuration for testing."""
        return {
            "environment": Environment.DEVELOPMENT,
            "log_level": "INFO",
            "memory": {
                "backend": "redis",
                "redis": {
                    "host": "localhost",
                    "port": 6379
                }
            },
            "limits": {
                "max_concurrent_tasks": 10,
                "request_timeout": 30
            }
        }

    def test_settings_initialization(self, default_config):
        """Test settings object initialization."""
        settings = Settings(default_config)
        
        assert settings.environment == Environment.DEVELOPMENT
        assert settings.log_level == "INFO"
        assert settings.memory.backend == "redis"
        assert settings.memory.redis.host == "localhost"
        assert settings.memory.redis.port == 6379

    def test_environment_variables_override(self, default_config):
        """Test environment variable overrides."""
        with patch.dict(os.environ, {
            "GRAMI_ENV": "production",
            "GRAMI_LOG_LEVEL": "DEBUG",
            "GRAMI_MEMORY_BACKEND": "postgresql"
        }):
            settings = Settings(default_config)
            assert settings.environment == Environment.PRODUCTION
            assert settings.log_level == "DEBUG"
            assert settings.memory.backend == "postgresql"

    def test_nested_config_access(self, default_config):
        """Test accessing nested configuration."""
        settings = Settings(default_config)
        
        assert settings.limits.max_concurrent_tasks == 10
        assert settings.limits.request_timeout == 30
        
        with pytest.raises(AttributeError):
            settings.nonexistent_key

    def test_config_validation(self, default_config):
        """Test configuration validation."""
        # Valid config
        assert validate_config(default_config) is True
        
        # Invalid environment
        invalid_config = default_config.copy()
        invalid_config["environment"] = "invalid"
        with pytest.raises(ConfigurationError):
            validate_config(invalid_config)
        
        # Missing required field
        invalid_config = default_config.copy()
        del invalid_config["environment"]
        with pytest.raises(ConfigurationError):
            validate_config(invalid_config)

    def test_config_merging(self, default_config):
        """Test configuration merging."""
        override_config = {
            "log_level": "DEBUG",
            "memory": {
                "redis": {
                    "port": 6380
                }
            }
        }
        
        merged = merge_configs(default_config, override_config)
        assert merged["log_level"] == "DEBUG"
        assert merged["memory"]["redis"]["port"] == 6380
        assert merged["memory"]["redis"]["host"] == "localhost"

    def test_environment_specific_config(self, default_config):
        """Test environment-specific configuration."""
        with patch.dict(os.environ, {"GRAMI_ENV": "production"}):
            prod_settings = Settings(default_config)
            assert prod_settings.environment == Environment.PRODUCTION
            
            # Production should have stricter limits
            assert prod_settings.limits.max_concurrent_tasks <= 10

    def test_config_file_loading(self, tmp_path):
        """Test loading configuration from file."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("""
            environment: development
            log_level: INFO
            memory:
                backend: redis
                redis:
                    host: localhost
                    port: 6379
        """)
        
        config = load_config(str(config_path))
        assert config["environment"] == Environment.DEVELOPMENT
        assert config["memory"]["backend"] == "redis"

    def test_sensitive_config_handling(self, default_config):
        """Test handling of sensitive configuration."""
        with patch.dict(os.environ, {
            "GRAMI_API_KEY": "secret_key",
            "GRAMI_DATABASE_PASSWORD": "db_password"
        }):
            settings = Settings(default_config)
            
            # Sensitive values should not appear in string representation
            settings_str = str(settings)
            assert "secret_key" not in settings_str
            assert "db_password" not in settings_str

    def test_dynamic_config_update(self, default_config):
        """Test dynamic configuration updates."""
        settings = Settings(default_config)
        
        # Update single value
        settings.update("log_level", "DEBUG")
        assert settings.log_level == "DEBUG"
        
        # Update nested value
        settings.update("memory.redis.port", 6380)
        assert settings.memory.redis.port == 6380
        
        # Invalid updates should fail
        with pytest.raises(ConfigurationError):
            settings.update("nonexistent.key", "value")

    def test_config_export(self, default_config):
        """Test configuration export functionality."""
        settings = Settings(default_config)
        exported = settings.export()
        
        assert exported["environment"] == Environment.DEVELOPMENT
        assert exported["memory"]["backend"] == "redis"
        
        # Sensitive values should be masked
        assert all(
            not isinstance(v, str) or not v.startswith("secret_")
            for v in exported.values()
        )
