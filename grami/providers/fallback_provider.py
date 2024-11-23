from typing import Any, Dict
from ..core.base import BaseLLMProvider, BaseTool

class SimpleLLMProvider(BaseLLMProvider):
    """
    A simple, generic LLM provider that uses direct tool execution.
    
    This provider is useful for LLMs that do not have native function calling capabilities
    or when you want a basic, predictable tool execution method.
    """
    
    def __init__(self, model_name: str = "simple-llm"):
        """
        Initialize the simple LLM provider.
        
        :param model_name: Name of the LLM model
        """
        super().__init__()
        self.model_name = model_name
        self._conversation_history = []
    
    def initialize_chat(self, system_instructions: str, context: Dict = None):
        """
        Initialize chat with system instructions.
        
        :param system_instructions: Initial system prompt
        :param context: Optional additional context
        """
        self._conversation_history = [system_instructions]
    
    def send_message(self, message: str, context: Dict = None) -> str:
        """
        Simulate sending a message (for demonstration purposes).
        
        :param message: User message
        :param context: Optional context
        :return: A placeholder response
        """
        self._conversation_history.append(message)
        return f"Simulated response to: {message}"
    
    def stream_message(self, message: str, context: Dict = None):
        """
        Simulate streaming a message response.
        
        :param message: User message
        :param context: Optional context
        :yield: Simulated response tokens
        """
        yield f"Simulated streaming response to: {message}"
    
    def execute_tool(self, tool: BaseTool, *args, **kwargs) -> Any:
        """
        Execute a tool using a simple, direct method.
        
        This method provides a straightforward approach to tool execution:
        1. Validate input parameters
        2. Execute the tool directly with provided arguments
        3. Log the tool execution
        
        :param tool: Tool to execute
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Tool execution result
        """
        try:
            # Validate input parameters
            if not tool.validate_input(*args, **kwargs):
                raise ValueError("Invalid tool input parameters")
            
            # Execute the tool directly
            result = tool.execute(*args, **kwargs)
            
            # Optional: Log tool execution (can be expanded)
            print(f"Executed tool: {tool.__class__.__name__}")
            print(f"Arguments: {args}, {kwargs}")
            
            return result
        
        except Exception as e:
            # Handle any execution errors
            print(f"Error executing tool {tool.__class__.__name__}: {e}")
            raise
