import asyncio
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

def read_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")
    return api_key

async def main():
    # Initialize components
    memory = LRUMemory(capacity=1000)
    provider = GeminiProvider(
        api_key=read_api_key(),
        system_prompt="You are a helpful AI assistant with perfect memory capabilities."
    )
    
    # Create agent with memory
    agent = AsyncAgent(
        name="MemoryBot",
        role="A helpful AI assistant with perfect memory capabilities",
        llm_provider=provider,
        memory_provider=memory
    )

    # Example conversation
    messages = [
        {"role": "user", "content": "Hi! My name is Alice and I love playing chess and piano."},
        {"role": "user", "content": "What's my name?"},
        {"role": "user", "content": "What are my hobbies?"},
        {"role": "user", "content": "I also enjoy painting watercolors and hiking in the mountains."},
        {"role": "user", "content": "Please list everything you know about me so far."}
    ]

    # Conversation loop
    for msg in messages:
        print(f"User: {msg['content']}")
        response = await agent.send_message(msg)
        
        # Explicitly store memory
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_key = f"{current_timestamp}_{str(uuid.uuid4())[:8]}"
        await memory.store(
            unique_key, 
            {
                "type": "conversation_turn",
                "user_message": {
                    "content": msg.get('content', ''),
                    "role": "user"
                },
                "model_response": {
                    "content": response,
                    "role": "model"
                },
                "timestamp": current_timestamp
            }
        )
        
        print(f"Agent: {response}\n")

    # Demonstrate memory retrieval
    print("Memory Contents:")
    contents = await memory.list_contents()
    import json
    print(json.dumps(contents, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
