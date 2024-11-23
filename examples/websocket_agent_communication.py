import asyncio
import logging
import json
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

async def example_custom_handler(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example custom message handler for demonstration.
    
    Args:
        message (Dict): Incoming message dictionary
    
    Returns:
        Dict: Processed response
    """
    logging.info(f"Processing message: {message}")
    
    if message.get('type') == 'agent_message':
        return {
            'status': 'processed',
            'response': f"Received agent message: {message.get('content')}"
        }
    return {'status': 'unknown_message_type'}

class AgentWebSocketServer:
    """
    WebSocket server for agent communication with FastAPI.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 8765):
        """
        Initialize the WebSocket server.
        
        Args:
            host (str): Server host. Defaults to 'localhost'.
            port (int): Server port. Defaults to 8765.
        """
        self.app = FastAPI(title="GRAMI-AI Agent WebSocket Server")
        self.host = host
        self.port = port
        self.logger = logging.getLogger(__name__)
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_websocket(websocket)
    
    async def handle_websocket(self, websocket: WebSocket):
        """
        Handle WebSocket connections and messages.
        
        Args:
            websocket (WebSocket): Connected WebSocket
        """
        await websocket.accept()
        
        try:
            while True:
                try:
                    # Receive message
                    data = await websocket.receive_text()
                    
                    # Parse and process message
                    parsed_message = json.loads(data)
                    response = await example_custom_handler(parsed_message)
                    
                    # Send response
                    await websocket.send_text(json.dumps(response))
                
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({
                        "status": "error",
                        "message": "Invalid JSON format"
                    }))
                except Exception as e:
                    self.logger.error(f"Message processing error: {e}")
        
        except WebSocketDisconnect:
            self.logger.info("WebSocket connection closed")
    
    def run(self):
        """
        Run the WebSocket server.
        """
        uvicorn.run(
            self.app, 
            host=self.host, 
            port=self.port, 
            log_level="info"
        )

async def websocket_client_example():
    """
    Example WebSocket client for testing.
    """
    import websockets
    
    uri = "ws://localhost:8765/ws"
    
    async with websockets.connect(uri) as websocket:
        # Send a test message
        test_message = {
            "type": "agent_message",
            "sender": "test_client",
            "content": "Hello, WebSocket server!"
        }
        await websocket.send(json.dumps(test_message))
        
        # Receive response
        response = await websocket.recv()
        print(f"Received response: {response}")

def main():
    """
    Main entry point for WebSocket server and client example.
    """
    logging.basicConfig(level=logging.INFO)
    
    # Start WebSocket server
    server = AgentWebSocketServer(host='localhost', port=8765)
    
    # Run server in a separate thread/process
    import threading
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    
    # Give the server a moment to start
    import time
    time.sleep(1)
    
    # Run client example
    asyncio.run(websocket_client_example())

if __name__ == "__main__":
    main()
