from abc import (
    abstractmethod,
    ABC,
)
from typing import Optional


class BaseLLM(ABC):
    """Base class responsible for defining LLM"""

    @abstractmethod
    def get_reply(self, prompt: Optional[str], **kwargs) -> str:
        """Get reply from LLM
        Args:
            prompt (Optional[str]): Prompt to be used for generating reply
        Returns:
            str: Reply from LLM"""
        raise NotImplementedError

    def get_code(self, prompt: Optional[str], **kwargs) -> str:
        """Get code from LLM
        Args:
            prompt (Optional[str]): Prompt to be used for generating code
        Returns:
            str: Code from LLM"""
        raise NotImplementedError
