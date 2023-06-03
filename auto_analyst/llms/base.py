from abc import (
    abstractmethod,
    ABC,
)
from typing import Optional


class BaseLLM(ABC):
    """Class responsible for defining LLM"""

    @abstractmethod
    def get_reply(self, prompt: Optional[str], **kwargs) -> str:
        """Get reply"""
        raise NotImplementedError

    def get_code(self, prompt: Optional[str], **kwargs) -> str:
        """Get code"""
        raise NotImplementedError
