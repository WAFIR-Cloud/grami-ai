import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import AsyncAgent
from grami.providers import GeminiProvider

# Read API key directly from .env file
def read_api_key():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        print("Error: .env file not found")
        return None

async def main():
    # Get Gemini API key
    api_key = read_api_key()
    if not api_key:
        print("Cannot proceed without API key")
        return

    # Initialize Gemini Provider with the API key
    gemini_provider = GeminiProvider(
        api_key=api_key
    )

    # Create an async Gemini agent specialized in scientific explanations
    science_agent = AsyncAgent(
        name="ScienceExplanationAgent",
        role="Scientific Concept Explainer",
        llm_provider=gemini_provider,
        initial_context=[
            {
                "role": "system", 
                "content": "You are an expert at explaining complex scientific concepts in a clear, engaging manner."
            }
        ]
    )

    # Demonstrate agent capabilities
    async def agent_demonstration():
        # Perform a complex scientific explanation
        print("\n--- Quantum Mechanics Explanation ---")
        quantum_response = await science_agent.send_message(
            "Explain quantum entanglement in simple terms for a high school student"
        )
        print(quantum_response)

        # Demonstrate streaming explanation
        print("\n--- Streaming Scientific Concept ---")
        async for token in science_agent.stream_message(
            "Describe how photosynthesis works at the molecular level"
        ):
            print(token, end='', flush=True)
        print()  # New line after streaming

        # Demonstrate multi-turn conversation
        print("\n--- Multi-turn Conversation ---")
        conversation_context = []
        
        # First message
        first_response = await science_agent.send_message(
            "What is dark matter?", 
            context=conversation_context
        )
        print("Dark Matter Explanation:", first_response)
        
        # Follow-up question
        follow_up_response = await science_agent.send_message(
            "How do scientists try to detect dark matter?", 
            context=conversation_context
        )
        print("\nDetection Methods:", follow_up_response)

    # Run the agent demonstration
    await agent_demonstration()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
