"""
Centralized logging configuration for GRAMI AI Framework.

This module provides a standardized logging setup across the entire framework,
ensuring consistent log formatting, levels, and output.
"""

import logging
import sys
from typing import Optional, Union

def configure_logger(
    name: str = 'grami_ai', 
    level: Union[int, str] = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a standardized logger.
    
    Args:
        name: Logger name (default: 'grami_ai')
        level: Logging level (default: logging.INFO)
        log_file: Optional file path to save logs
    
    Returns:
        Configured logging.Logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear any existing handlers to prevent duplicate logs
    logger.handlers.clear()
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter with timestamp, log level, and message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add console handler
    logger.addHandler(console_handler)
    
    # Optional file logging
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create a default logger
logger = configure_logger()
