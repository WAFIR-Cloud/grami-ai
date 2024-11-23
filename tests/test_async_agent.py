import pytest
import asyncio
from typing import Dict, Any, Optional
from grami.agent import AsyncAgent

class TestAsyncAgent:
    @pytest.mark.asyncio
    async def test_async_agent_initialization(self):
        """Test basic initialization of AsyncAgent"""
        agent = AsyncAgent(
            name="TestAgent",
            description="A test agent for AsyncAgent",
            role="Tester"
        )
        
        assert agent.name == "TestAgent"
        assert agent.description == "A test agent for AsyncAgent"
        assert agent.role == "Tester"
    
    @pytest.mark.asyncio
    async def test_dynamic_configuration(self):
        """Test dynamic configuration of AsyncAgent"""
        config = {
            "max_iterations": 5,
            "temperature": 0.7,
            "verbose": True
        }
        
        agent = AsyncAgent(
            name="ConfigurableAgent",
            config=config
        )
        
        assert agent.config == config
        assert agent.config.get("max_iterations") == 5
        assert agent.config.get("temperature") == 0.7
        assert agent.config.get("verbose") is True
    
    @pytest.mark.asyncio
    async def test_update_configuration(self):
        """Test updating agent configuration dynamically"""
        agent = AsyncAgent(name="DynamicAgent")
        
        # Initial configuration
        assert agent.config == {}
        
        # Update configuration
        await agent.update_config({
            "context_window": 4096,
            "model": "gpt-4"
        })
        
        assert agent.config.get("context_window") == 4096
        assert agent.config.get("model") == "gpt-4"
    
    @pytest.mark.asyncio
    async def test_async_method_execution(self):
        """Test async method execution capability"""
        class TestAsyncMethod(AsyncAgent):
            async def async_task(self, input_data: str) -> str:
                await asyncio.sleep(0.1)  # Simulate async work
                return f"Processed: {input_data}"
        
        agent = TestAsyncMethod(name="AsyncMethodAgent")
        result = await agent.async_task("test input")
        
        assert result == "Processed: test input"
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in AsyncAgent"""
        class ErrorHandlingAgent(AsyncAgent):
            async def risky_method(self):
                raise ValueError("Test error")
        
        agent = ErrorHandlingAgent(name="ErrorAgent")
        
        with pytest.raises(ValueError, match="Test error"):
            await agent.risky_method()
