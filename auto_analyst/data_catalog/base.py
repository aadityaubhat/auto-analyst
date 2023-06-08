from abc import (
    abstractmethod,
    ABC,
)
from typing import (
    List,
    Dict,
    Optional,
)
from dataclasses import dataclass, field


@dataclass
class Column:
    """
    Class to represent a column in a table
    Attributes:
        name (str): Name of the column
        datatype (str): Datatype of the column
        description (Optional[str]): Description of the column
        cardinality (Optional[int]): Cardinality of the column
        unique_values (Optional[int]): Number of unique values in the column"""

    name: str
    datatype: str
    description: Optional[str] = field(default=None)
    cardinality: Optional[int] = field(default=None)
    unique_values: Optional[int] = field(default=None)

    def to_str(self) -> str:
        """
        Convert Column object to string
        Returns:
            str: String representation of the Column object
        """
        return f"Column(name={self.name}, datatype={self.datatype}, description={self.description}, cardinality={self.cardinality}, unique_values={self.unique_values})"


@dataclass
class Table:
    """
    Class to represent a table
    Attributes:
        name (str): Name of the table
        description (Optional[str]): Description of the table
        columns (List[Column]): List of columns in the table
    """

    name: str
    description: Optional[str] = field(default=None)
    columns: List[Column] = field(default_factory=list)

    def to_str(self) -> str:
        return f"{self.name} : {self.description}"


class BaseDataCatalog(ABC):
    """Abstract base class responsible for defining Data Catalog"""

    @abstractmethod
    def get_table_schemas(self, table_list: List[str]) -> Dict[str, str]:
        """Get Table Schemas for a given list of tables
        Args:
            table_list (List[str]): List of table names
        Returns:
            Dict[str, str]: Dictionary of table schemas {table_name: table_schema}"""
        raise NotImplementedError

    @abstractmethod
    def get_source_tables(self, question: str) -> List[Optional[Table]]:
        """Get source tables for the given question
        Args:
            question (str): Question to be answered
        Returns:
            List[Dict]: List of tables [{table_name: str, table_description: str}, ...]
        """
        raise NotImplementedError
