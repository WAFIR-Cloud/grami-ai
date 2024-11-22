from .base import tool_registry, ToolCategory, ToolMetadata, AsyncBaseTool
from .content_generation import ContentGenerationTool
from .web_search import GoogleWebSearchTool

__all__ = [
    'ContentGenerationTool', 
    'create_content_generation_tool',
    'create_web_search_tool',
    'GoogleWebSearchTool',
    'tool_registry',
    'ToolCategory',
    'ToolMetadata',
    'AsyncBaseTool'
]

# Add a convenience method to create content generation tool
def create_content_generation_tool():
    """
    Convenience method to create and register a content generation tool
    
    Returns:
        Registered ContentGenerationTool instance
    """
    return tool_registry.add_content_generation_tool()

# Convenience method to create and register web search tool
def create_web_search_tool():
    """
    Convenience method to create and register a web search tool
    
    Returns:
        Registered GoogleWebSearchTool instance
    """
    tool = GoogleWebSearchTool()
    tool_registry.register_tool(tool)
    return tool
