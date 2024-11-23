from grami.core.base import BaseTool
import json
import datetime
import math

class WebSearchTool(BaseTool):
    """
    A tool for performing simulated web searches.
    """
    
    def validate_input(self, query: str = None) -> bool:
        """
        Validate the input for the web search.
        
        :param query: Search query
        :return: Boolean indicating if input is valid
        """
        return query is not None and len(query.strip()) > 0
    
    def execute(self, query: str) -> str:
        """
        Simulate a web search and return mock results.
        
        :param query: Search query
        :return: Simulated search results
        """
        # Predefined mock search results for common queries
        mock_results = {
            "AI advancements 2023": [
                {
                    'title': 'Top AI Trends in 2023',
                    'link': 'https://example.com/ai-trends-2023',
                    'snippet': 'Generative AI, Large Language Models, and Ethical AI are key trends.'
                },
                {
                    'title': 'AI Innovation Landscape',
                    'link': 'https://example.com/ai-innovation',
                    'snippet': 'Machine learning continues to evolve with more sophisticated models.'
                }
            ],
            "default": [
                {
                    'title': 'Search Result 1',
                    'link': 'https://example.com/result1',
                    'snippet': 'A simulated search result for your query.'
                }
            ]
        }
        
        # Use query-specific or default results
        results = mock_results.get(query, mock_results['default'])
        return json.dumps(results, indent=2)

class WeatherTool(BaseTool):
    """
    A tool for retrieving simulated weather information.
    """
    
    def validate_input(self, city: str = None) -> bool:
        """
        Validate the input for weather lookup.
        
        :param city: City name
        :return: Boolean indicating if input is valid
        """
        return city is not None and len(city.strip()) > 0
    
    def execute(self, city: str) -> str:
        """
        Simulate weather information for a specified city.
        
        :param city: City name
        :return: Simulated weather information
        """
        # Predefined mock weather data
        mock_weather = {
            "New York": {
                'temperature': 22.5,
                'description': 'Partly cloudy',
                'humidity': 65
            },
            "London": {
                'temperature': 15.3,
                'description': 'Light rain',
                'humidity': 80
            },
            "default": {
                'temperature': 20.0,
                'description': 'Mild weather',
                'humidity': 50
            }
        }
        
        # Use city-specific or default weather
        weather_data = mock_weather.get(city, mock_weather['default'])
        
        return json.dumps({
            'city': city,
            'temperature': weather_data['temperature'],
            'description': weather_data['description'],
            'humidity': weather_data['humidity'],
            'timestamp': datetime.datetime.now().isoformat()
        }, indent=2)

class CalculatorTool(BaseTool):
    """
    A comprehensive mathematical calculation tool.
    """
    
    def validate_input(self, operation: str = None, *args) -> bool:
        """
        Validate input for mathematical operations.
        
        :param operation: Mathematical operation
        :param args: Numeric arguments
        :return: Boolean indicating if input is valid
        """
        valid_operations = [
            'add', 'subtract', 'multiply', 'divide', 
            'power', 'square_root', 'area_circle', 
            'area_rectangle', 'volume_cube'
        ]
        
        # Validate operation and arguments
        if operation not in valid_operations:
            return False
        
        # Operation-specific validations
        if operation in ['add', 'subtract', 'multiply', 'divide', 'power']:
            return len(args) == 2 and all(isinstance(x, (int, float)) for x in args)
        elif operation in ['square_root', 'area_circle', 'volume_cube']:
            return len(args) == 1 and isinstance(args[0], (int, float))
        elif operation == 'area_rectangle':
            return len(args) == 2 and all(isinstance(x, (int, float)) for x in args)
        
        return False
    
    def execute(self, operation: str, *args) -> float:
        """
        Perform a mathematical operation.
        
        :param operation: Operation to perform
        :param args: Numeric arguments
        :return: Result of the operation
        """
        try:
            if operation == 'add':
                return args[0] + args[1]
            elif operation == 'subtract':
                return args[0] - args[1]
            elif operation == 'multiply':
                return args[0] * args[1]
            elif operation == 'divide':
                return args[0] / args[1]
            elif operation == 'power':
                return args[0] ** args[1]
            elif operation == 'square_root':
                return math.sqrt(args[0])
            elif operation == 'area_circle':
                return math.pi * (args[0] ** 2)
            elif operation == 'area_rectangle':
                return args[0] * args[1]
            elif operation == 'volume_cube':
                return args[0] ** 3
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        except Exception as e:
            return f"Calculation error: {str(e)}"
