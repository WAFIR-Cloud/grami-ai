import asyncio
import pytest
from grami_ai.agents.agent import AsyncAgent
from grami_ai.llms.gemini_llm import GeminiLLMProvider
from grami_ai.memory.memory import InMemoryAbstractMemory
from grami_ai.events.KafkaEvents import KafkaEvents
from grami_ai.tools.base_tools import AbstractTool

class DummyTool(AbstractTool):
    def __init__(self):
        super().__init__(
            name="dummy_tool", 
            description="A dummy tool for testing"
        )
    
    async def run(self, *args, **kwargs):
        return {"result": "dummy tool executed"}

@pytest.mark.asyncio
async def test_gemini_agent_creation():
    """
    Test creating an AsyncAgent with Gemini LLM
    """
    # Initialize LLM Provider
    llm_provider = GeminiLLMProvider()
    
    # Create Agent with a dummy tool
    agent = AsyncAgent(
        name="TestGeminiAgent",
        tools=[DummyTool()],
        memory=InMemoryAbstractMemory(),
        kafka=KafkaEvents(),
        llm_provider=llm_provider
    )
    
    # Start the agent
    await agent.start()
    
    # Test LLM generation
    response = await agent.llm.generate("Write a short poem about AI")
    
    # Assertions
    assert response is not None
    assert len(response) > 0
    
    # Stop the agent
    await agent.stop()
