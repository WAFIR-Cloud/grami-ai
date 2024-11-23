import sys
import os
import asyncio
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grami.agent import Agent
from grami.providers import GeminiProvider
from examples.tools import WebSearchTool, SentimentAnalysisTool

class WebResearchAgent:
    def __init__(self, api_key):
        # Initialize the LLM provider
        self.llm_provider = GeminiProvider(api_key=api_key)
        
        # Create the web research agent
        self.agent = Agent(
            name="ResearchPro",
            role="Advanced Web Research and Trend Analysis Specialist",
            llm_provider=self.llm_provider,
            tools=[
                WebSearchTool(),
                SentimentAnalysisTool()
            ],
            initial_context=[
                {
                    "role": "system",
                    "content": """You are an expert web researcher and trend analyst.
                    Your capabilities include conducting comprehensive web searches, 
                    analyzing search results, extracting key insights, and providing 
                    detailed, structured reports on various topics."""
                }
            ]
        )

    async def conduct_market_research(self, topic, industry):
        """
        Perform comprehensive market research on a given topic
        """
        # Conduct web search
        search_query = f"Latest trends and innovations in {topic} within {industry}"
        search_results = await self.agent.send_message(f"Perform web search: {search_query}")
        
        # Analyze sentiment of search results
        sentiment_analysis = await self.agent.send_message(
            f"Analyze the sentiment of these search results: {search_results}"
        )
        
        # Extract key insights
        insights_response = await self.agent.send_message(
            f"Extract and summarize key insights from these search results about {topic} in {industry}. "
            "Provide a structured analysis including trends, opportunities, and potential challenges."
        )
        
        # Generate a comprehensive report
        report = await self.agent.send_message(
            f"Create a detailed market research report based on these insights: {insights_response}. "
            "Include an executive summary, key findings, and recommendations."
        )
        
        return {
            "search_query": search_query,
            "search_results": search_results,
            "sentiment_analysis": sentiment_analysis,
            "insights": insights_response,
            "full_report": report
        }

    async def trend_prediction(self, industry, time_horizon='next 2 years'):
        """
        Predict future trends in a specific industry
        """
        # Research current trends
        trend_search = await self.agent.send_message(
            f"Research and identify emerging trends in {industry} for the {time_horizon}"
        )
        
        # Analyze potential impact
        trend_analysis = await self.agent.send_message(
            f"Analyze the potential impact of these trends: {trend_search}. "
            "Provide a structured prediction with potential scenarios and implications."
        )
        
        # Generate a trend prediction report
        prediction_report = await self.agent.send_message(
            f"Create a comprehensive trend prediction report based on this analysis: {trend_analysis}. "
            "Include probability assessments, potential disruptors, and strategic recommendations."
        )
        
        return {
            "industry": industry,
            "time_horizon": time_horizon,
            "current_trends": trend_search,
            "trend_analysis": trend_analysis,
            "prediction_report": prediction_report
        }

async def main():
    # Initialize the Web Research Agent
    research_agent = WebResearchAgent(
        api_key="YOUR_API_KEY"  # Replace with actual API key
    )
    
    # Demonstrate market research
    print("--- Market Research: AI in Marketing ---")
    market_research = await research_agent.conduct_market_research(
        topic="AI Technologies",
        industry="Digital Marketing"
    )
    
    # Print market research results
    print("\n--- Search Query ---")
    print(market_research['search_query'])
    
    print("\n--- Search Results ---")
    print(market_research['search_results'])
    
    print("\n--- Sentiment Analysis ---")
    print(market_research['sentiment_analysis'])
    
    print("\n--- Key Insights ---")
    print(market_research['insights'])
    
    print("\n--- Full Market Research Report ---")
    print(market_research['full_report'])
    
    # Demonstrate trend prediction
    print("\n\n--- Trend Prediction: Tech Industry ---")
    trend_prediction = await research_agent.trend_prediction(
        industry="Artificial Intelligence",
        time_horizon="next 3 years"
    )
    
    print("\n--- Trend Prediction Report ---")
    print(json.dumps(trend_prediction, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
