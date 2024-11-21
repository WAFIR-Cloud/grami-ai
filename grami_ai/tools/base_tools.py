"""
Grami AI Base Tools Module

This module provides foundational async tools for the Grami AI framework,
offering a comprehensive set of utility functions and base classes for 
building intelligent, asynchronous AI agents.

Key Features:
- Async tool base classes
- Flexible tool design
- Comprehensive error handling
- Modular architecture
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

class BaseTool(ABC):
    """
    Abstract base class for all Grami AI tools.

    Provides a standardized interface for async tool implementation,
    ensuring consistent behavior across different tool types.

    Attributes:
        name (str): Unique identifier for the tool.
        description (str): Human-readable description of the tool's purpose.
        logger (logging.Logger): Logging instance for the tool.
    """

    def __init__(
        self, 
        name: str, 
        description: str, 
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize a base tool with name, description, and optional logger.

        Args:
            name (str): Unique name for the tool.
            description (str): Detailed description of the tool's functionality.
            logger (Optional[logging.Logger], optional): Custom logger. 
                Defaults to None, which creates a default logger.
        """
        self.name = name
        self.description = description
        self.logger = logger or logging.getLogger(f"grami_ai.tools.{name}")

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method to execute the tool's primary functionality.

        Must be implemented by all subclasses to define the tool's core logic.

        Args:
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Any: Result of the tool's execution.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError(f"Tool {self.name} must implement run() method")

    async def validate_input(self, *args: Any, **kwargs: Any) -> bool:
        """
        Validate input parameters before tool execution.

        Provides a hook for input validation and preprocessing.

        Args:
            *args: Variable positional arguments to validate.
            **kwargs: Variable keyword arguments to validate.

        Returns:
            bool: True if input is valid, False otherwise.
        """
        return True

    def __str__(self) -> str:
        """
        String representation of the tool.

        Returns:
            str: Tool's name and description.
        """
        return f"Tool: {self.name} - {self.description}"

class CalculatorTool(BaseTool):
    """
    A specialized async calculator tool for mathematical operations.

    Supports basic arithmetic operations with comprehensive error handling
    and logging.

    Attributes:
        Inherits all attributes from BaseTool.
    """

    def __init__(self):
        """
        Initialize the CalculatorTool with predefined name and description.
        """
        super().__init__(
            name="calculator", 
            description="Perform mathematical calculations asynchronously"
        )

    async def run(
        self, 
        operation: str, 
        a: Union[int, float], 
        b: Union[int, float]
    ) -> Union[int, float]:
        """
        Perform a mathematical operation asynchronously.

        Args:
            operation (str): Mathematical operation to perform.
                Supported: 'add', 'subtract', 'multiply', 'divide'
            a (Union[int, float]): First operand.
            b (Union[int, float]): Second operand.

        Returns:
            Union[int, float]: Result of the calculation.

        Raises:
            ValueError: For invalid operations or division by zero.
        """
        await asyncio.sleep(0.1)  # Simulate async operation

        if not await self.validate_input(operation, a, b):
            raise ValueError("Invalid input parameters")

        try:
            if operation == 'add':
                return a + b
            elif operation == 'subtract':
                return a - b
            elif operation == 'multiply':
                return a * b
            elif operation == 'divide':
                if b == 0:
                    raise ValueError("Division by zero")
                return a / b
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            raise

    async def validate_input(
        self, 
        operation: str, 
        a: Union[int, float], 
        b: Union[int, float]
    ) -> bool:
        """
        Validate calculator input parameters.

        Args:
            operation (str): Mathematical operation.
            a (Union[int, float]): First operand.
            b (Union[int, float]): Second operand.

        Returns:
            bool: True if inputs are valid, False otherwise.
        """
        valid_operations = ['add', 'subtract', 'multiply', 'divide']
        
        if operation not in valid_operations:
            self.logger.warning(f"Invalid operation: {operation}")
            return False
        
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            self.logger.warning("Operands must be numeric")
            return False
        
        return True

class JSONParserTool(BaseTool):
    """
    Async JSON parsing and manipulation tool
    
    Supports:
    - JSON parsing
    - JSON validation
    - JSON transformation
    """
    
    def __init__(self):
        super().__init__(
            name="json_parser", 
            description="Parse and manipulate JSON data"
        )
    
    async def run(
        self, 
        json_data: str, 
        operation: str = 'parse',
        **kwargs: Any
    ) -> Any:
        """
        Async JSON processing method
        
        Args:
            json_data: JSON string to process
            operation: Processing operation (parse, validate, transform)
            **kwargs: Additional operation-specific parameters
        
        Returns:
            Processed JSON data
        """
        # Simulate async work
        await asyncio.sleep(0.1)
        
        try:
            if operation == 'parse':
                return json.loads(json_data)
            
            elif operation == 'validate':
                json.loads(json_data)
                return True
            
            elif operation == 'transform':
                data = json.loads(json_data)
                return self._transform_json(data, **kwargs)
            
            else:
                raise ValueError(f"Unsupported JSON operation: {operation}")
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    def _transform_json(
        self, 
        data: Dict[str, Any], 
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Transform JSON data based on provided rules
        
        Args:
            data: Input JSON data
            **kwargs: Transformation rules
        
        Returns:
            Transformed JSON data
        """
        # Example transformation logic
        if 'filter_keys' in kwargs:
            keys_to_keep = kwargs['filter_keys']
            return {k: v for k, v in data.items() if k in keys_to_keep}
        
        return data

class StringManipulationTool(BaseTool):
    """
    Async string manipulation tool
    
    Supports:
    - Text transformations
    - String analysis
    - Text cleaning
    """
    
    def __init__(self):
        super().__init__(
            name="string_manipulation", 
            description="Perform advanced string operations"
        )
    
    async def run(
        self, 
        text: str, 
        operation: str = 'clean',
        **kwargs: Any
    ) -> Any:
        """
        Async string processing method
        
        Args:
            text: Input text to process
            operation: Processing operation
            **kwargs: Additional operation-specific parameters
        
        Returns:
            Processed text
        """
        # Simulate async work
        await asyncio.sleep(0.1)
        
        try:
            if operation == 'clean':
                return self._clean_text(text)
            
            elif operation == 'count_words':
                return self._count_words(text)
            
            elif operation == 'reverse':
                return self._reverse_text(text)
            
            elif operation == 'capitalize':
                return self._capitalize_text(text, **kwargs)
            
            else:
                raise ValueError(f"Unsupported string operation: {operation}")
        
        except Exception as e:
            raise ValueError(f"String manipulation error: {e}")
    
    def _clean_text(self, text: str) -> str:
        """Remove extra whitespaces and normalize text"""
        return ' '.join(text.split())
    
    def _count_words(self, text: str) -> int:
        """Count words in the text"""
        return len(text.split())
    
    def _reverse_text(self, text: str) -> str:
        """Reverse the text"""
        return text[::-1]
    
    def _capitalize_text(
        self, 
        text: str, 
        mode: str = 'first'
    ) -> str:
        """
        Capitalize text based on mode
        
        Args:
            text: Input text
            mode: Capitalization mode (first, all, sentence)
        """
        if mode == 'first':
            return text.capitalize()
        elif mode == 'all':
            return text.upper()
        elif mode == 'sentence':
            return text.capitalize()
        else:
            raise ValueError(f"Invalid capitalization mode: {mode}")

class WebScraperTool(BaseTool):
    """
    Async web scraping tool
    
    Supports:
    - Fetching web content
    - Parsing HTML
    - Extracting specific elements
    """
    
    def __init__(self):
        super().__init__(
            name="web_scraper", 
            description="Fetch and parse web content"
        )
    
    async def run(
        self, 
        url: str, 
        operation: str = 'fetch',
        **kwargs: Any
    ) -> Any:
        """
        Async web scraping method
        
        Args:
            url: URL to scrape
            operation: Scraping operation
            **kwargs: Additional operation-specific parameters
        
        Returns:
            Scraped content
        """
        try:
            import aiohttp
            import bs4
        except ImportError:
            raise ImportError("Please install aiohttp and beautifulsoup4 for web scraping")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch URL: {response.status}")
                
                content = await response.text()
                
                if operation == 'fetch':
                    return content
                
                elif operation == 'parse':
                    soup = bs4.BeautifulSoup(content, 'html.parser')
                    return soup.get_text()
                
                elif operation == 'extract':
                    soup = bs4.BeautifulSoup(content, 'html.parser')
                    selector = kwargs.get('selector', 'body')
                    elements = soup.select(selector)
                    return [elem.get_text() for elem in elements]
                
                else:
                    raise ValueError(f"Unsupported web scraping operation: {operation}")
