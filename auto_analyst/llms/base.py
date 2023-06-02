from abc import (
    abstractmethod,
    ABC,
)


class BaseLLM(ABC):
    """Class responsible for defining LLM"""

    @abstractmethod
    def get_reply(self, prompt, **kwargs):
        """Get reply"""
        raise NotImplementedError
