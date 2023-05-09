from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import List


class BaseDataCatalog(ABC):
    """Class responsible for defining Data Catalog"""

    @abstractmethod
    def get_table_schemas(self, table_list: List[str]) -> List[pd.DataFrame]:
        """Get Table Schemas"""
        raise NotImplementedError

    @abstractmethod
    def get_source_tables(self, question: str) -> pd.DataFrame:
        """Get source tables for the given question"""
        raise NotImplementedError
