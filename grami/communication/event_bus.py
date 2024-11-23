import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

class EventBus:
    """
    An asynchronous event bus for managing publish-subscribe communication.
    
    Allows decoupled event handling and message routing between components.
    """
    
    def __init__(self, agent: Optional[Any] = None):
        """
        Initialize the event bus.
        
        Args:
            agent (Optional[Any]): Agent to process messages, if provided
        """
        self.subscribers: Dict[str, List[Callable]] = {}
        self.agent = agent
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe a handler to a specific event type.
        
        Args:
            event_type (str): Type of event to subscribe to
            handler (Callable): Function to handle the event
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event_type: str, data: Any):
        """
        Publish an event to all subscribers.
        
        Args:
            event_type (str): Type of event being published
            data (Any): Event payload
        """
        if event_type not in self.subscribers:
            self.logger.warning(f"No subscribers for event type: {event_type}")
            return
        
        # Process agent message if agent is provided
        if event_type == 'user_message' and self.agent:
            try:
                response = await self.agent.send_message(data)
                await self.publish('agent_response', response)
            except Exception as e:
                self.logger.error(f"Error processing agent message: {e}")
        
        # Call all event handlers
        for handler in self.subscribers[event_type]:
            try:
                await handler(data)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event_type}: {e}")
    
    async def start(self):
        """
        Start event bus processing.
        Useful for long-running event processing tasks.
        """
        while True:
            # Keep the event bus running
            await asyncio.sleep(1)

# Example usage
async def example_event_handler(message):
    """
    Example event handler demonstrating basic event processing.
    
    :param message: Incoming message
    """
    print(f"Received message: {message}")

async def main():
    """
    Demonstration of event bus usage.
    """
    # Create an event bus
    event_bus = EventBus()
    
    # Subscribe to events
    event_bus.subscribe('user_message', example_event_handler)
    
    # Publish an event
    await event_bus.publish('user_message', 'Hello, world!')
    
    # Start processing events
    await event_bus.start()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
