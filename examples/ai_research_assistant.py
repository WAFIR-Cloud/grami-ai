import asyncio
import logging
from typing import List, Dict, Any

from grami_ai.memory import AsyncInMemoryMemory
from grami_ai.tools import (
    CalculatorTool, 
    JSONParserTool, 
    StringManipulationTool, 
    WebScraperTool
)

class AIResearchAssistant:
    """
    An advanced AI research assistant that leverages multiple tools
    and memory management to perform complex research tasks.
    """
    
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize memory and tools
        self.memory = AsyncInMemoryMemory(max_size=100)
        self.calculator = CalculatorTool()
        self.json_parser = JSONParserTool()
        self.string_tool = StringManipulationTool()
        self.web_scraper = WebScraperTool()
    
    async def research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Conduct a comprehensive research on a given topic
        
        Args:
            topic: Research topic to investigate
        
        Returns:
            Structured research findings
        """
        self.logger.info(f"Starting research on topic: {topic}")
        
        # Store initial research context
        await self.memory.add_item('research_context', {
            'topic': topic,
            'start_time': asyncio.get_event_loop().time()
        })
        
        # Web research phase
        web_sources = await self._gather_web_sources(topic)
        
        # Text processing phase
        processed_sources = await self._process_sources(web_sources)
        
        # Quantitative analysis
        statistical_summary = await self._analyze_sources(processed_sources)
        
        # Compile final research report
        research_report = {
            'topic': topic,
            'sources': web_sources,
            'processed_content': processed_sources,
            'statistics': statistical_summary
        }
        
        # Store final research in memory
        await self.memory.add_item('research_report', research_report)
        
        self.logger.info(f"Completed research on {topic}")
        return research_report
    
    async def _gather_web_sources(self, topic: str) -> List[str]:
        """
        Gather web sources related to the research topic
        
        Args:
            topic: Research topic
        
        Returns:
            List of web content sources
        """
        # Prepare search query
        search_query = await self.string_tool.execute(
            topic, 
            operation='clean'
        )
        
        # Predefined research sources (replace with actual URLs)
        research_sources = [
            f"https://en.wikipedia.org/wiki/{search_query.replace(' ', '_')}",
            f"https://scholar.google.com/scholar?q={search_query.replace(' ', '+')}"
        ]
        
        sources_content = []
        for url in research_sources:
            try:
                content = await self.web_scraper.execute(url, operation='parse')
                sources_content.append(content)
                self.logger.info(f"Scraped content from {url}")
            except Exception as e:
                self.logger.warning(f"Failed to scrape {url}: {e}")
        
        return sources_content
    
    async def _process_sources(self, sources: List[str]) -> List[Dict[str, Any]]:
        """
        Process and analyze web sources
        
        Args:
            sources: List of web source contents
        
        Returns:
            Processed and structured source information
        """
        processed_sources = []
        
        for source in sources:
            # Clean and analyze text
            cleaned_text = await self.string_tool.execute(source)
            word_count = await self.string_tool.execute(
                source, 
                operation='count_words'
            )
            
            processed_sources.append({
                'cleaned_text': cleaned_text,
                'word_count': word_count
            })
        
        return processed_sources
    
    async def _analyze_sources(self, processed_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform quantitative analysis on processed sources
        
        Args:
            processed_sources: Processed source information
        
        Returns:
            Statistical summary of sources
        """
        total_words = sum(
            source['word_count'] for source in processed_sources
        )
        
        # Simulate some statistical calculations
        avg_words = await self.calculator.execute(
            f'{total_words} / {len(processed_sources)}'
        )
        
        return {
            'total_sources': len(processed_sources),
            'total_words': total_words,
            'average_words_per_source': avg_words
        }

async def main():
    # Demonstrate the AI Research Assistant
    research_assistant = AIResearchAssistant()
    
    # Research a sample topic
    research_results = await research_assistant.research_topic(
        "Artificial Intelligence in Scientific Research"
    )
    
    # Pretty print results
    import json
    print(json.dumps(research_results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
