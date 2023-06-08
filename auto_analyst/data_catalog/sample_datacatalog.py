from auto_analyst.data_catalog.base import (
    BaseDataCatalog,
    Table,
)
from typing import (
    List,
    Dict,
    Optional,
)
import pandas as pd
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts.data_catalog import (
    render_source_tables_prompt,
    system_prompt,
)
from auto_analyst.databases.sqlite import SQLLite
import logging

logger = logging.getLogger(__name__)


class SampleDataCatalog(BaseDataCatalog):
    """Sample Data Catalog

    Attributes:
        llm (BaseLLM): Language Model Manager
        db (SQLLite): Database object"""

    def __init__(self, llm: BaseLLM):
        """Initialize Sample Data Catalog

        Args:
            llm (BaseLLM): Language Model Manager"""
        self.llm = llm
        self.db = SQLLite()

    def _get_all_tables(self) -> pd.DataFrame:
        """Get all tables
        Returns:
            pd.DataFrame: Dataframe containing all tables"""
        df_path = "auto_analyst/databases/sample_data/chinook_tables.csv"
        return pd.read_csv(df_path)

    def _get_table_schema(self, table_name: str) -> pd.DataFrame:
        """Get table schema

        Args:
            table_name (str): Name of the table
        Returns:
            pd.DataFrame: Dataframe containing table schema"""
        return self.db.get_schema(table_name)

    def get_source_tables(self, question: str) -> List[Optional[Table]]:
        """
        Get source tables for the given question returns empty list if no tables found

        Args:
            question (str): Question to be answered

        Returns:
            List[Dict]: List of tables [{table_name: str, table_description: str}, ...]
        """
        tables_df = self._get_all_tables()
        logger.info(f"Question: {question}")

        # Find the appropriate tables to answer the question
        response = self.llm.get_reply(
            system_prompt=system_prompt,
            prompt=render_source_tables_prompt(question, tables_df),
        )

        table_list: List[Optional[Table]] = []

        if response.lower().strip() == "no tables found":
            return table_list
        else:
            tables = [tbl.strip() for tbl in response.split(",")]
            logger.info(f"Tables: {tables}")
            logger.info(
                f"Length of tables DF: {len(tables_df[tables_df.table_name.isin(tables)])}"
            )
            logger.info(
                f"Length of tables DF: {len(tables_df[tables_df.table_name.isin(tables)])}"
            )

            for _, row in tables_df[tables_df.table_name.isin(tables)].iterrows():
                table_list.append(
                    Table(name=row.table_name, description=row.description)
                )

            return table_list

    def get_table_schemas(self, table_list: List[str]) -> Dict[str, pd.DataFrame]:
        """Get schema for schema

        Args:
            table_list (List[str]): List of table names
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of table schemas {table_name: table_schema}
        """
        result = {}
        for table in table_list:
            result[table] = self._get_table_schema(table)

        return result
