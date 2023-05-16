from auto_analyst.data_catalog.base import BaseDataCatalog
from typing import (
    List,
    Dict,
)
import pandas as pd
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts.data_catalog import (
    render_source_tables_prompt,
    system_prompt,
)
from auto_analyst.databases.sqlite import SQLLite


class SampleDataCatalog(BaseDataCatalog):
    """Sample Data Catalog"""

    def __init__(self, llm: BaseLLM):
        """Initialize Sample Data Catalog"""
        self.llm = llm
        self.db = SQLLite()

    def _get_all_tables(self) -> pd.DataFrame:
        """Get all tables"""
        df_path = "auto_analyst/databases/sample_data/chinook_tables.csv"
        return pd.read_csv(df_path)

    def _get_table_schema(self, table_name: str) -> pd.DataFrame:
        """Get table schema"""
        return self.db.get_schema(table_name)

    def get_source_tables_and_description(self, question: str) -> List[Dict]:
        """
        Get source tables for the given question returns empty list if no tables found

        Args:
            question (str): Question to be answered

        Returns:
            List[Dict]: List of tables [{table_name: str, table_description: str}, ...]
        """
        tables_df = self._get_all_tables()

        # Find the appropriate tables to answer the question
        response = self.llm.get_reply(
            system_prompt=system_prompt,
            prompt=render_source_tables_prompt(question, tables_df),
        )

        if response == "No Tables Found":
            return []
        else:
            table_list = [tbl for tbl in response.split(",")]
            return tables_df[tables_df.table_name.isin(table_list)].to_dict("records")

    def get_table_schemas(self, table_list: List[str]) -> Dict[str, pd.DataFrame]:
        """Get schema for schema"""
        result = {}
        for table in table_list:
            result[table] = self._get_table_schema(table)

        return result
