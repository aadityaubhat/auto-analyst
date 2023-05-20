from typing import (
    Dict,
    List,
    Union,
)
from plotly.graph_objs import Figure
import pandas as pd


class Analysis:
    def __init__(self, question: str) -> None:
        self._question = question
        self._analysis_type = None
        self._metadata = {}
        self._query = None
        self._result_data = None
        self._result_plot = None

    @property
    def metadata(self) -> Dict:
        """Get metadata"""
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Dict) -> None:
        """Add metadata to the analysis"""
        self._metadata.update(metadata)

    @property
    def query(self) -> str:
        """Get query"""
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        """Add query to the analysis"""
        self._query = query

    @property
    def result_data(self) -> Union[pd.DataFrame, None]:
        """Get result data"""
        return self._result_data

    @result_data.setter
    def result_data(self, result_data: Union[pd.DataFrame, None]) -> None:
        """Add result data to the analysis"""
        self._result_data = result_data

    @property
    def result_plot(self) -> Union[Figure, None]:
        """Get result plot"""
        return self._result_plot

    @result_plot.setter
    def result_plot(self, result_plot: Union[Figure, None]) -> None:
        """Add result plot to the analysis"""
        self._result_plot = result_plot

    @property
    def analysis_type(self) -> str:
        """Get analysis type"""
        return self._analysis_type

    @analysis_type.setter
    def analysis_type(self, analysis_type: str) -> None:
        """Set analysis type"""
        self._analysis_type = analysis_type

    def render_query(self) -> str:
        """Render the query"""
        return self.query

    def render_aggregation(self) -> str:
        """Render the aggregation"""
        return self.result_data.to_html()

    def render_plot(self) -> str:
        """Render the plot"""
        return self.result_plot.render_html()

    def render(self) -> str:
        """Render the analysis"""
        if self.analysis_type == "query":
            return self.render_query()
        if self.analysis_type == "aggregation":
            return self.render_aggregation()
        if self.analysis_type == "plot":
            return self.render_plot()
