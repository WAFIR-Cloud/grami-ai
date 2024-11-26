import asyncio
import os
from datetime import datetime
import json
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

from grami.agents import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Tool functions
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city: str = "London") -> str:
    """Get current weather for a city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found in environment variables"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"Current weather in {city}: {temp}°C, {desc}"
        else:
            return f"Error getting weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe characters
        safe_chars = set("0123456789+-*/(). ")
        if not all(c in safe_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    """Run the tools agent example."""
    # Initialize memory and provider
    memory = LRUMemory(capacity=5)
    provider = GeminiProvider(
        api_key=os.getenv("GEMINI_API_KEY"),
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1000,
            "candidate_count": 1
        }
    )
    
    # Create agent with tools
    agent = AsyncAgent(
        name="ToolsAgent",
        llm=provider,
        memory=memory,
        system_instructions="""You are a helpful AI assistant with access to various tools.
Available tools:
- get_current_time: Get the current date and time
- get_weather: Get current weather for a city (requires city name)
- calculate: Safely evaluate a mathematical expression

To use a tool, respond with: [TOOL] tool_name [/TOOL]
For example: [TOOL] get_current_time [/TOOL]

Always explain what you're doing before using a tool.""",
        tools=[get_current_time, get_weather, calculate]
    )
    
    print("Tools Agent Example")
    print("Available commands:")
    print("- Type 'exit' to quit")
    print("- Type 'clear' to clear conversation history")
    print("\nYou can ask about:")
    print("- Current time")
    print("- Weather in any city")
    print("- Mathematical calculations")
    print("\nExample questions:")
    print("- What time is it?")
    print("- What's the weather like in London?")
    print("- Calculate 15 * 24")
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit command
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            # Check for clear command
            if user_input.lower() == 'clear':
                memory.clear()
                print("Conversation history cleared!")
                continue
            
            # Process message and stream response
            print("Assistant: ", end="", flush=True)
            async for chunk in agent.stream_message(user_input):
                print(chunk, end="", flush=True)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
