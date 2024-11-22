import asyncio
import websockets
import json

async def send_message(websocket, message):
    await websocket.send(json.dumps(message))
    response = await websocket.recv()
    return json.loads(response)

async def main():
    uri = "ws://localhost:8765/ws"
    async with websockets.connect(uri) as websocket:
        # Example: Request content ideas for Instagram
        message = {
            "type": "content_request",
            "platform": "instagram",
            "niche": "tech_startup",
            "content_type": "carousel",
            "theme": "AI and automation"
        }
        
        print("Sending request for content ideas...")
        response = await send_message(websocket, message)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        # Example: Analyze engagement metrics
        message = {
            "type": "analyze_engagement",
            "platform": "instagram",
            "metrics": {
                "likes": 1200,
                "comments": 45,
                "shares": 30,
                "saves": 80,
                "reach": 5000
            }
        }
        
        print("\nRequesting engagement analysis...")
        response = await send_message(websocket, message)
        print(f"Response: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
