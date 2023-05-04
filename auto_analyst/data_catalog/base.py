from abc import (
    abstractmethod,
    ABC,
)
import pandas as pd
from typing import List

class BaseDataCatalog(ABC):
    """Class responsible for defining Data Catalog"""


    @abstractmethod
    def get_schemas(self) -> List[str]:
        """Run query"""
        raise NotImplementedError

    @abstractmethod
    def list_tables(self, schema: str) -> pd.DataFrame:
        """List tables"""
        raise NotImplementedError

    @abstractmethod
    def get_columns(self, table_name: str) -> pd.DataFrame:
        """Get schema for the given table"""
        raise NotImplementedError
