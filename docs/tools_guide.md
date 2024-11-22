# Grami AI Tools Guide

## Overview

Tools are the core building blocks of the Grami AI Framework. They provide modular, extensible functionality for various tasks such as content generation, web searching, and more.

## Tool Basics

### What is a Tool?
- A self-contained unit of functionality
- Implements the `AsyncBaseTool` interface
- Can be dynamically registered and used

### Key Components
- **Metadata**: Describes tool characteristics
- **generate()** method: Core tool functionality
- **run()** method: Default execution wrapper

## Creating a Custom Tool

### Step-by-Step Guide

1. Import Required Classes
```python
from grami_ai.tools.base import AsyncBaseTool, ToolMetadata, ToolCategory
```

2. Define Your Tool Class
```python
class MyCustomTool(AsyncBaseTool):
    def __init__(self, metadata=None):
        # Define default metadata if not provided
        default_metadata = ToolMetadata(
            name="my_custom_tool",
            description="A specialized tool for specific tasks",
            category=ToolCategory.CUSTOM,
            performance_score=0.7,
            reliability_score=0.8
        )
        
        # Use provided or default metadata
        super().__init__(metadata=metadata or default_metadata)
```

3. Implement the `generate()` Method
```python
async def generate(self, **kwargs):
    """
    Implement your tool's core logic here
    
    Args:
        **kwargs: Flexible input parameters
    
    Returns:
        Result of tool's operation
    """
    try:
        # Your tool's implementation
        result = await self._perform_task(**kwargs)
        return result
    except Exception as e:
        # Handle and log errors
        self.logger.error(f"Tool execution error: {e}")
        raise
```

4. Register Your Tool
```python
from grami_ai.tools.base import tool_registry

# Create and register the tool
my_tool = MyCustomTool()
tool_registry.register_tool(my_tool)
```

## Built-in Tools

### Content Generation Tool
- Generate social media content
- Supports multiple platforms
- Customizable by platform and niche

### Web Search Tool
- Perform web searches using Google Custom Search
- Configurable search parameters
- Returns structured search results

## Tool Best Practices

1. **Keep Tools Focused**
   - Each tool should have a single, clear purpose
   - Avoid complex, multi-purpose tools

2. **Use Metadata Effectively**
   - Provide comprehensive tool descriptions
   - Include performance and reliability scores
   - Add relevant tags

3. **Error Handling**
   - Always implement robust error handling
   - Use logging to track tool performance
   - Provide meaningful error messages

4. **Async Design**
   - Leverage `async/await` for non-blocking operations
   - Minimize synchronous code within tools

## Advanced Tool Features

### Dynamic Configuration
- Tools can be configured via environment variables
- Support runtime parameter adjustment
- Implement flexible initialization

### Logging and Monitoring
- Integrated logging support
- Track tool performance and reliability
- Generate insights for tool improvement

## Troubleshooting

### Common Issues
- Async method not implemented
- Missing metadata
- Incorrect tool registration
- Configuration errors

### Debugging Tips
- Use detailed logging
- Check tool metadata
- Verify async method implementation
- Validate input parameters

## Example: Advanced Tool

```python
class AdvancedAnalysisTool(AsyncBaseTool):
    def __init__(self, api_key=None):
        metadata = ToolMetadata(
            name="advanced_analysis",
            description="Perform complex data analysis",
            category=ToolCategory.DATA_PROCESSING,
            tags=["analysis", "data_science"]
        )
        super().__init__(metadata=metadata)
        
        # Dynamic configuration
        self.api_key = api_key or os.getenv('ANALYSIS_API_KEY')
    
    async def generate(self, data, analysis_type='basic'):
        # Implement sophisticated analysis logic
        pass
```

## Conclusion

Tools are the heart of the Grami AI Framework. By following these guidelines, you can create powerful, flexible, and efficient tools that extend the framework's capabilities.
