from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import (
    List,
    Dict,
)


class BaseDataCatalog(ABC):
    """Class responsible for defining Data Catalog"""

    @abstractmethod
    def get_table_schemas(self, table_list: List[str]) -> List[pd.DataFrame]:
        """Get Table Schemas"""
        raise NotImplementedError

    @abstractmethod
    def get_source_tables_and_description(self, question: str) -> List[Dict]:
        """Get source tables for the given question"""
        raise NotImplementedError
