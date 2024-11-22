import asyncio
from typing import Dict, Any, Optional

from grami_ai.core.agent import AsyncAgent
from grami_ai.tools.base import AsyncBaseTool

class WeatherAnalysisTool(AsyncBaseTool):
    """
    A custom tool demonstrating advanced tool creation in Grami AI
    """
    def __init__(self):
        super().__init__()
        self.metadata.name = "weather_analysis"
        self.metadata.description = "Analyze weather conditions and provide insights"

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Simulate weather analysis based on given context
        
        :param task: Type of weather analysis task
        :param context: Context for weather analysis
        :return: Weather analysis results
        """
        location = context.get('location', 'default')
        analysis_type = context.get('type', 'current')
        
        # Simulated weather data
        weather_data = {
            'san_francisco': {
                'current': {
                    'temperature': 65,
                    'condition': 'Partly Cloudy',
                    'humidity': 62
                },
                'forecast': {
                    'next_24h': 'Mild with occasional light rain',
                    'temperature_range': '60-70°F'
                }
            },
            'new_york': {
                'current': {
                    'temperature': 45,
                    'condition': 'Cloudy',
                    'humidity': 75
                },
                'forecast': {
                    'next_24h': 'Cold with possible snow showers',
                    'temperature_range': '40-50°F'
                }
            }
        }
        
        # Retrieve weather information
        location_data = weather_data.get(location.lower().replace(' ', '_'), 
                                         weather_data['san_francisco'])
        
        result = location_data.get(analysis_type, location_data['current'])
        
        return {
            'status': 'success',
            'location': location,
            'analysis_type': analysis_type,
            'data': result
        }

async def main():
    """
    Demonstrate a custom tool integrated with an AsyncAgent
    """
    # Create an agent with a custom weather analysis tool
    agent = await AsyncAgent.create(
        name="WeatherInsightAgent",
        llm="gemini",  # Configurable LLM provider
        tools=[WeatherAnalysisTool()],
        system_instruction="Provide detailed weather insights and analysis"
    )

    # Analyze weather for different locations
    locations = ['San Francisco', 'New York']
    analysis_types = ['current', 'forecast']
    
    for location in locations:
        for analysis_type in analysis_types:
            response = await agent.process({
                "type": "weather_analysis",
                "location": location,
                "analysis_type": analysis_type
            })
            
            print(f"Weather Analysis for {location} - {analysis_type.capitalize()}:")
            print(f"Data: {response['data']}")
            print("\n---\n")

if __name__ == "__main__":
    asyncio.run(main())
