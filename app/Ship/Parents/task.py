from abc import ABC, abstractmethod
from typing import Any

class Task(ABC):
    @abstractmethod
    async def run(self, *args, **kwargs) -> Any:
        pass