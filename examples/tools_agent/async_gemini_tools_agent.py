import asyncio
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from grami.agent import AsyncAgent
from grami.providers.gemini_provider import GeminiProvider
from grami.memory.lru import LRUMemory

# Load environment variables
load_dotenv()

# Utility functions for demonstration
def get_current_time() -> str:
    """
    Retrieve the current time.
    
    Returns:
        Current time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_age(birth_year: int, current_year: Optional[int] = None) -> int:
    """
    Calculate a person's age based on their birth year.
    
    Args:
        birth_year: The year the person was born
        current_year: Optional current year (defaults to current year)
    
    Returns:
        The person's age
    """
    if current_year is None:
        current_year = datetime.now().year
    
    return current_year - birth_year

def greet_person(name: str, age: Optional[int] = None) -> str:
    """
    Generate a personalized greeting.
    
    Args:
        name: The name of the person to greet
        age: Optional age of the person
    
    Returns:
        A personalized greeting message
    """
    if age is not None:
        return f"Hello, {name}! You are {age} years old. Nice to meet you!"
    return f"Hello, {name}! Nice to meet you!"

async def main():
    # Initialize Gemini provider
    provider = GeminiProvider(api_key=os.getenv('GEMINI_API_KEY'))

    # Create AsyncAgent with tools
    agent = AsyncAgent(
        name="ToolsDemoAgent",
        llm=provider,
        memory=LRUMemory(capacity=100),
        tools=[
            get_current_time,
            calculate_age,
            greet_person
        ],
        system_instructions=(
            "You are a precise and helpful AI assistant with access to specific utility functions. "
            "CRITICAL FUNCTION CALLING GUIDELINES:\n"
            "1. When a query can be answered by a specific function, suggest calling that function.\n"
            "2. For time-related queries, suggest calling get_current_time()\n"
            "3. For age calculations, suggest calling calculate_age(birth_year)\n"
            "4. For personalized greetings, suggest calling greet_person(name, age)\n"
            "5. Explain the function's purpose and why it's relevant to the query.\n"
            "6. If a function can provide an exact answer, prioritize its use.\n"
            "7. Available functions:\n"
            "   - get_current_time(): Returns the exact current timestamp\n"
            "   - calculate_age(birth_year): Calculates precise age\n"
            "   - greet_person(name, age): Generates a personalized greeting\n"
            "IMPORTANT: Demonstrate clear reasoning for function usage."
        )
    )

    # Demonstrate tool usage
    test_messages = [
        "What is the exact current time right now?",
        "Calculate how old someone would be if they were born in 1990.",
        "Create a personalized greeting for Alice, who is 33 years old.",
        "Help me calculate my age if I was born in 1985. Show your calculation."
    ]

    for message in test_messages:
        print(f"\nUser: {message}")
        response = await agent.send_message(message)
        print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
