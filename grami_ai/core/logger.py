import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json
import asyncio
import os

from grami_ai.core.config import settings, Settings

class ColorFormatter(logging.Formatter):
    """
    Colorized log formatter for enhanced readability
    """
    COLORS = {
        "DEBUG": "\033[94m",    # Blue
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "CRITICAL": "\033[95m", # Magenta
        "RESET": "\033[0m"      # Reset
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        log_format = (
            f"{color}[%(levelname)s] %(asctime)s - %(message)s{reset}"
        )
        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

class AsyncLogger:
    """
    Advanced async-first logging system for Grami AI
    
    Features:
    - Async logging
    - Multiple output streams
    - Structured logging
    - Colorized output
    - Telemetry support
    """
    
    def __init__(
        self, 
        name: str = "grami_ai", 
        config: Optional[Settings] = None
    ):
        """
        Initialize logger with flexible configuration
        
        Args:
            name: Logger name
            config: Optional configuration settings
        """
        self.config = config or settings
        self.name = name
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._get_log_level())
        
        # Configure handlers
        self._setup_handlers()
    
    def _get_log_level(self) -> int:
        """
        Convert string log level to logging module constant
        
        Returns:
            Logging level constant
        """
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(self.config.logging.LEVEL.upper(), logging.INFO)
    
    def _setup_handlers(self):
        """
        Configure logging handlers based on configuration
        
        Supports:
        - Console logging with colors
        - File logging
        - Optional telemetry
        """
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console Handler with Color Formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        self.logger.addHandler(console_handler)
        
        # Optional File Logging
        log_file = self.config.logging.FILE_PATH
        if log_file:
            # Ensure log directory exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )
            self.logger.addHandler(file_handler)
    
    async def log(
        self, 
        level: str, 
        message: str, 
        extra: Optional[Dict[str, Any]] = None
    ):
        """
        Async logging method with structured logging support
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            message: Log message
            extra: Additional context
        """
        # Prepare log record
        log_record = {
            'timestamp': datetime.now().isoformat(),
            'level': level.upper(),
            'message': message,
            'extra': extra or {}
        }
        
        # Async log method to prevent blocking
        def _log():
            log_method = getattr(self.logger, level.lower())
            log_method(json.dumps(log_record))
        
        # Run in executor to avoid blocking
        await asyncio.get_event_loop().run_in_executor(None, _log)
    
    async def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Debug level logging"""
        await self.log('DEBUG', message, extra)
    
    async def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Info level logging"""
        await self.log('INFO', message, extra)
    
    async def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Warning level logging"""
        await self.log('WARNING', message, extra)
    
    async def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Error level logging"""
        await self.log('ERROR', message, extra)
    
    async def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Critical level logging"""
        await self.log('CRITICAL', message, extra)

# Global logger instance
logger = AsyncLogger()

# Async context manager for logging
class LoggingContext:
    """
    Context manager for structured logging and performance tracking
    
    Supports:
    - Automatic logging of method entry/exit
    - Performance tracking
    - Error capture
    """
    
    def __init__(
        self, 
        name: str, 
        logger: Optional[AsyncLogger] = None
    ):
        """
        Initialize logging context
        
        Args:
            name: Context/method name
            logger: Optional custom logger
        """
        self.name = name
        self.logger = logger or globals()['logger']
        self.start_time = None
    
    async def __aenter__(self):
        """
        Async context entry point
        
        Logs method entry and records start time
        """
        self.start_time = datetime.now()
        await self.logger.debug(
            f"Entering {self.name}", 
            {'method': self.name}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context exit point
        
        Logs method exit, duration, and handles exceptions
        """
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type:
            # Log exception details
            await self.logger.error(
                f"Exception in {self.name}", 
                {
                    'method': self.name,
                    'exception_type': str(exc_type),
                    'exception_value': str(exc_val),
                    'duration': duration
                }
            )
            return False  # Propagate exception
        
        await self.logger.debug(
            f"Exiting {self.name}", 
            {
                'method': self.name,
                'duration_seconds': duration
            }
        )
        return True  # No exception
