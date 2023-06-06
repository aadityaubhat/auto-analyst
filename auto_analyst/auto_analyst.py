from auto_analyst.databases.base import BaseDatabase
from auto_analyst.data_catalog.base import BaseDataCatalog, Table
from auto_analyst.analysis import Analysis, AnalysisType
import pandas as pd
from auto_analyst.llms.base import BaseLLM
from auto_analyst.prompts import (
    render_type_messages,
    render_query_prompt,
    query_system_prompt,
    transformed_data_system_prompt,
    yes_no_system_prompt,
    plotly_system_prompt,
    render_update_query_prompt,
    render_transformed_data_prompt,
    render_plotly_code_prompt,
    render_plotly_code_check_prompt,
)
import logging
from plotly.graph_objs import Figure

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

    def _generate_data_query(
        self,
        question: str,
        source_data: List[Table],
        table_schema: Dict,
        analysis_type: str,
        transformed_data: str = "",
    ) -> Tuple[str, str]:
        """Generate query to answer the question"""
        query_prompt = render_query_prompt(
            question=question,
            source_data=source_data,
            table_schema=table_schema,
            analysis_type=analysis_type,
            transformed_data=transformed_data,
        )
        logger.info(f"Query prompt: {query_prompt}")
        query = self.driver_llm.get_code(
            prompt=query_prompt,
            system_prompt=query_system_prompt,
        )

        return query_prompt, query

    def _generate_plotly_code(
        self, question: str, transformed_data: str, retry_count: int = 1
    ) -> str:
        """Generate plotly code to plot the data"""
        plotly_code_prompt = render_plotly_code_prompt(
            question=question,
            transformed_data=transformed_data,
        )

        plotly_code = self.driver_llm.get_code(
            prompt=plotly_code_prompt,
            system_prompt=plotly_system_prompt,
        )

        plotly_code_check_prompt = render_plotly_code_check_prompt(
            code=plotly_code,
        )

        plotly_code_check = self.driver_llm.get_reply(
            prompt=plotly_code_check_prompt,
            system_prompt=yes_no_system_prompt,
        )

        if plotly_code_check.strip().lower() == "no":
            if retry_count > 0:
                plotly_code = self._generate_plotly_code(
                    question=question,
                    transformed_data=transformed_data,
                    retry_count=retry_count - 1,
                )
            else:
                raise ValueError("Plotly code generation failed")
        return plotly_code

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

    def _run_plotly_code(self, plotly_code: str, result_data: pd.DataFrame) -> Figure:
        namespace = {"result_data": result_data}
        plotly_code = plotly_code.replace("fig.show()", "")
        logger.info(f"Plotly code to be executed: {plotly_code}")
        exec(plotly_code, namespace)
        return namespace["fig"]  # type: ignore

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

        if analysis_type in ["query", "data"]:
            # Generate query
            query_prompt, query = self._generate_data_query(
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
            transformed_data = self.driver_llm.get_reply(
                prompt=render_transformed_data_prompt(
                    question=question,
                    source_data=source_tables,  # type: ignore
                    table_schema=table_schema,
                ),
                system_prompt=transformed_data_system_prompt,
            )

            query_prompt, query = self._generate_data_query(
                question=question,
                source_data=source_tables,  # type: ignore
                table_schema=table_schema,
                analysis_type=analysis_type,
                transformed_data=transformed_data,
            )

            result_data = self._run_query(
                query=query,
                query_prompt=query_prompt,
                retry_count=self.query_retry_count,
            )
            analysis.result_data = result_data

            # Generate plotting code
            plotly_code = self._generate_plotly_code(
                question=question,
                transformed_data=transformed_data,
            )

            fig = self._run_plotly_code(
                plotly_code=plotly_code, result_data=result_data
            )
            analysis.result_plot = fig
        return analysis
