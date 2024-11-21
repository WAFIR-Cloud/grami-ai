"""Tests for GRAMI AI event system."""

import pytest
from typing import Dict, Any, List
from unittest.mock import AsyncMock, patch

from grami_ai.events import (
    Event,
    EventHandler,
    EventBus,
    EventType,
    Priority
)
from grami_ai.core.exceptions import EventError

class MockEventHandler(EventHandler):
    """Mock event handler for testing."""
    
    def __init__(self):
        super().__init__()
        self.handled_events: List[Event] = []
    
    async def handle_event(self, event: Event) -> None:
        self.handled_events.append(event)

class TestEventSystem:
    """Test suite for the event system."""
    
    @pytest.fixture
    def event_bus(self):
        """Create a test event bus instance."""
        return EventBus()

    @pytest.fixture
    def mock_handler(self):
        """Create a mock event handler."""
        return MockEventHandler()

    def test_event_creation(self):
        """Test event object creation."""
        event_data = {"key": "value"}
        event = Event(
            type=EventType.TASK_CREATED,
            data=event_data,
            priority=Priority.HIGH
        )
        
        assert event.type == EventType.TASK_CREATED
        assert event.data == event_data
        assert event.priority == Priority.HIGH
        assert event.timestamp is not None

    @pytest.mark.asyncio
    async def test_event_handler_registration(self, event_bus, mock_handler):
        """Test event handler registration."""
        event_bus.register_handler(
            EventType.TASK_CREATED,
            mock_handler
        )
        
        assert len(event_bus.handlers[EventType.TASK_CREATED]) == 1
        assert event_bus.handlers[EventType.TASK_CREATED][0] == mock_handler

    @pytest.mark.asyncio
    async def test_event_publishing(self, event_bus, mock_handler):
        """Test event publishing."""
        event_bus.register_handler(
            EventType.TASK_CREATED,
            mock_handler
        )
        
        event = Event(
            type=EventType.TASK_CREATED,
            data={"test": "data"}
        )
        
        await event_bus.publish(event)
        assert len(mock_handler.handled_events) == 1
        assert mock_handler.handled_events[0] == event

    @pytest.mark.asyncio
    async def test_multiple_handlers(self, event_bus):
        """Test multiple handlers for same event type."""
        handler1 = MockEventHandler()
        handler2 = MockEventHandler()
        
        event_bus.register_handler(EventType.TASK_CREATED, handler1)
        event_bus.register_handler(EventType.TASK_CREATED, handler2)
        
        event = Event(
            type=EventType.TASK_CREATED,
            data={"test": "data"}
        )
        
        await event_bus.publish(event)
        assert len(handler1.handled_events) == 1
        assert len(handler2.handled_events) == 1

    @pytest.mark.asyncio
    async def test_handler_error_handling(self, event_bus):
        """Test error handling in event handlers."""
        async def failing_handler(event: Event):
            raise Exception("Handler error")
        
        handler = AsyncMock(side_effect=failing_handler)
        event_bus.register_handler(EventType.TASK_CREATED, handler)
        
        event = Event(
            type=EventType.TASK_CREATED,
            data={"test": "data"}
        )
        
        with pytest.raises(EventError):
            await event_bus.publish(event)

    @pytest.mark.asyncio
    async def test_event_priority_handling(self, event_bus, mock_handler):
        """Test event priority handling."""
        event_bus.register_handler(EventType.TASK_CREATED, mock_handler)
        
        high_priority_event = Event(
            type=EventType.TASK_CREATED,
            data={"priority": "high"},
            priority=Priority.HIGH
        )
        
        low_priority_event = Event(
            type=EventType.TASK_CREATED,
            data={"priority": "low"},
            priority=Priority.LOW
        )
        
        # Publish events in reverse priority order
        await event_bus.publish(low_priority_event)
        await event_bus.publish(high_priority_event)
        
        # Verify they were handled in priority order
        assert mock_handler.handled_events[0].priority == Priority.HIGH
        assert mock_handler.handled_events[1].priority == Priority.LOW

    @pytest.mark.asyncio
    async def test_handler_unregistration(self, event_bus, mock_handler):
        """Test handler unregistration."""
        event_bus.register_handler(EventType.TASK_CREATED, mock_handler)
        event_bus.unregister_handler(EventType.TASK_CREATED, mock_handler)
        
        event = Event(
            type=EventType.TASK_CREATED,
            data={"test": "data"}
        )
        
        await event_bus.publish(event)
        assert len(mock_handler.handled_events) == 0

    @pytest.mark.asyncio
    async def test_event_filtering(self, event_bus, mock_handler):
        """Test event filtering."""
        event_bus.register_handler(
            EventType.TASK_CREATED,
            mock_handler,
            lambda e: e.data.get("important", False)
        )
        
        important_event = Event(
            type=EventType.TASK_CREATED,
            data={"important": True}
        )
        
        unimportant_event = Event(
            type=EventType.TASK_CREATED,
            data={"important": False}
        )
        
        await event_bus.publish(important_event)
        await event_bus.publish(unimportant_event)
        
        assert len(mock_handler.handled_events) == 1
        assert mock_handler.handled_events[0] == important_event
