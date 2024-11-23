import asyncio
import sys
import os
import random

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import AsyncAgent

class DataAnalysisAgent(AsyncAgent):
    """
    A specialized AsyncAgent for data analysis with custom async methods.
    """
    async def analyze_data(self, data_points: list) -> dict:
        """
        Simulate an async data analysis process.
        
        :param data_points: List of numerical data points
        :return: Analysis results
        """
        # Simulate complex async computation
        await asyncio.sleep(1)  # Simulating processing time
        
        return {
            "mean": sum(data_points) / len(data_points),
            "min": min(data_points),
            "max": max(data_points),
            "variance": self._calculate_variance(data_points)
        }
    
    def _calculate_variance(self, data_points: list) -> float:
        """
        Calculate variance (internal method).
        
        :param data_points: List of numerical data points
        :return: Variance of the data
        """
        mean = sum(data_points) / len(data_points)
        return sum((x - mean) ** 2 for x in data_points) / len(data_points)
    
    async def generate_sample_data(self, size: int) -> list:
        """
        Asynchronously generate sample data.
        
        :param size: Number of data points to generate
        :return: List of random data points
        """
        await asyncio.sleep(0.5)  # Simulate data generation time
        return [random.uniform(0, 100) for _ in range(size)]

async def main():
    # Create a DataAnalysisAgent
    data_agent = DataAnalysisAgent(
        name="DataAnalyzer",
        description="An AI agent for data analysis",
        config={
            "analysis_mode": "comprehensive",
            "confidence_level": 0.95
        }
    )

    # Generate sample data
    sample_data = await data_agent.generate_sample_data(50)
    print(f"Generated {len(sample_data)} data points")

    # Perform data analysis
    analysis_results = await data_agent.analyze_data(sample_data)
    
    # Print analysis results
    print("\nData Analysis Results:")
    for key, value in analysis_results.items():
        print(f"{key.capitalize()}: {value}")

    # Demonstrate configuration update
    await data_agent.update_config({"sample_size": 50})
    print("\nUpdated Configuration:", data_agent.config)

if __name__ == "__main__":
    asyncio.run(main())
