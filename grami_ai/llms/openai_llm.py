"""
OpenAI LLM provider implementation for GRAMI AI.
"""

from typing import Dict, Any, Optional, List
import os
import json
import logging
import asyncio
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from grami_ai.llms.base_llm import BaseLLMProvider
from grami_ai.core.config import settings
from grami_ai.core.constants import Role
from grami_ai.llms.prompts import Message, MessageRole, FORMATTERS

logger = logging.getLogger(__name__)

class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        system_instruction: Optional[str] = None,
        generation_config: Optional[Dict[str, Any]] = None
    ):
        """Initialize OpenAI provider.
        
        Args:
            model_name: OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4")
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            system_instruction: System prompt for the conversation
            generation_config: Model generation parameters
        """
        super().__init__()
        
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
            
        self.system_instruction = FORMATTERS["openai"].format_system_prompt(
            system_instruction or "You are a helpful AI assistant."
        )
        
        self.generation_config = generation_config or {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        # Initialize client and formatter
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.formatter = FORMATTERS["openai"]
        
        # Initialize conversation history
        self.messages = [
            Message(role=MessageRole.SYSTEM, content=self.system_instruction)
        ]
    
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
        """Send a message to the OpenAI model.
        
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
            
            # Format messages for OpenAI API
            formatted_messages = self.formatter.format_messages(self.messages)
            
            # Get response from OpenAI
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=formatted_messages,
                **{**self.generation_config, **kwargs}
            )
            
            # Extract and store response
            assistant_message = response.choices[0].message.content
            self.messages.append(Message(
                role=MessageRole.ASSISTANT,
                content=assistant_message
            ))
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for the input text.
        
        Args:
            text: Input text to get embeddings for
        
        Returns:
            List of embedding values
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            raise
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.messages = [
            Message(role=MessageRole.SYSTEM, content=self.system_instruction)
        ]
