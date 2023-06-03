from auto_analyst.databases.base import BaseDatabase
from auto_analyst.data_catalog.base import BaseDataCatalog, Table
from auto_analyst.analysis import Analysis, AnalysisType
import pandas as pd
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts import (
    render_type_messages,
    render_query_prompt,
    query_system_prompt,
    render_update_query_prompt,
)
import logging

from typing import (
    Dict,
    List,
    Tuple,
)


logger = logging.getLogger(__name__)


class AutoAnalyst:
    def __init__(
        self,
        database: BaseDatabase,
        datacatalog: BaseDataCatalog,
        driver_llm: BaseLLM,
        query_retry_count: int = 0,
    ) -> None:
        self.database = database
        self.datacatalog = datacatalog
        self.driver_llm = driver_llm
        # self.analysis: Optional[Analysis] = None
        # self.query: Optional[str] = None
        # self.query_prompt: Optional[str] = None
        self.query_retry_count = query_retry_count
        logger.info(
            f"Initalized AutoAnalyst with retry count: {self.query_retry_count}"
        )

    def _generate_query(
        self,
        question: str,
        source_data: List[Table],
        table_schema: Dict,
        analysis_type: str,
    ) -> Tuple[str, str]:
        """Generate query to answer the question"""
        query_prompt = render_query_prompt(
            question=question,
            source_data=source_data,
            table_schema=table_schema,
            analysis_type=analysis_type,
        )
        query = self.driver_llm.get_code(
            prompt=query_prompt,
            system_prompt=query_system_prompt,
        )

        return query_prompt, query

    def _update_query(self, query: str, query_prompt: str, error: str) -> str:
        """Update query to answer the question"""

        update_query_prompt = render_update_query_prompt(
            prompt=query_prompt,
            query=query,
            error=error,
        )
        logger.info(f"Update query prompt: {update_query_prompt}")
        query = self.driver_llm.get_code(
            prompt=update_query_prompt,
            system_prompt=query_system_prompt,
        )
        logger.info(f"Updated query: {query}")
        return query  # Type: ignore

    def _run_query(
        self, query: str, query_prompt: str, retry_count: int = 0
    ) -> pd.DataFrame:
        """Run query and return the result"""
        try:
            return self.database.run_query(query)
        except Exception as e:
            if retry_count > 0:
                query = self._update_query(
                    query=query, query_prompt=query_prompt, error=str(e)
                )
                return self._run_query(
                    query=query, query_prompt=query_prompt, retry_count=retry_count - 1
                )
            else:
                raise e

    def analyze(self, question: str) -> Analysis:
        """Analyze the question and return the analysis"""

        analysis = Analysis(question)
        logger.info(f"Analyzing question: {question}")

        # Determine whether the question can be answered using query, aggregate data or a plot
        analysis_type = self.driver_llm.get_reply(
            messages=render_type_messages(question)
        )  # type: ignore
        logger.info(f"Analysis type: {analysis_type}")

        analysis.analysis_type = AnalysisType(analysis_type)

        # Determine source data
        source_tables = self.datacatalog.get_source_tables(question)
        if len(source_tables) == 0:
            raise ValueError("No source tables found")

        analysis.metadata = {"source_data": [tbl.to_str() for tbl in source_tables]}  # type: ignore
        logger.info(f"Source tables: {[tbl.to_str() for tbl in source_tables]}")  # type: ignore

        table_schema = self.datacatalog.get_table_schemas([tbl.name for tbl in source_tables])  # type: ignore
        analysis.metadata = {"table_schema": {k: v.to_dict(orient="records") for k, v in table_schema.items()}}  # type: ignore
        logger.info(f"Table schema: {table_schema}")

        # Generate query
        query_prompt, query = self._generate_query(
            question=question,
            source_data=source_tables,  # type: ignore
            table_schema=table_schema,
            analysis_type=analysis_type,
        )
        analysis.query = query

        if analysis_type == "data":
            # Run query
            result_data = self._run_query(
                query=query,
                query_prompt=query_prompt,
                retry_count=self.query_retry_count,
            )
            analysis.result_data = result_data

        elif analysis_type == "plot":
            pass

        return analysis
