import asyncio
import json
import logging
from typing import Any, Dict, Optional, Set, Union

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from .event_bus import EventBus

class WebSocketAgentCommunication:
    """
    WebSocket communication interface for real-time agent interactions using FastAPI.
    
    Supports bidirectional communication for AI agents, allowing 
    real-time message exchange, event streaming, and agent coordination.
    """
    
    def __init__(
        self, 
        host: str = 'localhost', 
        port: int = 8765,
        agent: Optional[Any] = None
    ):
        """
        Initialize WebSocket server for agent communication.
        
        Args:
            host (str): Hostname to bind the WebSocket server. Defaults to 'localhost'.
            port (int): Port number for WebSocket server. Defaults to 8765.
            agent (Optional[Any]): Agent instance to process messages
        """
        self.app = FastAPI(title="GRAMI-AI WebSocket Server")
        self.host = host
        self.port = port
        
        # Create event bus with the agent
        self.event_bus = EventBus(agent)
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Track active WebSocket connections
        self.active_connections: Set[WebSocket] = set()
        
        # Setup WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.handle_client(websocket)
        
        # Subscribe to agent response events
        self.event_bus.subscribe('agent_response', self.broadcast_agent_response)
    
    async def handle_client(self, websocket: WebSocket):
        """
        Handle individual WebSocket client connections.
        
        Args:
            websocket (WebSocket): Connected WebSocket client
        """
        try:
            # Accept the WebSocket connection
            await websocket.accept()
            self.active_connections.add(websocket)
            
            while True:
                try:
                    # Receive message
                    data = await websocket.receive_text()
                    
                    try:
                        # Parse incoming message
                        parsed_message = json.loads(data)
                        
                        # Publish message to event bus
                        await self.event_bus.publish('user_message', parsed_message.get('content', ''))
                    
                    except json.JSONDecodeError:
                        self.logger.error(f"Invalid JSON: {data}")
                        await websocket.send_text(json.dumps({
                            "status": "error",
                            "message": "Invalid JSON format"
                        }))
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                        await websocket.send_text(json.dumps({
                            "status": "error",
                            "message": str(e)
                        }))
                
                except WebSocketDisconnect:
                    break
        
        except Exception as e:
            self.logger.error(f"WebSocket connection error: {e}")
        
        finally:
            # Remove the connection
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
    
    async def broadcast_agent_response(self, response: str):
        """
        Broadcast agent response to all connected WebSocket clients.
        
        Args:
            response (str): Agent's response to broadcast
        """
        if not self.active_connections:
            self.logger.warning("No clients connected for broadcast")
            return
        
        for websocket in self.active_connections.copy():
            try:
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_text(json.dumps({
                        "type": "agent_response",
                        "content": response
                    }))
            except Exception as e:
                self.logger.error(f"Error broadcasting: {e}")
                # Remove disconnected websockets
                self.active_connections.discard(websocket)
    
    def run(self):
        """
        Run the communication server.
        """
        uvicorn.run(
            self.app, 
            host=self.host, 
            port=self.port, 
            log_level="info"
        )

def main():
    """
    Main entry point for WebSocket server.
    """
    logging.basicConfig(level=logging.INFO)
    
    ws_server = WebSocketAgentCommunication(
        host='localhost', 
        port=8765
    )
    
    ws_server.run()

if __name__ == "__main__":
    main()
