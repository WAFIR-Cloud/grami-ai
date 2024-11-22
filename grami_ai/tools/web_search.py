import os
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List

from grami_ai.tools.base import AsyncBaseTool, ToolMetadata, ToolCategory, tool_registry
from grami_ai.core.exceptions import ToolConfigurationError, ToolExecutionError
from grami_ai.core.config import settings

class GoogleWebSearchTool(AsyncBaseTool):
    """
    Real-world Google Web Search tool using Google Custom Search API
    
    Configuration Requirements:
    1. GOOGLE_SEARCH_API_KEY: API key for Google Custom Search
    2. GOOGLE_SEARCH_ENGINE_ID: Custom Search Engine ID
    
    Environment Variables:
    - GOOGLE_SEARCH_API_KEY
    - GOOGLE_SEARCH_ENGINE_ID
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        search_engine_id: Optional[str] = None
    ):
        """
        Initialize Google Web Search Tool
        
        Args:
            api_key: Optional API key (overrides environment variable)
            search_engine_id: Optional Search Engine ID (overrides environment variable)
        """
        super().__init__(
            metadata=ToolMetadata(
                name="GoogleWebSearch",
                description="Perform comprehensive web searches using Google Custom Search API",
                category=ToolCategory.SEARCH,
                performance_score=0.9,
                reliability_score=0.9,
                tags=["web_search", "google", "search_api"]
            )
        )
        
        # Prioritize passed arguments, then environment variables
        self.api_key = api_key or os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = search_engine_id or os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        # Validate configuration
        if not self.api_key or not self.search_engine_id:
            raise ToolConfigurationError(
                "Google Web Search requires API key and Search Engine ID. "
                "Set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables."
            )
    
    async def _execute(
        self, 
        task: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute web search using Google Custom Search API
        
        Args:
            task: Search query
            context: Additional search context (e.g., max_results)
        
        Returns:
            Structured search results
        """
        max_results = context.get('max_results', 5) if context else 5
        
        async with aiohttp.ClientSession() as session:
            try:
                params = {
                    'key': self.api_key,
                    'cx': self.search_engine_id,
                    'q': task,
                    'num': max_results
                }
                
                async with session.get('https://www.googleapis.com/customsearch/v1', params=params) as response:
                    if response.status != 200:
                        raise ToolExecutionError(f"Search API returned status {response.status}")
                    
                    data = await response.json()
                    
                    # Extract and structure search results
                    results = []
                    for item in data.get('items', []):
                        results.append({
                            'title': item.get('title', ''),
                            'link': item.get('link', ''),
                            'snippet': item.get('snippet', '')
                        })
                    
                    return {
                        'query': task,
                        'total_results': len(results),
                        'results': results
                    }
            
            except aiohttp.ClientError as e:
                raise ToolExecutionError(f"Network error during web search: {str(e)}")
            except Exception as e:
                raise ToolExecutionError(f"Unexpected error in web search: {str(e)}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Define web search parameters
        
        Returns:
            Dictionary of search parameters
        """
        return {
            "query": {
                "type": "string",
                "description": "Search query to perform",
                "required": True
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of search results",
                "default": 5,
                "min": 1,
                "max": 10
            }
        }

# Register the tool with the global registry
tool_registry.register_tool(GoogleWebSearchTool())
