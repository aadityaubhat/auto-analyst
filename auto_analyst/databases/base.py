from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import List


class BaseDatabase(ABC):
    """Abstract Base Class responsible for defining Database"""

    @abstractmethod
    def run_query(self, query: str) -> pd.DataFrame:
        """Run query"""
        raise NotImplementedError

    @abstractmethod
    def get_tables(self) -> List:
        """List tables"""
        raise NotImplementedError

    @abstractmethod
    def get_schema(self, table_name: str) -> pd.DataFrame:
        """Get schema for the given table"""
        raise NotImplementedError
