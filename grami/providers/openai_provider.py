from typing import Any, Dict, List
import openai
from ..core.base import BaseLLMProvider, BaseTool

class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI LLM Provider with native function calling support.
    
    Demonstrates how to implement tool execution using OpenAI's function calling API.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI provider.
        
        :param api_key: OpenAI API key
        :param model: OpenAI model to use
        """
        super().__init__()
        openai.api_key = api_key
        self.model = model
        self._conversation_history = []
    
    def initialize_chat(self, system_instructions: str, context: Dict = None):
        """
        Initialize chat with system instructions.
        
        :param system_instructions: Initial system prompt
        :param context: Optional additional context
        """
        self._conversation_history = [
            {"role": "system", "content": system_instructions}
        ]
    
    def send_message(self, message: str, context: Dict = None) -> str:
        """
        Send a message and get a response.
        
        :param message: User message
        :param context: Optional context
        :return: LLM response
        """
        self._conversation_history.append({"role": "user", "content": message})
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self._conversation_history
        )
        
        assistant_response = response.choices[0].message.content
        self._conversation_history.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    
    def stream_message(self, message: str, context: Dict = None):
        """
        Stream message response.
        
        :param message: User message
        :param context: Optional context
        :yield: Streamed response tokens
        """
        self._conversation_history.append({"role": "user", "content": message})
        
        for chunk in openai.ChatCompletion.create(
            model=self.model,
            messages=self._conversation_history,
            stream=True
        ):
            if chunk.choices[0].delta.get("content"):
                yield chunk.choices[0].delta.content
    
    def execute_tool(self, tool: BaseTool, *args, **kwargs) -> Any:
        """
        Execute a tool using OpenAI's function calling mechanism.
        
        :param tool: Tool to execute
        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :return: Tool execution result
        """
        # Convert tool to OpenAI function definition
        function_def = {
            "name": tool.__class__.__name__,
            "description": tool.__doc__ or "A custom tool for the AI agent",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        
        # Dynamically generate function parameters based on tool's signature
        import inspect
        signature = inspect.signature(tool.execute)
        for param_name, param in signature.parameters.items():
            if param_name not in ['self', 'args', 'kwargs']:
                param_type = "string"  # Default to string, can be more sophisticated
                function_def["parameters"]["properties"][param_name] = {
                    "type": param_type,
                    "description": f"Parameter {param_name}"
                }
                if param.default == inspect.Parameter.empty:
                    function_def["parameters"]["required"].append(param_name)
        
        # Call OpenAI with function definition
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self._conversation_history + [
                {
                    "role": "user", 
                    "content": "Please help me execute this tool with the given parameters."
                }
            ],
            functions=[function_def],
            function_call={"name": tool.__class__.__name__}
        )
        
        # Extract function arguments from the response
        function_call = response.choices[0].message.get("function_call")
        if function_call:
            import json
            try:
                # Parse function arguments
                func_args = json.loads(function_call.arguments)
                
                # Execute the tool with parsed arguments
                return tool.execute(**func_args)
            except Exception as e:
                # Fallback to direct execution if function call parsing fails
                return tool.execute(*args, **kwargs)
        
        # Fallback to direct tool execution
        return tool.execute(*args, **kwargs)
