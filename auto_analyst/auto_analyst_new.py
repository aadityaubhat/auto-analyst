from auto_analyst.databases.base import BaseDatabase
from auto_analyst.data_catalog.base import BaseDataCatalog
from auto_analyst.analysis import Analysis
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts import render_type_messages

from typing import (
    Dict,
    List,
)


class AutoAnalyst:
    def __init__(
        self, database: BaseDatabase, datacatalog: BaseDataCatalog, driver_llm: BaseLLM
    ) -> None:
        self.database = database
        self.datacatalog = datacatalog
        self.driver_llm = driver_llm
        pass

    def _generate_query(
        self, question: str, source_data: List, table_schema: Dict
    ) -> str:
        pass

    def analyze(self, question: str) -> Analysis:
        """Analyze the question and return the analysis"""

        analysis = Analysis(question)

        # Determine whether the question can be answered using query, aggregate data or a plot
        analysis_type = self.driver_llm.get_reply(render_type_messages(question))

        # Determin source data
        source_tables = self.datacatalog.get_source_tables(question)
        analysis.add_metadata("source_data", source_tables)

        table_schema = self.datacatalog.get_table_schemas(source_tables)
        analysis.add_metadata("table_schema", table_schema)

        if analysis_type == "query":
            # Generate query
            query = self._generate_query(question, table_schema)
            analysis.set_query(query)

        elif analysis_type == "aggregation":
            pass

        elif analysis_type == "plot":
            pass
            # Run query
            result_data = self.database.run_query(query)
