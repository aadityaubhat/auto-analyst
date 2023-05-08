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
