from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

class MessageRole(Enum):
    """
    Standardized message roles across different LLM providers
    
    Provides a unified representation of conversation roles
    that can be mapped to provider-specific implementations
    """
    SYSTEM = auto()    # System-level instructions
    USER = auto()      # User input
    ASSISTANT = auto() # AI response
    FUNCTION = auto()  # Function/tool call result
    CONTEXT = auto()   # Contextual information
    MEMORY = auto()    # Retrieved memory context

@dataclass
class Message:
    """
    Comprehensive message representation
    
    Supports rich metadata and provider-agnostic design
    """
    content: str
    role: MessageRole
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_provider_format(self, provider: str) -> Dict[str, Any]:
        """
        Convert message to provider-specific format
        
        Supports mapping between different LLM conversation paradigms
        """
        provider_roles = {
            'gemini': {
                MessageRole.SYSTEM: 'model',
                MessageRole.USER: 'user',
                MessageRole.ASSISTANT: 'model',
                MessageRole.FUNCTION: 'function',
                MessageRole.CONTEXT: 'user',
                MessageRole.MEMORY: 'user'
            },
            'openai': {
                MessageRole.SYSTEM: 'system',
                MessageRole.USER: 'user',
                MessageRole.ASSISTANT: 'assistant',
                MessageRole.FUNCTION: 'function',
                MessageRole.CONTEXT: 'system',
                MessageRole.MEMORY: 'system'
            },
            'anthropic': {
                MessageRole.SYSTEM: 'system',
                MessageRole.USER: 'user',
                MessageRole.ASSISTANT: 'assistant',
                MessageRole.FUNCTION: 'user',
                MessageRole.CONTEXT: 'system',
                MessageRole.MEMORY: 'system'
            },
            'ollama': {
                MessageRole.SYSTEM: 'system',
                MessageRole.USER: 'user',
                MessageRole.ASSISTANT: 'assistant',
                MessageRole.FUNCTION: 'user',
                MessageRole.CONTEXT: 'system',
                MessageRole.MEMORY: 'system'
            }
        }
        
        return {
            'role': provider_roles.get(provider.lower(), {}).get(self.role, 'user'),
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

@dataclass
class ToolDefinition:
    """
    Standardized tool definition for cross-LLM compatibility
    
    Provides a generic representation of tools/functions 
    that can be adapted to different LLM providers' specifications
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    
    def to_provider_format(self, provider: str) -> Dict[str, Any]:
        """
        Convert tool definition to provider-specific format
        
        Supports:
        - Google Gemini
        - OpenAI
        - Anthropic
        - Ollama
        """
        formats = {
            'gemini': self._to_gemini_format(),
            'openai': self._to_openai_format(),
            'anthropic': self._to_anthropic_format(),
            'ollama': self._to_ollama_format()
        }
        return formats.get(provider.lower(), {})
    
    def _to_gemini_format(self) -> Dict[str, Any]:
        """Gemini-specific tool definition"""
        return {
            'function_declarations': [{
                'name': self.name,
                'description': self.description,
                'parameters': {
                    'type': 'OBJECT',
                    'properties': {
                        k: {'type': v.get('type', 'STRING')} 
                        for k, v in self.parameters.items()
                    }
                }
            }]
        }
    
    def _to_openai_format(self) -> Dict[str, Any]:
        """OpenAI function calling format"""
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': {
                    'type': 'object',
                    'properties': self.parameters
                }
            }
        }
    
    def _to_anthropic_format(self) -> Dict[str, Any]:
        """Anthropic tool definition"""
        return {
            'name': self.name,
            'description': self.description,
            'input_schema': {
                'type': 'object',
                'properties': self.parameters
            }
        }
    
    def _to_ollama_format(self) -> Dict[str, Any]:
        """Ollama tool definition"""
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': self.parameters
            }
        }

class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers with flexible tool integration
    """
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model_name: str = 'default',
        system_instruction: Optional[str] = None,
        tool_definitions: Optional[List[ToolDefinition]] = None
    ):
        """
        Initialize LLM provider with flexible configuration
        
        Args:
            api_key: Optional API key for provider
            model_name: Specific model variant
            system_instruction: Initial context/personality
            tool_definitions: Predefined tools/functions
        """
        self.api_key = api_key
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.tools = tool_definitions or []
    
    @abstractmethod
    async def start_chat(
        self, 
        tools: Optional[List[ToolDefinition]] = None,
        **provider_specific_params
    ) -> Any:
        """
        Start a new chat session with provider-specific configurations
        
        Allows dynamic tool injection and provider-specific settings
        """
        pass
    
    @abstractmethod
    async def send_message(
        self, 
        conversation: Any, 
        message: str, 
        tools: Optional[List[ToolDefinition]] = None,
        **provider_specific_params
    ) -> str:
        """
        Send a message with flexible tool handling
        
        Supports:
        - Dynamic tool injection
        - Provider-specific message sending
        - Automatic or manual function calling
        """
        pass
    
    def register_tool(self, tool: ToolDefinition) -> None:
        """
        Dynamically register a new tool/function
        
        Allows runtime tool addition to the agent's toolkit
        """
        self.tools.append(tool)
    
    def _prepare_tools_for_provider(self, tools: List[ToolDefinition]) -> Any:
        """
        Convert tools to provider-specific format
        
        Abstract method to be implemented by each provider
        """
        raise NotImplementedError("Subclasses must implement tool preparation")
