from typing import Dict, Any, List
from src.base_agent import BaseDigitalMarketingAgent, AgentConfig, ProjectState

class ContentCreationAgent(BaseDigitalMarketingAgent):
    """Agent responsible for generating media and textual content"""
    
    def __init__(self, config: AgentConfig = None):
        if config is None:
            config = AgentConfig(
                name="ContentCreator",
                role="content_creator",
                description="Generates media and textual content for Instagram growth"
            )
        super().__init__(config)
    
    async def process_task(self, task: Dict[str, Any], project_state: ProjectState) -> ProjectState:
        """
        Generate content based on project requirements
        
        Args:
            task (Dict[str, Any]): Content generation task details
            project_state (ProjectState): Current project state
        
        Returns:
            ProjectState: Updated project state with generated content
        """
        # Generate content based on customer preferences
        generated_content = await self.generate_content(
            project_state.customer_details.get('content_preferences', {})
        )
        
        # Update project state with new media assets
        project_state.media_assets.extend(generated_content)
        project_state.current_stage = "content_generation"
        project_state.team_progress["content_creator"] = "completed"
        
        # Communicate content generation completion
        await self.communicate_with_team(
            f"Content generated for project {project_state.project_id}", 
            recipients=["growth_manager", "scheduling_specialist"]
        )
        
        # Update project state
        await self.update_project_state(project_state)
        
        return project_state
    
    async def generate_content(self, content_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate diverse content for Instagram growth
        
        Args:
            content_preferences (Dict[str, Any]): Content generation guidelines
        
        Returns:
            List[Dict[str, Any]]: Generated content assets
        """
        # Placeholder for actual content generation logic
        # In a real implementation, this would use an LLM or specialized content generation service
        content_types = content_preferences.get('content_types', ['post', 'reel', 'story'])
        
        generated_content = []
        for content_type in content_types:
            content = {
                "type": content_type,
                "caption": f"AI-generated {content_type} for Instagram growth",
                "hashtags": ["#AIMarketing", "#InstagramGrowth"],
                "media_url": f"placeholder_url_for_{content_type}",
                "content_quality_score": 0.8  # Simulated content quality assessment
            }
            generated_content.append(content)
        
        return generated_content
