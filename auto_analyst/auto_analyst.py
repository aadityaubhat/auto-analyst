from auto_analyst.databases.base import BaseDatabase
from auto_analyst.data_catalog.base import BaseDataCatalog
from auto_analyst.analysis import Analysis
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts import (
    render_type_messages,
    render_query_prompt,
    analysis_type_system_prompt,
)
import logging

from typing import (
    Dict,
    List,
)


logger = logging.getLogger(__name__)


class AutoAnalyst:
    def __init__(
        self, database: BaseDatabase, datacatalog: BaseDataCatalog, driver_llm: BaseLLM
    ) -> None:
        self.database = database
        self.datacatalog = datacatalog
        self.driver_llm = driver_llm

    def _generate_query(
        self, question: str, source_data: List, table_schema: Dict, analysis_type: str
    ) -> str:
        """Generate query to answer the question"""
        query_prompt = render_query_prompt(
            question=question,
            source_data=source_data,
            table_schema=table_schema,
            analysis_type=analysis_type,
        )
        query = self.driver_llm.get_code(
            prompt=query_prompt, system_prompt=analysis_type_system_prompt
        )
        return query

    def analyze(self, question: str) -> Analysis:
        """Analyze the question and return the analysis"""

        analysis = Analysis(question)
        logger.info(f"Analyzing question: {question}")

        # Determine whether the question can be answered using query, aggregate data or a plot
        analysis_type = self.driver_llm.get_reply(
            messages=render_type_messages(question)
        )
        logger.info(f"Analysis type: {analysis_type}")

        # Determin source data
        source_tables_dscrptn = self.datacatalog.get_source_tables_and_description(
            question
        )
        analysis.metadata = {"source_data": source_tables_dscrptn}
        logger.info(f"Source tables: {source_tables_dscrptn}")

        source_tables = [tbl["table_name"] for tbl in source_tables_dscrptn]

        table_schema = self.datacatalog.get_table_schemas(source_tables)
        analysis.metadata = {"table_schema": table_schema}
        logger.info(f"Table schema: {table_schema}")

        if analysis_type == "query":
            # Generate query
            query = self._generate_query(
                question=question,
                source_data=source_tables_dscrptn,
                table_schema=table_schema,
                analysis_type=analysis_type,
            )
            analysis.query = query

        elif analysis_type == "aggregation":
            # Generate query
            query = self._generate_query(
                question=question,
                source_data=source_tables_dscrptn,
                table_schema=table_schema,
                analysis_type=analysis_type,
            )
            analysis.query = query

            # Run query
            result_data = self.database.run_query(query)
            analysis.result_data = result_data

        elif analysis_type == "plot":
            pass

        return analysis
