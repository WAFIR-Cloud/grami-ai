import os
import asyncio
from typing import Optional, Dict, Any, List

from grami_ai.llms.base import BaseLLMProvider, Message, MessageRole, ToolDefinition
import google.generativeai as genai

class GeminiLLMProvider(BaseLLMProvider):
    """
    Gemini LLM Provider for Grami AI Framework
    
    Supports async text generation using Google's Gemini AI
    """
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model_name: str = 'gemini-pro',
        system_instruction: Optional[str] = None,
        tool_definitions: Optional[List[ToolDefinition]] = None,
        **kwargs
    ):
        """
        Initialize Gemini LLM Provider
        
        Args:
            api_key: Google AI API key (defaults to GOOGLE_API_KEY env var)
            model_name: Gemini model to use
            system_instruction: Initial context/personality
            tool_definitions: Predefined tools/functions
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            system_instruction=system_instruction,
            tool_definitions=tool_definitions
        )
        
        if not self.api_key:
            self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Google AI API key must be provided via 'api_key' "
                "or GOOGLE_API_KEY environment variable"
            )
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Select model
        self.model = genai.GenerativeModel(model_name)
        
        # Additional configuration
        self.config = kwargs.get('config', {
            'temperature': 0.7,
            'top_p': 0.9,
            'max_output_tokens': 2048
        })
        
        # Initialize chat
        self.chat = None
        self.messages = []
        
        # Add system instruction if provided
        if self.system_instruction:
            self.messages.append(Message(
                role=MessageRole.SYSTEM,
                content=self.system_instruction
            ))
    
    async def start_chat(
        self,
        tools: Optional[List[ToolDefinition]] = None,
        **provider_specific_params
    ):
        """Start a new chat session."""
        self.chat = self.model.start_chat()
        self.messages = []
        
        # Add system instruction if provided
        if self.system_instruction:
            self.messages.append(Message(
                role=MessageRole.SYSTEM,
                content=self.system_instruction
            ))
            
        # Register tools if provided
        if tools:
            for tool in tools:
                self.register_tool(tool)
    
    async def send_message(
        self,
        conversation: Any,
        message: str,
        tools: Optional[List[ToolDefinition]] = None,
        **provider_specific_params
    ) -> str:
        """Send a message and get response."""
        # Add user message to history
        self.messages.append(Message(
            role=MessageRole.USER,
            content=message
        ))
        
        # Prepare full context
        full_context = []
        for msg in self.messages:
            if msg.role == MessageRole.SYSTEM:
                full_context.append(f"System: {msg.content}")
            elif msg.role == MessageRole.USER:
                full_context.append(f"User: {msg.content}")
            elif msg.role == MessageRole.ASSISTANT:
                full_context.append(f"Assistant: {msg.content}")
        
        # Generate response
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(
                "\n".join(full_context),
                generation_config=self.config
            )
        )
        
        # Add assistant response to history
        assistant_message = response.text
        self.messages.append(Message(
            role=MessageRole.ASSISTANT,
            content=assistant_message
        ))
        
        return assistant_message
    
    def register_tool(self, tool: ToolDefinition):
        """Register a new tool."""
        self.tools.append(tool)
    
    def _prepare_tools_for_provider(self, tools: List[ToolDefinition]) -> List[Dict[str, Any]]:
        """Convert tools to Gemini-specific format."""
        return [tool.to_provider_format('gemini') for tool in tools]
    
    async def generate(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        Async text generation using Gemini
        
        Args:
            prompt: User prompt
            system_instruction: Optional system-level instructions
            context: Optional context dictionary
            **kwargs: Additional generation parameters
        
        Returns:
            Generated text response
        """
        # Merge default config with passed kwargs
        generation_config = {**self.config, **kwargs.get('config', {})}
        
        # Prepare full prompt with system instruction and context
        full_prompt = []
        if system_instruction:
            full_prompt.append(system_instruction)
        
        if context:
            context_str = "\n".join([
                f"{k}: {v}" for k, v in context.items()
            ])
            full_prompt.append(f"Context:\n{context_str}")
        
        full_prompt.append(prompt)
        
        # Run generation in executor to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: self.model.generate_content(
                "\n".join(full_prompt), 
                generation_config=generation_config
            )
        )
        
        return response.text
    
    async def stream_generate(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Stream text generation
        
        Args:
            prompt: User prompt
            system_instruction: Optional system-level instructions
            context: Optional context dictionary
            **kwargs: Additional generation parameters
        
        Yields:
            Streaming text chunks
        """
        # Similar to generate, but uses streaming
        pass  # TODO: Implement streaming generation
