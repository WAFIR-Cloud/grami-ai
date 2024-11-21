"""
Advanced example showcasing GRAMI AI's features including:
- Custom tools
- Redis memory backend
- Event handling
- Multiple agents collaboration
"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

from grami_ai.agents.base_agent import BaseAgent
from grami_ai.memory import RedisMemory
from grami_ai.tools import BaseTool
from grami_ai.events import EventBus, Event
from grami_ai.core.config import settings
from grami_ai.core.constants import Priority

@dataclass
class DataAnalysisTool(BaseTool):
    name: str = "data_analysis"
    description: str = "Analyzes data and returns insights"
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        data = params.get("data", [])
        # Simulate data analysis
        return {
            "mean": sum(data) / len(data) if data else 0,
            "count": len(data),
            "insights": "Sample data analysis result"
        }

class DataCollectorAgent(BaseAgent):
    """Agent responsible for collecting and preprocessing data."""
    
    async def initialize(self) -> None:
        self.memory = RedisMemory(
            host=settings.redis.host,
            port=settings.redis.port
        )
        self.name = "Data Collector"
        self.event_bus = EventBus()
        
        # Subscribe to data collection events
        await self.event_bus.subscribe("data_collection", self.handle_data)
    
    async def handle_data(self, event: Event) -> None:
        """Handle incoming data collection events."""
        data = event.data.get("values", [])
        
        # Store data in memory
        await self.memory.add_item(
            f"dataset_{event.id}",
            {"values": data, "timestamp": event.timestamp}
        )
        
        # Notify analysis agent
        await self.event_bus.publish(
            Event(
                type="analysis_ready",
                data={"dataset_id": f"dataset_{event.id}"}
            )
        )

class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing collected data."""
    
    async def initialize(self) -> None:
        self.memory = RedisMemory(
            host=settings.redis.host,
            port=settings.redis.port
        )
        self.tools = [DataAnalysisTool()]
        self.name = "Data Analyzer"
        self.event_bus = EventBus()
        
        # Subscribe to analysis events
        await self.event_bus.subscribe("analysis_ready", self.handle_analysis)
    
    async def handle_analysis(self, event: Event) -> None:
        """Handle data analysis requests."""
        dataset_id = event.data.get("dataset_id")
        
        # Retrieve data from memory
        dataset = await self.memory.get_items(dataset_id)
        if not dataset:
            return
        
        # Analyze data
        result = await self.execute_tool(
            "data_analysis",
            {"data": dataset.get("values", [])}
        )
        
        # Store results
        await self.memory.add_item(
            f"analysis_{dataset_id}",
            result
        )
        
        # Notify completion
        await self.event_bus.publish(
            Event(
                type="analysis_complete",
                data={
                    "dataset_id": dataset_id,
                    "results": result
                }
            )
        )

async def main():
    # Initialize agents
    collector = DataCollectorAgent()
    analyzer = AnalysisAgent()
    
    await collector.initialize()
    await analyzer.initialize()
    
    # Simulate data collection
    data_events = [
        Event(
            type="data_collection",
            data={"values": [1, 2, 3, 4, 5]}
        ),
        Event(
            type="data_collection",
            data={"values": [10, 20, 30, 40, 50]}
        )
    ]
    
    # Process events
    for event in data_events:
        print(f"\nProcessing data collection: {event.id}")
        await collector.handle_data(event)
        
        # Wait for analysis to complete
        await asyncio.sleep(1)
        
        # Check results
        analysis_result = await analyzer.memory.get_items(
            f"analysis_dataset_{event.id}"
        )
        print(f"Analysis results: {analysis_result}")

if __name__ == "__main__":
    # Configure settings
    settings.configure(
        redis_host="localhost",
        redis_port=6379,
        log_level="INFO"
    )
    
    # Run the example
    asyncio.run(main())
