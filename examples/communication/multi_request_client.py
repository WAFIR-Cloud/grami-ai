import asyncio
import json
import logging
import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiRequestWebSocketClient:
    """
    WebSocket client for sending multiple types of requests to the agent.
    """
    
    def __init__(self, uri: str = "ws://localhost:8767"):
        """
        Initialize WebSocket client.
        
        Args:
            uri (str): WebSocket server URI
        """
        self.uri = uri
    
    async def send_request(self, websocket, request_type: str, payload: dict):
        """
        Send a request to the WebSocket server.
        
        Args:
            websocket: Active WebSocket connection
            request_type (str): Type of request to send
            payload (dict): Request payload
        
        Returns:
            dict: Server response
        """
        try:
            # Prepare the request
            request = {
                "type": "agent_request",
                "request_type": request_type,
                "payload": payload
            }
            
            # Send the request
            await websocket.send(json.dumps(request))
            logger.info(f"Sent {request_type} request: {payload}")
            
            # Receive the response
            response_str = await websocket.recv()
            response = json.loads(response_str)
            
            logger.info(f"Received {request_type} response: {response}")
            return response
        
        except Exception as e:
            logger.error(f"Error in {request_type} request: {e}")
            return {"status": "error", "message": str(e)}
    
    async def run_example_requests(self):
        """
        Run a series of example requests to demonstrate multi-request capabilities.
        """
        try:
            async with websockets.connect(self.uri, subprotocols=['agent-protocol']) as websocket:
                # Text Generation Request
                text_gen_response = await self.send_request(
                    websocket, 
                    'text_generation', 
                    {
                        'prompt': 'Write a short story about a curious robot',
                        'max_length': 50
                    }
                )
                
                # Code Analysis Request
                code_analysis_response = await self.send_request(
                    websocket, 
                    'code_analysis', 
                    {
                        'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
''',
                        'language': 'python'
                    }
                )
                
                # Math Problem Request
                math_problem_response = await self.send_request(
                    websocket, 
                    'math_problem', 
                    {
                        'problem': 'Solve the equation: 3x + 7 = 22'
                    }
                )
                
                # Collect and log all responses
                return {
                    'text_generation': text_gen_response,
                    'code_analysis': code_analysis_response,
                    'math_problem': math_problem_response
                }
        
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"WebSocket connection error: {e}")
            return None

async def main():
    """
    Main function to run the multi-request WebSocket client.
    """
    client = MultiRequestWebSocketClient()
    results = await client.run_example_requests()
    
    if results:
        # Pretty print results
        for request_type, response in results.items():
            print(f"\n{request_type.upper()} Response:")
            print(json.dumps(response, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
