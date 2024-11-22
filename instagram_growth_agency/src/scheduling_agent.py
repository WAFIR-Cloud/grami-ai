from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.base_agent import BaseDigitalMarketingAgent, AgentConfig, ProjectState

class SchedulingAgent(BaseDigitalMarketingAgent):
    """Agent responsible for creating optimal posting schedules"""
    
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="SchedulingSpecialist",
                role="scheduling_specialist",
                description="Creates optimal content posting schedules"
            )
        super().__init__(config)
    
    async def process_task(self, task: Dict[str, Any], project_state: ProjectState) -> ProjectState:
        """
        Create a posting schedule for generated content
        
        Args:
            task (Dict[str, Any]): Scheduling task details
            project_state (ProjectState): Current project state
        
        Returns:
            ProjectState: Updated project state with posting schedule
        """
        # Generate posting schedule based on customer preferences
        posting_schedule = await self.create_posting_schedule(
            project_state.media_assets, 
            project_state.customer_details.get('scheduling_preferences', {})
        )
        
        # Update project state with posting schedule
        project_state.posting_schedule = posting_schedule
        project_state.current_stage = "scheduling"
        project_state.team_progress["scheduling_specialist"] = "completed"
        
        # Communicate schedule creation
        await self.communicate_with_team(
            f"Posting schedule created for project {project_state.project_id}", 
            recipients=["growth_manager", "execution_specialist"]
        )
        
        # Update project state
        await self.update_project_state(project_state)
        
        return project_state
    
    async def create_posting_schedule(
        self, 
        media_assets: List[Dict[str, Any]], 
        scheduling_preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Create an optimal posting schedule for content
        
        Args:
            media_assets (List[Dict[str, Any]]): Generated content assets
            scheduling_preferences (Dict[str, Any]): Scheduling guidelines
        
        Returns:
            List[Dict[str, Any]]: Scheduled content posting times
        """
        # Determine posting interval (default to every 2 days)
        posting_interval = scheduling_preferences.get('posting_interval', 2)
        
        # Start scheduling from current time
        current_time = datetime.now()
        
        # Create schedule for each media asset
        posting_schedule = []
        for index, asset in enumerate(media_assets):
            scheduled_time = current_time + timedelta(days=index * posting_interval)
            
            schedule_entry = {
                "media_asset": asset,
                "scheduled_time": scheduled_time.isoformat(),
                "status": "pending",
                "best_time_score": 0.75  # Simulated best time to post score
            }
            
            posting_schedule.append(schedule_entry)
        
        return posting_schedule
