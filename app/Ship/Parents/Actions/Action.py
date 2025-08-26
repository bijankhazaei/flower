from abc import ABC
from typing import Any

class Action(ABC):
    def run(self, *args, **kwargs) -> Any:
        pass