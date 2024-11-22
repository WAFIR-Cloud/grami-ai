import asyncio
import websockets
import json
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def send_message(websocket, message):
    try:
        logger.info(f"Sending message: {message}")
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        parsed_response = json.loads(response)
        logger.info(f"Received response: {parsed_response}")
        return parsed_response
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response")
        return None
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def get_websocket_port():
    # Try environment variable first
    port = os.environ.get('GRAMI_WEBSOCKET_PORT')
    
    # If not in environment, try reading from file
    if not port:
        try:
            with open('/tmp/grami_websocket_port.txt', 'r') as f:
                port = f.read().strip()
        except FileNotFoundError:
            logger.error("Could not find WebSocket port")
            port = 8765  # Fallback default
    
    return int(port)

async def main():
    # Get the WebSocket port
    port = get_websocket_port()
    uri = f"ws://localhost:{port}/ws"
    
    logger.info(f"Attempting to connect to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("WebSocket connection established")
            
            # Example: Request content ideas for Instagram
            message = {
                "type": "content_request",
                "platform": "instagram",
                "niche": "tech",
                "content_type": "post"
            }
            
            response = await send_message(websocket, message)
            if response:
                logger.info("Received response successfully")
    except Exception as e:
        logger.error(f"Connection error: {e}")
        # Print out any environment variables that might be relevant
        logger.info(f"Environment GRAMI_WEBSOCKET_PORT: {os.environ.get('GRAMI_WEBSOCKET_PORT')}")

if __name__ == "__main__":
    asyncio.run(main())
