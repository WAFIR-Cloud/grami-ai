import sys
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import Agent, AgentCrew
from grami.providers import GeminiProvider
from examples.tools import WebSearchTool, WeatherTool, CalculatorTool

async def main():
    # Initialize Gemini Provider with the provided API key
    gemini_provider = GeminiProvider(
        api_key=os.getenv('GEMINI_API_KEY')
    )

    # Create multiple agents with different roles
    research_agent = Agent(
        name="ResearchAssistant",
        role="Research and Information Gathering Specialist",
        llm_provider=gemini_provider,
        tools=[WebSearchTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a research assistant specialized in finding and summarizing information from the web."
            }
        ]
    )

    weather_agent = Agent(
        name="WeatherExpert",
        role="Climate and Weather Information Analyst",
        llm_provider=gemini_provider,
        tools=[WeatherTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a weather expert who provides detailed and accurate weather information for various locations."
            }
        ]
    )

    math_agent = Agent(
        name="MathTutor",
        role="Mathematical Calculation and Problem-Solving Assistant",
        llm_provider=gemini_provider,
        tools=[CalculatorTool()],
        initial_context=[
            {
                "role": "system", 
                "content": "You are a math tutor who helps solve mathematical problems and performs precise calculations."
            }
        ]
    )

    # Create an AgentCrew with the specialized agents
    agent_crew = AgentCrew(
        agents=[research_agent, weather_agent, math_agent]
    )

    # Demonstration of agent crew capabilities
    async def crew_demonstration():
        # Retrieve a specific agent
        math_specialist = await agent_crew.get_agent("MathTutor")
        
        # Perform a calculation
        print("\n--- Math Calculation ---")
        math_response = await math_specialist.send_message("Calculate the area of a circle with radius 5")
        print(math_response)

        # Retrieve weather information
        weather_specialist = await agent_crew.get_agent("WeatherExpert")
        print("\n--- Weather Information ---")
        weather_response = await weather_specialist.send_message("What's the current temperature in New York?")
        print(weather_response)

        # Perform a web search
        research_specialist = await agent_crew.get_agent("ResearchAssistant")
        print("\n--- Web Research ---")
        research_response = await research_specialist.send_message("What are the latest advancements in AI for 2023?")
        print(research_response)

        # Demonstrate streaming with a math agent
        print("\n--- Streaming Calculation Explanation ---")
        async for token in math_specialist.stream_message("Explain how to calculate the area of a circle"):
            print(token, end='', flush=True)
        print()  # New line after streaming

    # Run the crew demonstration
    await crew_demonstration()

if __name__ == "__main__":
    asyncio.run(main())
