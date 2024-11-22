import logging
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import google.generativeai as genai
import redis

class ConversationMemory:
    """
    Advanced conversation memory management with Redis and token-based prioritization
    """
    def __init__(self, redis_host='localhost', redis_port=6379, max_history_tokens=4000):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        self.max_history_tokens = max_history_tokens
        self.logger = logging.getLogger(__name__)

    def generate_chat_id(self) -> str:
        """Generate a unique chat identifier"""
        return str(uuid.uuid4())

    def store_message(self, chat_id: str, role: str, message: str):
        """
        Store a message in Redis with timestamp
        
        :param chat_id: Unique identifier for the conversation
        :param role: Role of the message sender (user/model)
        :param message: Message content
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        message_data = {
            'role': role,
            'content': message,
            'timestamp': timestamp
        }
        
        # Use Redis list to store conversation history
        self.redis_client.rpush(f'chat:{chat_id}:history', str(message_data))
        
        # Trim history to prevent unlimited growth
        self.redis_client.ltrim(f'chat:{chat_id}:history', -100, -1)

    def get_conversation_history(
        self, 
        chat_id: str, 
        model: Any = None, 
        max_messages: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Retrieve and prioritize conversation history
        
        :param chat_id: Unique identifier for the conversation
        :param model: LLM model for token counting
        :param max_messages: Maximum number of messages to retrieve
        :return: Prioritized conversation history
        """
        # Retrieve raw history from Redis
        raw_history = self.redis_client.lrange(f'chat:{chat_id}:history', -max_messages, -1)
        
        # Convert byte strings to dictionaries
        history = [eval(msg.decode('utf-8')) for msg in raw_history]
        
        # If no model provided, return full history
        if not model:
            return history
        
        # Token-based prioritization
        return self._prioritize_messages(history, model)

    def _prioritize_messages(
        self, 
        history: List[Dict[str, Any]], 
        model: Any, 
        base_recent_count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Prioritize messages based on tokens and recency
        
        :param history: Full conversation history
        :param model: LLM model for token counting
        :param base_recent_count: Number of recent messages to always include
        :return: Prioritized message list
        """
        def count_tokens(messages: List[Dict[str, Any]]) -> int:
            transformed = [
                {"role": m["role"], "parts": [{"text": m["content"]}]} 
                for m in messages
            ]
            return model.count_tokens(transformed).total_tokens

        # Always include recent messages
        prioritized = history[-base_recent_count:]
        total_tokens = count_tokens(prioritized)

        # Add important messages from earlier in the conversation
        for msg in reversed(history[:-base_recent_count]):
            msg_tokens = count_tokens([msg])
            if total_tokens + msg_tokens <= self.max_history_tokens:
                prioritized.insert(0, msg)
                total_tokens += msg_tokens
            else:
                break

        return prioritized


class GramiChatInterface:
    """
    Comprehensive Chat Interface for Grami AI Framework
    """
    def __init__(
        self, 
        api_key: str, 
        model_name: str = 'gemini-1.5-pro',
        memory_manager: Optional[ConversationMemory] = None
    ):
        # Configure Generative AI
        genai.configure(api_key=api_key)
        
        # Initialize model
        self.model = self._configure_model(model_name)
        
        # Memory management
        self.memory = memory_manager or ConversationMemory()
        
        # Logging
        self.logger = logging.getLogger(__name__)

    def _configure_model(self, model_name: str):
        """
        Configure Generative Model with safety and generation settings
        
        :param model_name: Name of the Generative AI model
        :return: Configured Generative Model
        """
        return genai.GenerativeModel(
            model_name=model_name,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
            generation_config=genai.GenerationConfig(
                max_output_tokens=4000,
                temperature=0.5,
                top_p=0.95,
                top_k=64,
                response_mime_type="text/plain",
            )
        )

    def start_chat(self, system_prompt: Optional[str] = None) -> str:
        """
        Start a new chat session
        
        :param system_prompt: Optional system-level instruction
        :return: Generated chat ID
        """
        chat_id = self.memory.generate_chat_id()
        
        if system_prompt:
            self.memory.store_message(chat_id, 'system', system_prompt)
        
        return chat_id

    def send_message(self, chat_id: str, message: str) -> Dict[str, Any]:
        """
        Send a message and get a response
        
        :param chat_id: Unique chat identifier
        :param message: User's message
        :return: Response dictionary with message details
        """
        # Store user message
        self.memory.store_message(chat_id, 'user', message)
        
        # Retrieve conversation history
        history = self.memory.get_conversation_history(chat_id, self.model)
        
        # Start chat with history
        convo = self.model.start_chat(history=history)
        
        # Send message
        response = convo.send_message(message)
        
        # Store model's response
        self.memory.store_message(chat_id, 'model', response.text)
        
        return {
            'chat_id': chat_id,
            'message': response.text,
            'tokens': {
                'total': response.usage_metadata.total_token_count,
                'prompt': response.usage_metadata.prompt_token_count,
                'candidates': response.usage_metadata.candidates_token_count
            }
        }

# Example Usage
def main():
    # Initialize chat interface
    chat = GramiChatInterface(
        api_key='YOUR_GEMINI_API_KEY',
        model_name='gemini-1.5-pro'
    )
    
    # Start a new chat
    chat_id = chat.start_chat(
        system_prompt="You are a helpful AI assistant focused on providing clear and concise answers."
    )
    
    # Send messages
    response1 = chat.send_message(chat_id, "Hello, how are you today?")
    print(response1)
    
    response2 = chat.send_message(chat_id, "Can you help me understand quantum computing?")
    print(response2)

if __name__ == '__main__':
    main()
