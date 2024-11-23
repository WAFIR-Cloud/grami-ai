import asyncio
import json
import logging
import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketClient:
    """
    WebSocket client for testing AI agent communication.
    """
    
    def __init__(self, uri: str = "ws://localhost:8765"):
        """
        Initialize WebSocket client.
        
        Args:
            uri (str): WebSocket server URI
        """
        self.uri = uri
    
    async def connect(self):
        """
        Establish WebSocket connection and handle communication.
        """
        try:
            async with websockets.connect(self.uri, subprotocols=['agent-protocol']) as websocket:
                # Send initial test message
                await self.send_message(websocket, "Hello, AI Agent!")
                
                # Receive and process response
                response = await websocket.recv()
                parsed_response = json.loads(response)
                
                logger.info(f"Received agent response: {parsed_response}")
        
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"WebSocket connection error: {e}")
    
    async def send_message(self, websocket, message: str):
        """
        Send a message to the WebSocket server.
        
        Args:
            websocket: Active WebSocket connection
            message (str): Message to send
        """
        try:
            payload = json.dumps({
                "type": "agent_message",
                "content": message
            })
            await websocket.send(payload)
            logger.info(f"Sent message: {message}")
        
        except Exception as e:
            logger.error(f"Error sending message: {e}")

async def main():
    """
    Main function to run the WebSocket client.
    """
    client = WebSocketClient()
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
