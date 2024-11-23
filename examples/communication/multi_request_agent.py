import asyncio
import json
import logging
import os
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv

from grami.agent import AsyncAgent
from grami.providers import GeminiProvider
from grami.core.base import BaseLLMProvider

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiRequestAgent(AsyncAgent):
    """
    Advanced WebSocket agent capable of handling multiple request types.
    """
    
    def __init__(
        self, 
        name: str = "Multi-Request Agent",
        llm: Optional[BaseLLMProvider] = None,
        system_instructions: Optional[str] = None
    ):
        """
        Initialize the multi-request agent.
        
        Args:
            name (str): Agent's name
            llm (Optional[BaseLLMProvider]): Language model provider
            system_instructions (Optional[str]): Initial system context
        """
        # Retrieve API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Use Gemini provider if no LLM is provided
        llm = llm or GeminiProvider(api_key=api_key)
        
        # Set default system instructions if not provided
        system_instructions = system_instructions or (
            "You are a versatile AI assistant capable of handling "
            "multiple types of requests across different domains."
        )
        
        # Initialize the parent AsyncAgent
        super().__init__(
            name=name, 
            llm=llm, 
            system_instructions=system_instructions
        )
    
    async def process_request(self, request_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process different types of requests.
        
        Args:
            request_type (str): Type of request to process
            payload (Dict[str, Any]): Request payload
        
        Returns:
            Dict[str, Any]: Processed response
        """
        logger.info(f"Processing {request_type} request: {payload}")
        
        try:
            if request_type == 'text_generation':
                return await self._handle_text_generation(payload)
            elif request_type == 'code_analysis':
                return await self._handle_code_analysis(payload)
            elif request_type == 'math_problem':
                return await self._handle_math_problem(payload)
            else:
                return {
                    'status': 'error',
                    'message': f'Unsupported request type: {request_type}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    async def _handle_text_generation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle text generation requests.
        
        Args:
            payload (Dict[str, Any]): Text generation request payload
        
        Returns:
            Dict[str, Any]: Generated text response
        """
        prompt = payload.get('prompt', '')
        max_length = payload.get('max_length', 100)
        
        response = await self.send_message(f"Generate a text of up to {max_length} words: {prompt}")
        
        return {
            'status': 'success',
            'type': 'text_generation',
            'content': response,
            'length': len(response.split())
        }
    
    async def _handle_code_analysis(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle code analysis requests.
        
        Args:
            payload (Dict[str, Any]): Code analysis request payload
        
        Returns:
            Dict[str, Any]: Code analysis response
        """
        code = payload.get('code', '')
        language = payload.get('language', 'python')
        
        response = await self.send_message(f"Analyze the following {language} code and provide insights: {code}")
        
        return {
            'status': 'success',
            'type': 'code_analysis',
            'language': language,
            'insights': response
        }
    
    async def _handle_math_problem(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle mathematical problem-solving requests.
        
        Args:
            payload (Dict[str, Any]): Math problem request payload
        
        Returns:
            Dict[str, Any]: Math problem solution
        """
        problem = payload.get('problem', '')
        
        response = await self.send_message(f"Solve this mathematical problem step by step: {problem}")
        
        return {
            'status': 'success',
            'type': 'math_problem',
            'solution': response
        }

async def main():
    """
    Main function to demonstrate multi-request WebSocket communication.
    """
    # Create the multi-request WebSocket agent
    agent = MultiRequestAgent()
    
    # Setup communication interface
    communication_interface = await AsyncAgent.setup_communication(
        host='localhost', 
        port=8767  # Changed from 8766 to avoid address in use error
    )
    
    logger.info(f"Multi-Request WebSocket server started on {communication_interface['host']}:{communication_interface['port']}")
    
    # Keep the server running
    await communication_interface['server'].wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
