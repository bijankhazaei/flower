from abc import ABC, abstractmethod
from typing import Any

class Action(ABC):
    @abstractmethod
    async def run(self, *args, **kwargs) -> Any:
        pass