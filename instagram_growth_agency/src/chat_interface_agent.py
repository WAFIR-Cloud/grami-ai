import asyncio
from typing import Dict, Any, Optional
from src.base_agent import BaseDigitalMarketingAgent, AgentConfig, ProjectState, CommunicationProtocol, AgentRole
import uuid

class ChatInterfaceAgent(BaseDigitalMarketingAgent):
    """
    Chat Interface Agent responsible for:
    1. Receiving customer requests
    2. Initializing project workflow
    3. Coordinating communication between agents
    4. Providing real-time updates to customers
    """
    
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="ChatInterface",
                role=AgentRole.GROWTH_MANAGER,
                description="Manages customer interactions and workflow coordination"
            )
        super().__init__(config)
        
        # Conversation state tracking
        self.active_conversations = {}
    
    async def process_communication(self, communication: CommunicationProtocol):
        """
        Process incoming communication from various sources
        
        Args:
            communication (CommunicationProtocol): Received communication
        """
        if communication.message_type == "customer_request":
            await self.handle_customer_request(communication)
        elif communication.message_type == "agent_update":
            await self.handle_agent_update(communication)
    
    async def handle_customer_request(self, communication: CommunicationProtocol):
        """
        Handle initial customer request and start workflow
        
        Args:
            communication (CommunicationProtocol): Customer request details
        """
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Create initial project state
        project_state = ProjectState(
            project_id=project_id,
            customer_details=communication.payload
        )
        
        # Store conversation state
        self.active_conversations[project_id] = {
            "customer_id": communication.sender,
            "project_state": project_state
        }
        
        # Notify Growth Manager to start project
        await self.publish_event(
            "growth_manager_tasks", 
            CommunicationProtocol(
                sender=self.config.name,
                recipient="growth_manager",
                message_type="start_project",
                payload=project_state.dict(),
                project_id=project_id
            )
        )
    
    async def handle_agent_update(self, communication: CommunicationProtocol):
        """
        Handle updates from various agents and relay to customer
        
        Args:
            communication (CommunicationProtocol): Agent update details
        """
        project_id = communication.project_id
        
        if project_id in self.active_conversations:
            # Update project state
            self.active_conversations[project_id]["project_state"] = ProjectState(**communication.payload)
            
            # Notify customer about progress
            await self.publish_event(
                "customer_notifications", 
                CommunicationProtocol(
                    sender=self.config.name,
                    recipient=self.active_conversations[project_id]["customer_id"],
                    message_type="project_update",
                    payload={
                        "stage": communication.payload.get("current_stage"),
                        "progress": communication.payload.get("team_progress")
                    },
                    project_id=project_id
                )
            )
    
    async def run(self):
        """
        Main event loop for chat interface agent
        """
        await self.initialize_communication_channels()
        
        # Start consuming events
        await self.consume_events()

def main():
    """Entry point for chat interface agent"""
    agent = ChatInterfaceAgent()
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
