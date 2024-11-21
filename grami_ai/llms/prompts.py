"""
Provider-specific prompt formatting and templates.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass

class MessageRole(str, Enum):
    """Message roles across different providers."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

@dataclass
class Message:
    """Unified message format for all providers."""
    role: MessageRole
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None

class PromptFormatter:
    """Base class for provider-specific prompt formatting."""
    
    def format_messages(self, messages: List[Message]) -> Any:
        """Format messages for provider API."""
        raise NotImplementedError
    
    def format_system_prompt(self, instruction: str) -> str:
        """Format system instruction."""
        return instruction

class OpenAIPromptFormatter(PromptFormatter):
    """OpenAI-specific prompt formatting."""
    
    def format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Format messages for OpenAI chat API."""
        formatted = []
        for msg in messages:
            message = {"role": msg.role, "content": msg.content}
            if msg.name:
                message["name"] = msg.name
            if msg.function_call:
                message["function_call"] = msg.function_call
            formatted.append(message)
        return formatted

class AnthropicPromptFormatter(PromptFormatter):
    """Anthropic-specific prompt formatting."""
    
    def format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Format messages for Anthropic API."""
        formatted = []
        system_message = None
        
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_message = msg.content
                continue
                
            content = msg.content
            if system_message and len(formatted) == 0 and msg.role == MessageRole.USER:
                # Prepend system message to first user message
                content = f"{system_message}\n\n{content}"
                system_message = None
                
            formatted.append({
                "role": "user" if msg.role == MessageRole.USER else "assistant",
                "content": content
            })
        
        return formatted
    
    def format_system_prompt(self, instruction: str) -> str:
        """Format system instruction for Anthropic.
        
        Note: Anthropic doesn't support system messages directly,
        so we'll prepend it to the first user message.
        """
        return f"Instructions: {instruction}\n\nAssistant: I understand and will follow these instructions."

class GeminiPromptFormatter(PromptFormatter):
    """Google Gemini-specific prompt formatting."""
    
    def format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Format messages for Gemini API."""
        formatted = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                # Gemini doesn't have system messages, add as user
                formatted.append({
                    "role": "user",
                    "parts": [{"text": f"System: {msg.content}"}]
                })
            else:
                formatted.append({
                    "role": "user" if msg.role == MessageRole.USER else "model",
                    "parts": [{"text": msg.content}]
                })
        return formatted
    
    def format_system_prompt(self, instruction: str) -> str:
        """Format system instruction for Gemini."""
        return f"You are an AI assistant. {instruction}"

class OllamaPromptFormatter(PromptFormatter):
    """Ollama-specific prompt formatting."""
    
    def format_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Format messages for Ollama API."""
        formatted = []
        system_message = None
        
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                system_message = msg.content
                continue
                
            formatted.append({
                "role": msg.role,
                "content": msg.content
            })
            
        if system_message:
            # Add system message as metadata
            formatted.insert(0, {
                "role": "system",
                "content": system_message
            })
            
        return formatted

# Provider-specific formatters
FORMATTERS = {
    "openai": OpenAIPromptFormatter(),
    "anthropic": AnthropicPromptFormatter(),
    "gemini": GeminiPromptFormatter(),
    "ollama": OllamaPromptFormatter()
}
