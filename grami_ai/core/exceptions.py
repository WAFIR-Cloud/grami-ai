"""
Grami AI Core Exceptions Module

This module defines custom exceptions and error handling utilities for the framework.
"""

from typing import Any, Dict, Optional, Type

class GramiError(Exception):
    """Base exception for all Grami AI errors."""
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}

class ConfigurationError(GramiError):
    """Raised when there is an error in configuration."""
    pass

class ValidationError(GramiError):
    """Raised when data validation fails."""
    pass

class ResourceError(GramiError):
    """Raised when there is an error with resource management."""
    pass

class MemoryError(GramiError):
    """Raised when there is an error with memory operations."""
    pass

class EventError(GramiError):
    """Raised when there is an error with event handling."""
    pass

class ProviderError(GramiError):
    """Raised when there is an error with external providers."""
    pass

class AuthenticationError(GramiError):
    """Raised when there is an authentication error."""
    pass

class RateLimitError(GramiError):
    """Raised when rate limits are exceeded."""
    pass

class TimeoutError(GramiError):
    """Raised when an operation times out."""
    pass

class NotFoundError(GramiError):
    """Raised when a requested resource is not found."""
    pass

class DuplicateError(GramiError):
    """Raised when attempting to create a duplicate resource."""
    pass

class StateError(GramiError):
    """Raised when an operation is invalid for the current state."""
    pass

def handle_exception(
    exc: Exception,
    default_msg: str = "An unexpected error occurred",
    error_cls: Type[GramiError] = GramiError
) -> GramiError:
    """Convert any exception to a GramiError.
    
    Args:
        exc: Original exception
        default_msg: Default error message
        error_cls: GramiError subclass to use
        
    Returns:
        Converted GramiError
    """
    if isinstance(exc, GramiError):
        return exc
        
    details = {
        "type": exc.__class__.__name__,
        "original_message": str(exc)
    }
    
    return error_cls(
        message=default_msg,
        details=details
    )

def format_error(error: GramiError) -> Dict[str, Any]:
    """Format a GramiError for API responses.
    
    Args:
        error: GramiError instance
        
    Returns:
        Formatted error dictionary
    """
    return {
        "error": {
            "code": error.code,
            "message": error.message,
            "details": error.details
        }
    }

def is_retryable_error(error: Exception) -> bool:
    """Check if an error should trigger a retry.
    
    Args:
        error: Exception to check
        
    Returns:
        True if error is retryable
    """
    retryable_errors = (
        TimeoutError,
        ResourceError,
        ProviderError
    )
    
    return isinstance(error, retryable_errors)

def is_fatal_error(error: Exception) -> bool:
    """Check if an error is fatal and should stop processing.
    
    Args:
        error: Exception to check
        
    Returns:
        True if error is fatal
    """
    fatal_errors = (
        ConfigurationError,
        AuthenticationError,
        ValidationError
    )
    
    return isinstance(error, fatal_errors)
