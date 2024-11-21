import asyncio
import json
from typing import List, Dict, Any

from grami_ai.memory import AsyncInMemoryMemory
from grami_ai.tools import (
    CalculatorTool, 
    JSONParserTool, 
    StringManipulationTool, 
    WebScraperTool
)

class MultiToolWorkflow:
    """
    An advanced workflow demonstrating complex 
    interactions between multiple async tools
    """
    
    def __init__(self):
        # Initialize tools and memory
        self.memory = AsyncInMemoryMemory(max_size=100)
        self.calculator = CalculatorTool()
        self.json_parser = JSONParserTool()
        self.string_tool = StringManipulationTool()
        self.web_scraper = WebScraperTool()
    
    async def analyze_global_trends(self, topics: List[str]) -> Dict[str, Any]:
        """
        Perform a multi-step global trend analysis
        
        Args:
            topics: List of topics to analyze
        
        Returns:
            Comprehensive trend analysis report
        """
        # Store initial context
        await self.memory.add_item('analysis_context', {
            'topics': topics,
            'start_time': asyncio.get_event_loop().time()
        })
        
        # Parallel topic research
        topic_results = await asyncio.gather(
            *[self._research_topic(topic) for topic in topics]
        )
        
        # Aggregate and analyze results
        trend_report = await self._synthesize_trend_report(topic_results)
        
        # Store final report in memory
        await self.memory.add_item('trend_report', trend_report)
        
        return trend_report
    
    async def _research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Conduct in-depth research on a single topic
        
        Args:
            topic: Research topic
        
        Returns:
            Detailed topic research
        """
        # Clean topic name
        cleaned_topic = await self.string_tool.execute(topic)
        
        # Construct research URLs
        research_urls = [
            f"https://en.wikipedia.org/wiki/{cleaned_topic.replace(' ', '_')}",
            f"https://trends.google.com/trends/explore?q={cleaned_topic.replace(' ', '%20')}"
        ]
        
        # Fetch and process sources
        topic_sources = []
        for url in research_urls:
            try:
                # Web scraping
                content = await self.web_scraper.execute(url, operation='parse')
                
                # Process content
                word_count = await self.string_tool.execute(
                    content, 
                    operation='count_words'
                )
                
                topic_sources.append({
                    'url': url,
                    'content': content,
                    'word_count': word_count
                })
            
            except Exception as e:
                print(f"Error researching {topic} from {url}: {e}")
        
        return {
            'topic': cleaned_topic,
            'sources': topic_sources
        }
    
    async def _synthesize_trend_report(
        self, 
        topic_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Synthesize a comprehensive trend report
        
        Args:
            topic_results: Research results for multiple topics
        
        Returns:
            Aggregated trend analysis
        """
        # Calculate total research volume
        total_sources = sum(
            len(result['sources']) for result in topic_results
        )
        
        # Calculate total word count
        total_words = 0
        for result in topic_results:
            for source in result['sources']:
                total_words += source.get('word_count', 0)
        
        # Calculate average words per source
        avg_words_per_source = await self.calculator.execute(
            f'{total_words} / {total_sources}' if total_sources > 0 else '0'
        )
        
        # Prepare trend report
        trend_report = {
            'total_topics': len(topic_results),
            'total_sources': total_sources,
            'total_words': total_words,
            'average_words_per_source': avg_words_per_source,
            'topic_details': topic_results
        }
        
        return trend_report

async def main():
    # Demonstrate the Multi-Tool Workflow
    workflow = MultiToolWorkflow()
    
    # Analyze global trends for multiple topics
    global_trends = await workflow.analyze_global_trends([
        "Artificial Intelligence",
        "Climate Change",
        "Renewable Energy"
    ])
    
    # Pretty print results
    print(json.dumps(global_trends, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
