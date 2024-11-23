import os
import asyncio
from typing import Optional
from datetime import datetime, timedelta

from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Utility functions for demonstration
def get_current_time() -> str:
    """
    Get the current timestamp.
    
    :return: Current timestamp as a string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_days_until_birthday(birth_date: str) -> int:
    """
    Calculate the number of days until the next birthday.
    
    :param birth_date: Birth date in YYYY-MM-DD format
    :return: Number of days until next birthday
    """
    try:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.now()
        
        # Calculate next birthday
        next_birthday = birth_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        # Calculate days until next birthday
        days_until_birthday = (next_birthday - today).days
        return days_until_birthday
    except ValueError:
        return -1

def generate_personalized_advice(age: int, interests: Optional[str] = None) -> str:
    """
    Generate personalized life advice based on age and optional interests.
    
    :param age: Age of the person
    :param interests: Optional interests of the person
    :return: Personalized advice
    """
    base_advice = {
        (0, 18): "Focus on education and personal growth.",
        (18, 30): "Explore career opportunities and build skills.",
        (30, 45): "Balance career and personal life, invest wisely.",
        (45, 60): "Plan for retirement and enjoy life experiences.",
        (60, 100): "Stay active, spend time with loved ones, and pursue hobbies."
    }
    
    # Find appropriate advice based on age
    advice = next((adv for (min_age, max_age), adv in base_advice.items() if min_age <= age < max_age), 
                  "Enjoy life and stay positive!")
    
    # Personalize advice if interests are provided
    if interests:
        advice += f" Consider exploring {interests} to enrich your life."
    
    return advice

async def main():
    # Initialize Gemini Provider with API key from environment
    gemini_provider = GeminiProvider(
        api_key=os.getenv('GEMINI_API_KEY', ''),
        model_name="gemini-pro"
    )
    
    # Initialize AsyncAgent with Gemini Provider, LRU Memory, and Tools
    agent = AsyncAgent(
        name="StreamToolsAgent",
        llm=gemini_provider,
        memory=LRUMemory(capacity=100),
        tools=[
            get_current_time,
            calculate_days_until_birthday,
            generate_personalized_advice
        ]
    )
    
    # Demonstration of streaming tool calls
    async def stream_interaction(query: str):
        print(f"\n🤖 Query: {query}")
        print("🌊 Streaming Response:")
        
        # Stream the response
        async for chunk in agent.stream_message(query):
            print(chunk, end='', flush=True)
        print("\n")
    
    # Test interactions
    await stream_interaction("What is the current time?")
    await stream_interaction("How many days untiam afl my birthday if I was born on 1990-05-15?")
    await stream_interaction("Give me life advice for a 35-year-old interested in technology")
    
    # Print conversation history
    print("\n📜 Conversation History:")
    history = gemini_provider.get_conversation_history()
    for turn in history:
        print(f"User: {turn.get('user_message', {}).get('content', 'N/A')}")
        print(f"Model: {turn.get('model_response', {}).get('content', 'N/A')}\n")

if __name__ == "__main__":
    asyncio.run(main())
