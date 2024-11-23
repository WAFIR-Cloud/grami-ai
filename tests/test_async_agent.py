"""
Comprehensive Test Suite for AsyncAgent

This test suite covers the core functionality of the AsyncAgent framework.
"""

import asyncio
import pytest
from typing import List, Dict, Any

from grami_ai.core.agent import (
    AsyncAgent, 
    AgentConfig, 
    AgentType, 
    AgentGoal,
    AgentPrompt
)
from grami_ai.llms.gemini import GeminiLLMProvider
from grami_ai.core.memory import AsyncMemory, AsyncInMemoryMemory
from grami_ai.tools.base import AsyncBaseTool
from grami_ai.tools.search import WebSearchTool
from grami_ai.tools.calculator import CalculatorTool

@pytest.mark.asyncio
class TestAsyncAgent:
    """Test suite for AsyncAgent"""
    
    async def test_agent_initialization(self):
        """
        Test basic agent initialization
        """
        # Prepare configuration
        config = AgentConfig(
            name="ResearchAgent",
            type=AgentType.RESEARCH,
            llm_provider=GeminiLLMProvider(),
            tools=[
                WebSearchTool(),
                CalculatorTool()
            ],
            prompt=AgentPrompt(
                system_prompt="You are a helpful research assistant.",
                temperature=0.7
            )
        )
        
        # Create agent
        agent = AsyncAgent(config)
        
        # Assertions
        assert agent.name == "ResearchAgent"
        assert agent.config.type == AgentType.RESEARCH
        assert len(agent.tools) == 2
        assert isinstance(agent.llm, GeminiLLMProvider)
    
    async def test_goal_processing(self):
        """
        Test goal processing functionality
        """
        # Prepare configuration
        config = AgentConfig(
            llm_provider=GeminiLLMProvider(),
            goals=[
                AgentGoal(
                    description="Research AI ethics",
                    success_criteria=["Comprehensive analysis"],
                    priority=8
                )
            ],
            prompt=AgentPrompt(
                system_prompt="You are an AI ethics researcher.",
                temperature=0.5
            )
        )
        
        # Create agent
        agent = AsyncAgent(config)
        
        # Process goal
        result = await agent.process_goal(
            "Investigate ethical implications of AI in healthcare"
        )
        
        # Assertions
        assert isinstance(result, dict)
        assert "goal" in result
        assert "strategy" in result
        assert result["goal"]["description"] == "Investigate ethical implications of AI in healthcare"
    
    async def test_communication(self):
        """
        Test agent communication with streaming
        """
        # Prepare configuration
        config = AgentConfig(
            llm_provider=GeminiLLMProvider(),
            prompt=AgentPrompt(
                system_prompt="You are a helpful AI assistant.",
                temperature=0.6
            )
        )
        
        # Create agent
        agent = AsyncAgent(config)
        
        # Collect streaming chunks
        chunks = []
        async for chunk in agent.communicate("Explain the basics of quantum computing"):
            chunks.append(chunk)
        
        # Assertions
        assert len(chunks) > 0
        assert isinstance("".join(chunks), str)
    
    async def test_tool_management(self):
        """
        Test dynamic tool addition and validation
        """
        # Prepare configuration
        config = AgentConfig(
            llm_provider=GeminiLLMProvider()
        )
        
        # Create agent
        agent = AsyncAgent(config)
        
        # Add tool
        web_search_tool = WebSearchTool()
        await agent.add_tool(web_search_tool)
        
        # Assertions
        assert len(agent.tools) == 1
        assert agent.tools[0].name == "web_search"
    
    async def test_agent_initialization_with_memory(self):
        """
        Test agent initialization with custom memory
        """
        # Prepare configuration with custom memory
        custom_memory = AsyncInMemoryMemory()
        config = AgentConfig(
            name="MemoryAgent",
            llm_provider=GeminiLLMProvider(),
            memory=custom_memory,
            prompt=AgentPrompt(
                system_prompt="You have advanced memory capabilities.",
                temperature=0.4
            )
        )
        
        # Create and initialize agent
        agent = AsyncAgent(config)
        await agent.initialize()
        
        # Assertions
        assert agent.memory == custom_memory
        assert agent.name == "MemoryAgent"
    
    async def test_agent_close(self):
        """
        Test graceful agent resource closure
        """
        # Prepare configuration
        config = AgentConfig(
            llm_provider=GeminiLLMProvider(),
            prompt=AgentPrompt(
                system_prompt="You are a temporary agent.",
                temperature=0.3
            )
        )
        
        # Create agent
        agent = AsyncAgent(config)
        
        # Close agent (should not raise exceptions)
        try:
            await agent.close()
        except Exception as e:
            pytest.fail(f"Agent closure failed: {e}")

# Pytest configuration for async tests
def pytest_configure(config):
    """Configure pytest for async testing"""
    config.addinivalue_line(
        "markers", 
        "asyncio: mark test as an async test"
    )
