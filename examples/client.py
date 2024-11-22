import asyncio
import websockets
import json
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami_ai.core.interfaces import find_free_port

async def send_message(websocket, message):
    try:
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        return json.loads(response)
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

async def main():
    # Read the port from an environment variable or use a default
    port = int(os.environ.get('GRAMI_WEBSOCKET_PORT', 8765))
    uri = f"ws://localhost:{port}/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            # Example: Request content ideas for Instagram
            message = {
                "type": "content_request",
                "platform": "instagram",
                "niche": "tech",
                "content_type": "post"
            }
            
            response = await send_message(websocket, message)
            if response:
                print("Response:", response)
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
