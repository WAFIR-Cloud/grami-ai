from typing import Dict, Any
import uuid
from src.base_agent import BaseDigitalMarketingAgent, AgentConfig, ProjectState

class GrowthManagerAgent(BaseDigitalMarketingAgent):
    """Agent responsible for customer onboarding and project initialization"""
    
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="GrowthManager",
                role="growth_manager",
                description="Manages customer onboarding and project planning"
            )
        super().__init__(config)
    
    async def process_task(self, task: Dict[str, Any], project_state: ProjectState = None) -> ProjectState:
        """
        Process customer onboarding and create initial project plan
        
        Args:
            task (Dict[str, Any]): Customer details and requirements
            project_state (ProjectState, optional): Existing project state
        
        Returns:
            ProjectState: Initialized project state
        """
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Initialize project state
        project_state = ProjectState(
            project_id=project_id,
            customer_details=task,
            current_stage="onboarding",
            team_progress={
                "growth_manager": "completed",
                "content_creator": "pending",
                "scheduling_specialist": "pending",
                "execution_specialist": "pending"
            }
        )
        
        # Log project initialization
        self.logger.info(f"Initialized project {project_id} for customer: {task.get('customer_name')}")
        
        # Broadcast project initialization to team
        await self.communicate_with_team(
            f"New project initialized: {project_id}", 
            recipients=["content_creator", "scheduling_specialist"]
        )
        
        # Update project state in shared memory
        await self.update_project_state(project_state)
        
        return project_state
    
    async def collect_customer_requirements(self, customer_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect and process customer requirements
        
        Args:
            customer_input (Dict[str, Any]): Raw customer input
        
        Returns:
            Dict[str, Any]: Processed and structured customer requirements
        """
        # Use LLM to process and structure customer requirements
        # This is a placeholder for actual LLM interaction
        processed_requirements = {
            "account_type": customer_input.get("account_type", "business"),
            "target_audience": customer_input.get("target_audience", ""),
            "growth_goals": customer_input.get("growth_goals", {}),
            "content_preferences": customer_input.get("content_preferences", {})
        }
        
        return processed_requirements
