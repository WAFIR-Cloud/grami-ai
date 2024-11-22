import logging
import sys
from typing import Optional

def create_logger(
    name: str = "grami_ai", 
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Create a configured logger with optional file output
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional file path to log to
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Default logger
logger = create_logger()
