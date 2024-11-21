"""Tests for GRAMI AI agent functionality."""

import pytest
from typing import Dict, Any, List
from unittest.mock import AsyncMock, patch

from grami_ai.agent import BaseAgent, Tool
from grami_ai.core.exceptions import ValidationError, ExecutionError
from grami_ai.memory import InMemoryAbstractMemory

class MockTool(Tool):
    """Mock tool for testing."""
    
    def __init__(self):
        super().__init__(
            name="mock_tool",
            description="A mock tool for testing",
            parameters={
                "param1": {"type": "string", "description": "Test parameter"}
            }
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        return {"result": f"Executed with {kwargs.get('param1', '')}"}

class TestBaseAgent:
    """Test suite for the BaseAgent class."""
    
    @pytest.fixture
    async def agent(self, mock_llm_provider):
        """Create a test agent instance."""
        memory = InMemoryAbstractMemory()
        agent = BaseAgent(
            name="test_agent",
            description="Test agent",
            llm_provider=mock_llm_provider,
            memory=memory,
            tools=[MockTool()]
        )
        return agent

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "test_agent"
        assert agent.description == "Test agent"
        assert len(agent.tools) == 1
        assert isinstance(agent.tools[0], MockTool)

    @pytest.mark.asyncio
    async def test_agent_tool_execution(self, agent):
        """Test tool execution through agent."""
        result = await agent.execute_tool(
            "mock_tool",
            {"param1": "test_value"}
        )
        assert result["result"] == "Executed with test_value"

        with pytest.raises(ValidationError):
            await agent.execute_tool(
                "nonexistent_tool",
                {"param1": "test"}
            )

    @pytest.mark.asyncio
    async def test_agent_memory_interaction(self, agent):
        """Test agent memory interactions."""
        conversation_id = "test_conv"
        message = {"role": "user", "content": "Hello"}
        
        await agent.memory.add_item(conversation_id, message)
        history = await agent.memory.get_items(conversation_id)
        
        assert len(history) == 1
        assert history[0] == message

    @pytest.mark.asyncio
    async def test_agent_conversation(self, agent):
        """Test agent conversation handling."""
        conversation_id = "test_conv"
        user_message = "Can you help me?"
        
        response = await agent.process_message(
            conversation_id,
            user_message
        )
        
        assert response is not None
        history = await agent.memory.get_items(conversation_id)
        assert len(history) == 2  # User message + agent response

    @pytest.mark.asyncio
    async def test_agent_error_handling(self, agent):
        """Test agent error handling."""
        with pytest.raises(ValidationError):
            await agent.execute_tool(
                "mock_tool",
                {"invalid_param": "value"}
            )

        with patch.object(MockTool, 'execute', side_effect=Exception("Test error")):
            with pytest.raises(ExecutionError):
                await agent.execute_tool(
                    "mock_tool",
                    {"param1": "test"}
                )

    @pytest.mark.asyncio
    async def test_agent_tool_validation(self, agent):
        """Test tool parameter validation."""
        # Valid parameters
        result = await agent.validate_tool_params(
            "mock_tool",
            {"param1": "valid_value"}
        )
        assert result is True

        # Invalid parameters
        with pytest.raises(ValidationError):
            await agent.validate_tool_params(
                "mock_tool",
                {"invalid_param": "value"}
            )

    @pytest.mark.asyncio
    async def test_agent_conversation_context(self, agent):
        """Test conversation context handling."""
        conversation_id = "test_conv"
        
        # Add some context
        context = {"key": "value"}
        await agent.set_conversation_context(
            conversation_id,
            context
        )
        
        # Verify context is used
        stored_context = await agent.get_conversation_context(
            conversation_id
        )
        assert stored_context == context

    @pytest.mark.asyncio
    async def test_agent_tool_list(self, agent):
        """Test tool listing and information."""
        tools = agent.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "mock_tool"
        assert "description" in tools[0]
        assert "parameters" in tools[0]

    @pytest.mark.asyncio
    async def test_agent_conversation_cleanup(self, agent):
        """Test conversation cleanup."""
        conversation_id = "test_conv"
        message = {"role": "user", "content": "Hello"}
        
        await agent.memory.add_item(conversation_id, message)
        await agent.cleanup_conversation(conversation_id)
        
        history = await agent.memory.get_items(conversation_id)
        assert len(history) == 0
