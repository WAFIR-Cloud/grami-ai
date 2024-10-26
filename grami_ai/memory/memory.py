from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractMemory(ABC):
    @abstractmethod
    async def add_item(self, chat_id: str, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def get_items(self, chat_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def clear_items(self, chat_id: str) -> None:
        pass
