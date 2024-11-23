from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass
    
    @abstractmethod
    async def _call(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Execute the tool's functionality."""
        pass
    
    async def __call__(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Make the tool callable."""
        return await self._call(*args, **kwargs)
