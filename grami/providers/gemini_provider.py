import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerationConfig
import asyncio
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Union, Any, Callable
import logging
import uuid

class GeminiProvider:
    """Provider for Google's Gemini API."""

    # Default safety settings
    DEFAULT_SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        generation_config: Optional[Dict] = None,
        safety_settings: Optional[List[Dict[str, str]]] = None,
    ):
        """Initialize the Gemini provider with model configuration.
        
        :param api_key: Gemini API key
        :param model: Model name to use (default: gemini-pro)
        :param generation_config: Optional generation configuration for controlling model behavior
        :param safety_settings: Optional custom safety settings to override defaults
        """
        genai.configure(api_key=api_key)
        
        # Use provided safety settings or defaults
        model_safety_settings = safety_settings or self.DEFAULT_SAFETY_SETTINGS
        
        # Initialize model with provided configs
        self._model = GenerativeModel(
            model,
            generation_config=GenerationConfig(**(generation_config or {})),
            safety_settings=model_safety_settings
        )
        self._chat = None
        self._history = []
        self._memory_provider = None

    def _transform_history_for_gemini(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform history into Gemini's format."""
        transformed = []
        for msg in history:
            if msg["role"] not in ["user", "model"]:
                continue
            content = msg["content"] if isinstance(msg["content"], str) else msg["content"].get("text", "")
            transformed.append({
                "role": msg["role"],
                "parts": [{"text": content}]
            })
        return transformed

    def _prioritize_messages(self, history: List[Dict[str, Any]], max_tokens: int = 1500, base_recent: int = 30) -> List[Dict[str, Any]]:
        """Prioritize messages based on recency and token limits."""
        if not history:
            return []

        # Always keep most recent messages
        prioritized = history[-base_recent:]
        
        # Count tokens for recent messages
        transformed = self._transform_history_for_gemini(prioritized)
        total_tokens = self._model.count_tokens(transformed).total_tokens
        
        # Add older messages if space allows
        for msg in reversed(history[:-base_recent]):
            msg_tokens = self._model.count_tokens(self._transform_history_for_gemini([msg])).total_tokens
            if total_tokens + msg_tokens <= max_tokens:
                prioritized.insert(0, msg)
                total_tokens += msg_tokens
            else:
                break
                
        return prioritized

    def set_history(self, history: List[Dict[str, Any]]) -> None:
        """Set the conversation history."""
        self._history = history
        if self._chat and history:
            transformed = self._transform_history_for_gemini(history)
            self._chat.history = transformed

    async def send_message(
        self,
        message: Union[str, Dict[str, str]],
        context: Optional[Dict] = None
    ) -> str:
        """Send a message and get a response."""
        message_content = message if isinstance(message, str) else message.get('content', message.get('text', ''))
            
        try:
            # Initialize chat if needed
            if not self._chat:
                transformed_history = self._transform_history_for_gemini(self._history)
                self._chat = self._model.start_chat(history=transformed_history)
            else:
                # Update chat history
                transformed = self._transform_history_for_gemini(self._history)
                self._chat.history = transformed

            # Store user message
            user_message = {"role": "user", "content": message_content}
            self._history.append(user_message)
            if self._memory_provider:
                await self._memory_provider.add_message(role="user", content=message_content)

            # Try different prompts if we get a RECITATION error
            prompts = [
                message_content,
                f"Please provide a natural response to: {message_content}",
                f"Respond naturally to this message: {message_content}",
                f"As a helpful assistant, please respond to: {message_content}"
            ]
            
            response_text = None
            last_error = None
            
            for prompt in prompts:
                try:
                    response = await self._chat.send_message_async(prompt)
                    if hasattr(response, 'text'):
                        response_text = response.text
                        break
                except Exception as e:
                    last_error = e
                    if "RECITATION" not in str(e):
                        raise
                    continue
            
            if response_text is None:
                if last_error:
                    raise last_error
                raise Exception("Failed to get a valid response after multiple attempts")

            # Store model response
            model_message = {"role": "model", "content": response_text}
            self._history.append(model_message)
            if self._memory_provider:
                await self._memory_provider.add_message(role="assistant", content=response_text)

            return response_text
            
        except Exception as e:
            logging.error(f"Error in send_message: {str(e)}")
            raise

    async def stream_message(
        self,
        message: Union[str, Dict[str, str]],
        context: Optional[Dict] = None
    ):
        """Stream a message response."""
        message_content = message if isinstance(message, str) else message.get('content', message.get('text', ''))

        try:
            # Initialize chat if needed
            if not self._chat:
                transformed_history = self._transform_history_for_gemini(self._history)
                self._chat = self._model.start_chat(history=transformed_history)
            else:
                # Update chat history
                transformed = self._transform_history_for_gemini(self._history)
                self._chat.history = transformed

            # Store user message
            user_message = {"role": "user", "content": message_content}
            self._history.append(user_message)
            if self._memory_provider:
                await self._memory_provider.add_message(role="user", content=message_content)

            # Send message with streaming enabled
            response = await self._chat.send_message_async(message_content, stream=True)
            full_response = []

            # Stream chunks and collect them
            async for chunk in response:
                chunk_text = chunk.text
                full_response.append(chunk_text)
                yield chunk_text

            # Store complete response after all chunks are received
            complete_response = "".join(full_response)
            model_message = {"role": "model", "content": complete_response}
            self._history.append(model_message)
            
            # Add to memory only after all chunks are received
            if self._memory_provider:
                await self._memory_provider.add_message(role="assistant", content=complete_response)

        except Exception as e:
            logging.error(f"Error in stream_message: {str(e)}")
            raise

    def get_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history.
        
        :return: List of message dictionaries
        """
        return self._history.copy()

    async def _process_function_calls(self, contents: List[Dict], is_streaming: bool = False) -> tuple:
        """
        Process function calls in the model's response.
        
        :param contents: Conversation contents
        :param is_streaming: Whether the response is streaming or not
        :return: Tuple of updated contents and final response text
        """
        # Generate content with tools
        response = self._model.generate_content(
            contents=contents,
            stream=False  # Always use non-streaming for predictable function call handling
        )
        
        # Check if the response contains a function call
        function_calls = [
            part.function_call 
            for part in response.candidates[0].content.parts 
            if part.function_call
        ]
        
        # Process function calls manually
        for function_call in function_calls:
            # Execute the function call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            # Find and execute the corresponding function
            if hasattr(self, '_tools') and function_name in self._tools:
                tool = self._tools[function_name]
                try:
                    # Handle both sync and async functions
                    if asyncio.iscoroutinefunction(tool):
                        tool_result = await tool(**function_args)
                    else:
                        tool_result = tool(**function_args)
                    
                    # Create a function response part
                    function_response = genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name, 
                            response={"result": tool_result}
                        )
                    )
                    
                    # Add function response to the conversation
                    contents.append({'role': 'model', 'parts': [function_call]})
                    contents.append({'role': 'user', 'parts': [function_response]})
                except Exception as e:
                    logging.error(f"Error executing tool {function_name}: {e}")
        
        # Generate final response with function call results
        final_response = self._model.generate_content(
            contents=contents,
            stream=False
        )
        
        return contents, final_response.text

    def validate_configuration(self, **kwargs) -> None:
        """Validate the configuration parameters."""
        if not kwargs.get("api_key"):
            raise ValueError("API key is required")
        if not kwargs.get("model_name"):
            raise ValueError("Model name is required")

    def set_memory_provider(self, memory_provider: Any) -> None:
        """Set the memory provider for the LLM.
        
        Args:
            memory_provider: Memory provider instance
        """
        self._memory_provider = memory_provider

    def register_tools(self, tools: List[Callable]) -> None:
        """
        Register tools with the Gemini provider using native function calling.
        
        Args:
            tools: List of callable functions to be used as tools
        """
        # Convert Python functions to Gemini-compatible function declarations
        self._tools = {tool.__name__: tool for tool in tools}
        
        # Prepare tools for the Gemini model
        self._tool_declarations = tools
        
        # Reconfigure the model with the new tools
        try:
            # Attempt to preserve existing configuration
            safety_settings = getattr(self._model, '_safety_settings', None)
            generation_config = getattr(self._model, '_generation_config', None)
            
            self._model = genai.GenerativeModel(
                model_name=self._model.model_name,
                safety_settings=safety_settings,
                generation_config=generation_config,
                tools=self._tool_declarations
            )
        except Exception as e:
            # Fallback to default configuration if preservation fails
            logging.warning(f"Could not preserve model configuration: {e}")
            self._model = genai.GenerativeModel(
                model_name=self._model.model_name,
                tools=self._tool_declarations
            )
        
        logging.info(f"Registered {len(tools)} tools with GeminiProvider")