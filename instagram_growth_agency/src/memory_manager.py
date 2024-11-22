import json
import logging
from typing import Dict, Any, Optional
import redis.asyncio as redis
from datetime import timedelta

class ProjectMemoryManager:
    """
    Redis-based memory management for tracking project states and metadata.
    """
    
    def __init__(self, 
                 host: str = 'localhost', 
                 port: int = 6379, 
                 db: int = 0):
        """
        Initialize Redis connection for project memory management.
        
        Args:
            host (str): Redis server host
            port (int): Redis server port
            db (int): Redis database number
        """
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    
    async def save_project_state(self, 
                                  project_id: str, 
                                  state: Dict[str, Any], 
                                  ttl: Optional[int] = None):
        """
        Save project state to Redis.
        
        Args:
            project_id (str): Unique project identifier
            state (Dict[str, Any]): Project state dictionary
            ttl (Optional[int]): Time-to-live in seconds
        """
        try:
            key = f"project:{project_id}:state"
            state_json = json.dumps(state)
            
            await self.redis_client.set(key, state_json)
            
            if ttl:
                await self.redis_client.expire(key, timedelta(seconds=ttl))
            
            self.logger.info(f"Saved state for project {project_id}")
        except Exception as e:
            self.logger.error(f"Error saving project state: {e}")
    
    async def get_project_state(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve project state from Redis.
        
        Args:
            project_id (str): Unique project identifier
        
        Returns:
            Optional[Dict[str, Any]]: Project state or None
        """
        try:
            key = f"project:{project_id}:state"
            state_json = await self.redis_client.get(key)
            
            if state_json:
                return json.loads(state_json)
            
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving project state: {e}")
            return None
    
    async def update_project_stage(self, 
                                   project_id: str, 
                                   stage: str, 
                                   metadata: Optional[Dict[str, Any]] = None):
        """
        Update project stage and optional metadata.
        
        Args:
            project_id (str): Unique project identifier
            stage (str): Current project stage
            metadata (Optional[Dict[str, Any]]): Additional metadata
        """
        try:
            current_state = await self.get_project_state(project_id) or {}
            current_state['current_stage'] = stage
            
            if metadata:
                current_state.update(metadata)
            
            await self.save_project_state(project_id, current_state)
            
            self.logger.info(f"Updated project {project_id} to stage: {stage}")
        except Exception as e:
            self.logger.error(f"Error updating project stage: {e}")
    
    async def close(self):
        """Close Redis connection."""
        await self.redis_client.close()
