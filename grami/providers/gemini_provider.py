import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types import GenerationConfig
import asyncio
import re

class GeminiProvider:
    """Provider for Google's Gemini API."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-pro"
    ):
        """Initialize the Gemini provider.
        
        Args:
            api_key: The API key for Gemini
            model_name: The model name to use
        """
        genai.configure(api_key=api_key)
        
        self._model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=4000,
                temperature=0.5,
                top_p=0.95,
                top_k=64,
                response_mime_type="text/plain",
            ),
        )
        
        self._chat = None
        self._conversation_history = []

    async def initialize_conversation(self, chat_id: Optional[str] = None) -> None:
        """Initialize a new conversation."""
        try:
            self._chat = self._model.start_chat()
            logging.info("Chat session initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing conversation: {str(e)}")
            raise

    async def send_message(self, message: Union[str, Dict[str, str]], context: Optional[Dict] = None) -> str:
        """
        Asynchronously send a message and get a response with manual function calling.
        
        :param message: User message (string or dictionary)
        :param context: Optional context
        :return: LLM's response as a string
        """
        # Ensure the model is configured with tools if available
        if hasattr(self, '_tool_declarations'):
            self._model = genai.GenerativeModel(
                model_name=self._model.model_name,
                tools=self._tool_declarations
            )
        
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {"role": "user", "content": message}
        else:
            message_payload = message
        
        try:
            # Prepare conversation history if it exists
            if hasattr(self, '_conversation_history') and self._conversation_history:
                contents = [
                    {'role': 'user', 'parts': [part['content']]} 
                    for part in self._conversation_history 
                    if part.get('role') == 'user'
                ]
                contents.append({'role': 'user', 'parts': [message_payload['content']]})
            else:
                contents = [{'role': 'user', 'parts': [message_payload['content']]}]
            
            # Process function calls
            contents, response_text = await self._process_function_calls(contents)
            
            # Store conversation history
            await self._store_conversation_memory(
                user_message=message_payload['content'], 
                model_response=response_text
            )
            
            return response_text
        except Exception as e:
            print(f"Error sending message: {e}")
            raise

    async def stream_message(self, message: Union[str, Dict[str, str]], context: Optional[Dict] = None):
        """
        Asynchronously stream a message response.
        
        :param message: User message (string or dictionary)
        :param context: Optional context
        :return: Streaming response object to be iterated by the caller
        """
        if not self._chat:
            await self.initialize_conversation()
        
        # Normalize message to dictionary format
        if isinstance(message, str):
            message_payload = {'content': message, 'role': 'user'}
        else:
            message_payload = message
        
        # Add current message to conversation history
        self._conversation_history.append(message_payload)
        
        try:
            # Prepare contents, handling empty conversation history
            contents = [
                {'role': 'user', 'parts': [part['content'] for part in self._conversation_history if part.get('role') == 'user']},
                {'role': 'model', 'parts': [part['content'] for part in self._conversation_history if part.get('role') == 'model']}
            ]
            
            # Remove empty lists to prevent API errors
            contents = [content for content in contents if content['parts']]
            
            # Add current message
            contents.append({'role': 'user', 'parts': [message_payload['content']]})
            
            # Process function calls
            contents, response_text = await self._process_function_calls(contents, is_streaming=True)
            
            # If response_text is a string, convert it to a list of tokens
            if isinstance(response_text, str):
                response_tokens = [response_text]
            else:
                response_tokens = response_text
            
            # Stream the tokens
            for token in response_tokens:
                yield token
            
            # Store conversation history
            await self._store_conversation_memory(
                user_message=message_payload['content'], 
                model_response=response_text if isinstance(response_text, str) else ''.join(response_text)
            )
        except Exception as e:
            logging.error(f"Error preparing streaming message: {e}")
            raise

    async def _process_function_calls(self, contents: List[Dict], is_streaming: bool = False) -> Tuple[List[Dict], str]:
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

    async def _store_conversation_memory(self, user_message: str, model_response: str) -> None:
        """
        Store a conversation turn in the memory provider.
        
        :param user_message: The user's input message
        :param model_response: The model's response
        """
        if not hasattr(self, '_memory_provider') or not self._memory_provider:
            return
        
        try:
            import uuid
            from datetime import datetime
            
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
            
            memory_entry = {
                "type": "conversation_turn",
                "user_message": {
                    "content": user_message,
                    "role": "user"
                },
                "model_response": {
                    "content": model_response,
                    "role": "model"
                },
                "timestamp": current_timestamp
            }
            
            await self._memory_provider.store(unique_key, memory_entry)
        except Exception as memory_error:
            logging.error(f"Failed to store memory: {memory_error}")

    def set_memory_provider(self, memory_provider):
        """
        Set the memory provider for the Gemini provider.
        
        :param memory_provider: Memory provider to use
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

    def get_conversation_history(self) -> List[Dict]:
        """
        Retrieve the current conversation history.
        
        :return: List of conversation turns
        """
        if hasattr(self, '_chat'):
            return [
                {
                    'role': content.role, 
                    'parts': [
                        {'text': part.text} if part.text else 
                        {'function_call': part.function_call} if part.function_call else 
                        {'function_response': part.function_response}
                        for part in content.parts
                    ]
                } 
                for content in self._chat.history
            ]
        return []

    def validate_configuration(self, **kwargs) -> None:
        """Validate the configuration parameters."""
        if not kwargs.get("api_key"):
            raise ValueError("API key is required")
        if not kwargs.get("model_name"):
            raise ValueError("Model name is required")