"""Base implementation for tools or skills."""

from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import List


class BaseDatabase:
    """Class responsible for defining Database"""

    @abstractmethod
    def _connect(self):
        """Connect to database"""
        raise NotImplementedError

    @abstractmethod
    def _disconnect(self):
        """Disconnect from database"""
        raise NotImplementedError

    @abstractmethod
    def run_query(self, query: str) -> pd.DataFrame:
        """Run query"""
        raise NotImplementedError

    @abstractmethod
    def list_tables(self) -> List:
        """List tables"""
        raise NotImplementedError

    @abstractmethod
    def get_schema(self, table_name: str) -> pd.DataFrame:
        """Get schema for the given table"""
        raise NotImplementedError
