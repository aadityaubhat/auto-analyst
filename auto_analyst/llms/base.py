from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import List


class BaseLLM(ABC):
    """Class responsible for defining LLM"""

    @abstractmethod
    def get_reply(self, prompt):
        """Get reply"""
        raise NotImplementedError
