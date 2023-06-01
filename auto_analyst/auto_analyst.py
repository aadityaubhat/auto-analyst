from auto_analyst.databases.base import BaseDatabase
from auto_analyst.data_catalog.base import BaseDataCatalog
from auto_analyst.analysis import Analysis
import pandas as pd
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts import (
    render_type_messages,
    render_query_prompt,
    analysis_type_system_prompt,
    query_system_prompt,
    render_update_query_prompt,
)
import logging

from typing import (
    Dict,
    List,
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
        self.analysis = None
        self.query = None
        self.query_prompt = None
        self.query_retry_count = query_retry_count
        logger.info(
            f"Initalized AutoAnalyst with retry count: {self.query_retry_count}"
        )

    def _generate_query(
        self, question: str, source_data: List, table_schema: Dict, analysis_type: str
    ) -> None:
        """Generate query to answer the question"""
        self.query_prompt = render_query_prompt(
            question=question,
            source_data=source_data,
            table_schema=table_schema,
            analysis_type=analysis_type,
        )
        self.query = self.driver_llm.get_code(
            prompt=self.query_prompt,
            system_prompt=query_system_prompt,
        )

    def _update_query(self, error: str) -> None:
        """Update query to answer the question"""

        update_query_prompt = render_update_query_prompt(
            prompt=self.query_prompt,
            query=self.query,
            error=error,
        )
        logger.info(f"Update query prompt: {update_query_prompt}")
        self.query = self.driver_llm.get_code(
            query_system_prompt,
            update_query_prompt,
        )
        logger.info(f"Updated query: {self.query}")
        self.analysis.query = self.query

    def _run_query(self, retry_count: int = 0) -> pd.DataFrame:
        """Run query and return the result"""
        try:
            return self.database.run_query(self.query)
        except Exception as e:
            if retry_count > 0:
                self._update_query(error=str(e))
                return self._run_query(self.query, retry_count - 1)
            else:
                raise e

    def analyze(self, question: str) -> Analysis:
        """Analyze the question and return the analysis"""

        self.analysis = Analysis(question)
        logger.info(f"Analyzing question: {question}")

        # Determine whether the question can be answered using query, aggregate data or a plot
        analysis_type = self.driver_llm.get_reply(
            messages=render_type_messages(question)
        )
        logger.info(f"Analysis type: {analysis_type}")
        if analysis_type not in ["aggregation", "query", "plot"]:
            raise ValueError(
                f"Could not understand the question: {question} \n AutoAnalyst currently only supports Aggregations, Queries and Plots"
            )

        self.analysis.analysis_type = analysis_type

        # Determin source data
        source_tables_dscrptn = self.datacatalog.get_source_tables_and_description(
            question
        )
        self.analysis.metadata = {"source_data": source_tables_dscrptn}
        logger.info(f"Source tables: {source_tables_dscrptn}")

        source_tables = [tbl["table_name"] for tbl in source_tables_dscrptn]

        table_schema = self.datacatalog.get_table_schemas(source_tables)
        self.analysis.metadata = {
            "table_schema": {k: v.to_dict("records") for k, v in table_schema.items()}
        }
        logger.info(f"Table schema: {table_schema}")

        # Generate query
        self._generate_query(
            question=question,
            source_data=source_tables_dscrptn,
            table_schema=table_schema,
            analysis_type=analysis_type,
        )
        self.analysis.query = self.query

        if analysis_type == "aggregation":
            # Run query
            result_data = self._run_query(self.query_retry_count)
            self.analysis.result_data = result_data

        elif analysis_type == "plot":
            pass

        return self.analysis
