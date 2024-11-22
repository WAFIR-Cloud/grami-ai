import asyncio
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from growth_manager_agent import GrowthManagerAgent
from content_creation_agent import ContentCreationAgent
from scheduling_agent import SchedulingAgent
from execution_agent import ExecutionAgent
from base_agent import ProjectState

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def run_instagram_growth_workflow():
    """
    Simulate the complete Instagram growth workflow
    """
    # Step 1: Customer Onboarding (Growth Manager)
    growth_manager = GrowthManagerAgent()
    customer_details = {
        "customer_name": "TestClient",
        "account_type": "business",
        "target_audience": "Tech Professionals",
        "content_preferences": {
            "content_types": ["post", "reel", "story"],
            "themes": ["Technology", "Innovation"]
        },
        "scheduling_preferences": {
            "posting_interval": 2  # days between posts
        }
    }
    
    # Process customer requirements and initialize project
    logger.info("Starting customer onboarding...")
    project_state = await growth_manager.process_task(customer_details)
    logger.info(f"Project initialized with ID: {project_state.project_id}")
    
    # Step 2: Content Creation
    content_creator = ContentCreationAgent()
    logger.info("Starting content generation...")
    project_state = await content_creator.process_task({}, project_state)
    logger.info(f"Generated {len(project_state.media_assets)} content assets")
    
    # Step 3: Scheduling
    scheduling_agent = SchedulingAgent()
    logger.info("Creating posting schedule...")
    project_state = await scheduling_agent.process_task({}, project_state)
    logger.info("Posting schedule created")
    
    # Step 4: Execution
    execution_agent = ExecutionAgent()
    logger.info("Executing posting schedule...")
    project_state = await execution_agent.process_task({}, project_state)
    logger.info("Posting schedule executed")
    
    # Final project state summary
    logger.info("Instagram Growth Workflow Completed")
    logger.info(f"Project Stage: {project_state.current_stage}")
    logger.info(f"Team Progress: {project_state.team_progress}")
    
    return project_state

def main():
    """
    Main function to run the workflow
    """
    try:
        # Run the async workflow
        project_state = asyncio.run(run_instagram_growth_workflow())
        
        # Optional: Print execution results
        if hasattr(project_state, 'execution_results'):
            print("\nExecution Results:")
            for result in project_state.execution_results:
                print(f"Media Asset: {result['media_asset']['type']}")
                print(f"Performance Metrics: {result['performance_metrics']}\n")
        
        print("Workflow completed successfully!")
        return 0
    except Exception as e:
        print(f"Error running workflow: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
