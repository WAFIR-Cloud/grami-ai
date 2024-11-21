import asyncio
import json
import re
from typing import Any, Dict, Optional

from grami_ai.core.interfaces import AsyncTool

class BaseTool(AsyncTool):
    """
    Base implementation for async tools
    
    Provides:
    - Async execution
    - Input validation
    - Error handling
    - Logging support
    """
    
    def __init__(
        self, 
        name: str, 
        description: Optional[str] = None
    ):
        """
        Initialize a base tool
        
        Args:
            name: Tool name
            description: Optional tool description
        """
        self.name = name
        self.description = description or f"Tool for {name} operations"
    
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Base async execution method
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Execution result
        """
        raise NotImplementedError("Subclasses must implement execute method")

class CalculatorTool(BaseTool):
    """
    Async calculator tool with advanced parsing
    
    Supports:
    - Basic arithmetic
    - Complex expressions
    - Error handling
    """
    
    def __init__(self):
        super().__init__(
            name="calculator", 
            description="Perform mathematical calculations"
        )
    
    async def execute(self, expression: str) -> float:
        """
        Async calculation method
        
        Args:
            expression: Mathematical expression to evaluate
        
        Returns:
            Calculation result
        
        Raises:
            ValueError: For invalid expressions
        """
        # Simulate async work
        await asyncio.sleep(0.1)
        
        # Sanitize and validate expression
        sanitized_expr = self._sanitize_expression(expression)
        
        try:
            result = eval(sanitized_expr)
            return float(result)
        except (SyntaxError, TypeError, ZeroDivisionError) as e:
            raise ValueError(f"Invalid calculation: {e}")
    
    def _sanitize_expression(self, expression: str) -> str:
        """
        Sanitize mathematical expression
        
        Args:
            expression: Raw expression string
        
        Returns:
            Sanitized expression
        """
        # Remove whitespace
        expression = expression.replace(' ', '')
        
        # Validate characters
        if not re.match(r'^[0-9+\-*/().]+$', expression):
            raise ValueError("Invalid characters in expression")
        
        return expression

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
    
    async def execute(
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
    
    async def execute(
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
    
    async def execute(
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
