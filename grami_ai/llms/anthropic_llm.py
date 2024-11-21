"""
Anthropic (Claude) LLM provider implementation for GRAMI AI.
"""

from typing import Dict, Any, Optional, List
import os
import json
import asyncio
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.core.config import settings
from grami_ai.core.constants import Role
from grami_ai.llms.prompts import Message, MessageRole, FORMATTERS
from grami_ai.core.logging import logger

class AnthropicLLMProvider(BaseLLMProvider):
    """Anthropic (Claude) LLM provider implementation."""
    
    def __init__(
        self,
        model_name: str = "claude-2.1",
        api_key: Optional[str] = None,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Anthropic provider.
        
        Args:
            model_name: Anthropic model to use (e.g., "claude-2.1", "claude-instant-1")
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            system_instruction: System prompt for the conversation
            generation_config: Model generation parameters
        """
        super().__init__()
        
        self.model_name = model_name
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY") or settings.anthropic_api_key
        if not self.api_key:
            raise ValueError("Anthropic API key not found")
            
        self.system_instruction = FORMATTERS["anthropic"].format_system_prompt(
            system_instruction or "You are Claude, a helpful AI assistant."
        )
        
        self.generation_config = generation_config or {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0
        }
        
        # Initialize client and formatter
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.formatter = FORMATTERS["anthropic"]
        
        # Initialize conversation history
        self.messages = []
        if self.system_instruction:
            self.messages.append(Message(
                role=MessageRole.SYSTEM,
                content=self.system_instruction
            ))
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def send_message(
        self,
        message: str,
        role: Role = Role.USER,
        **kwargs
    ) -> str:
        """Send a message to the Anthropic model.
        
        Args:
            message: The message to send
            role: Role of the message sender (user/assistant/system)
            **kwargs: Additional parameters to pass to the model
        
        Returns:
            The model's response text
        """
        try:
            # Add message to history
            self.messages.append(Message(
                role=MessageRole(role.value),
                content=message
            ))
            
            # Format messages for Anthropic API
            formatted_messages = self.formatter.format_messages(self.messages)
            
            # Get response from Anthropic
            response = await self.client.messages.create(
                model=self.model_name,
                messages=formatted_messages,
                **{**self.generation_config, **kwargs}
            )
            
            # Extract and store response
            assistant_message = response.content[0].text
            self.messages.append(Message(
                role=MessageRole.ASSISTANT,
                content=assistant_message
            ))
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error in Anthropic API call: {str(e)}")
            raise
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for the input text.
        
        Note: Anthropic does not currently provide an embeddings API.
        This is a placeholder that raises NotImplementedError.
        
        Args:
            text: Input text to get embeddings for
        
        Raises:
            NotImplementedError: Anthropic does not provide embeddings
        """
        raise NotImplementedError(
            "Anthropic does not currently provide an embeddings API. "
            "Please use a different provider for embeddings."
        )
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.messages = []
        if self.system_instruction:
            self.messages.append(Message(
                role=MessageRole.SYSTEM,
                content=self.system_instruction
            ))
