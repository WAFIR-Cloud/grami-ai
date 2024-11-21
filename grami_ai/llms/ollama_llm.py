import asyncio
import json
import requests
from typing import Any, Dict, List, Optional

from grami_ai.llms.base_llm import BaseLLMProvider


class OllamaLLMProvider(BaseLLMProvider):
    """
    Concrete implementation of the BaseLLMProvider for OLLAMA (LLAMA) integration.
    
    This provider uses the OLLAMA local API to interact with LLAMA models.
    """

    def __init__(
            self,
            api_key: Optional[str] = None,  # Optional for local OLLAMA
            model_name: str = "llama3.2",  # Default LLAMA model
            system_instruction: Optional[str] = "You are a helpful AI assistant.",
            generation_config: Optional[Dict[str, Any]] = None,
            safety_settings: Optional[List[Dict[str, str]]] = None,
            base_url: str = "http://localhost:11434"  # Default OLLAMA API endpoint
    ):
        """
        Initialize the OLLAMA LLM provider.
        
        Args:
            api_key (Optional[str]): Not required for local OLLAMA, kept for interface compatibility
            model_name (str, optional): Name of the LLAMA model to use. Defaults to "llama2".
            system_instruction (Optional[str], optional): System-level instruction. 
            generation_config (Optional[Dict[str, Any]], optional): Generation configuration.
            safety_settings (Optional[List[Dict[str, str]]], optional): Safety settings (not used in OLLAMA).
            base_url (str, optional): Base URL for OLLAMA API. Defaults to local endpoint.
        """
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.base_url = base_url

        # Default generation config if not provided
        self.generation_config = generation_config or {
            "temperature": 0.7,
            "max_tokens": 4096
        }

        # Validate model exists
        self._validate_model()

    def _validate_model(self):
        """
        Validate that the specified model is available in OLLAMA.
        
        Raises:
            ValueError: If the model is not found
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get('models', [])

            # Check if model exists
            model_exists = any(
                model['name'].startswith(self.model_name)
                for model in models
            )

            if not model_exists:
                raise ValueError(f"Model {self.model_name} not found in OLLAMA. Available models: {models}")
        except requests.RequestException as e:
            raise ConnectionError(f"Unable to connect to OLLAMA API: {e}")

    async def start_chat(self, tools: Optional[List[Any]] = None):
        """
        Start a new chat session with OLLAMA.
        
        Args:
            tools (Optional[List[Any]], optional): Not used in OLLAMA, kept for interface compatibility
        
        Returns:
            Dict: A conversation context dictionary
        """
        # For OLLAMA, we'll just return a context dictionary
        return {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self.system_instruction}
            ]
        }

    async def send_message(self, conversation, message: str, tools: Optional[List[Any]] = None):
        """
        Send a message to the OLLAMA API.
        
        Args:
            conversation (Dict): Conversation context
            message (str): Message to send
            tools (Optional[List[Any]], optional): Not used in OLLAMA, kept for interface compatibility
        
        Returns:
            str: The model's response
        """
        # Add the new user message to the conversation
        conversation['messages'].append({"role": "user", "content": message})

        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "messages": conversation['messages'],
            **self.generation_config
        }

        # Make the API call
        try:
            response = await self._async_chat_request(payload)

            # Add the model's response to the conversation
            conversation['messages'].append({"role": "assistant", "content": response})

            return response
        except Exception as e:
            raise RuntimeError(f"Error communicating with OLLAMA: {e}")

    async def _async_chat_request(self, payload: Dict[str, Any]) -> str:
        """
        Async wrapper for OLLAMA chat request.
        
        Args:
            payload (Dict[str, Any]): Request payload
        
        Returns:
            str: Model's response
        """
        def sync_request():
            try:
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                
                # Parse the response directly
                response_data = response.json()
                return response_data.get('message', {}).get('content', '')
            except requests.RequestException as e:
                raise ConnectionError(f"Unable to connect to OLLAMA API: {e}")
        
        # Use asyncio to run the sync request in a thread pool
        return await asyncio.to_thread(sync_request)

    def format_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format conversation history for OLLAMA's requirements.
        
        Args:
            history (List[Dict[str, Any]]): Conversation history to format
        
        Returns:
            List[Dict[str, Any]]: Formatted conversation history
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]
