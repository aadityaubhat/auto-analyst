from typing import (
    Dict,
    Union,
    Any,
    Optional,
)
from plotly.graph_objs import Figure
import pandas as pd
from enum import Enum
import uuid
import plotly


class AnalysisStatus(Enum):
    """Class responsible for defining analysis status"""

    INITIATED = "initiated"
    QUESTION_TYPE_DONE = "determined question type"
    SOURCE_DATA_DONE = "determined source data"
    QUERY_DONE = "query done"
    RUNNING_QUERY = "running query"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisType(Enum):
    """Class responsible for defining analysis type"""

    QUERY = "query"
    DATA = "data"
    PLOT = "plot"


class Analysis:
    """Class responsible for defining analysis"""

    instances: Dict[uuid.UUID, "Analysis"] = {}

    def __init__(
        self, question: str, analysis_uuid: Union[uuid.UUID, None] = None
    ) -> None:
        self._question = question
        self._analysis_status = AnalysisStatus.INITIATED
        self._analysis_type: Optional[AnalysisType] = None
        self._metadata: Dict["str", Any] = {}
        self._query: Optional[str] = None
        self._result_data: Optional[pd.DataFrame] = None
        self._result_plot: Optional[Figure] = None

        if analysis_uuid is None:
            self._analysis_uuid = uuid.uuid4()
        else:
            self._analysis_uuid = analysis_uuid

        Analysis.instances[self._analysis_uuid] = self

    @property
    def analysis_uuid(self) -> uuid.UUID:
        """Get analysis UUID"""
        return self._analysis_uuid

    @property
    def analysis_status(self) -> AnalysisStatus:
        """Get analysis status"""
        return self._analysis_status

    @analysis_status.setter
    def analysis_status(self, analysis_status: AnalysisStatus) -> None:
        """Set analysis status"""
        self._analysis_status = analysis_status

    @property
    def metadata(self) -> Dict:
        """Get metadata"""
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: Dict) -> None:
        """Add metadata to the analysis"""
        self._metadata.update(metadata)

    @property
    def query(self) -> Optional[str]:
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
    def analysis_type(self) -> Optional[AnalysisType]:
        """Get analysis type"""
        return self._analysis_type

    @analysis_type.setter
    def analysis_type(self, analysis_type: str) -> None:
        """Set analysis type"""
        try:
            self._analysis_type = AnalysisType(analysis_type)
        except ValueError:
            raise ValueError(f"Invalid analysis type: {analysis_type}")

    def get_results(self) -> Dict:
        if isinstance(self.result_plot, plotly.graph_objs._figure.Figure):
            return {
                "result": {
                    "analysis_type": self.analysis_type,
                    "plot": self.result_plot.to_json(),
                    "data": self.result_data.to_dict(orient="records"),  # type: ignore
                    "query": self.query,
                }
            }
        elif isinstance(self.result_data, pd.DataFrame):
            return {
                "result": {
                    "analysis_type": self.analysis_type,
                    "data": self.result_data.to_dict(orient="records"),
                    "query": self.query,
                }
            }
        else:
            return {
                "result": {"analysis_type": self.analysis_type, "query": self.query}
            }

    def to_json(self) -> Dict:
        """Convert analysis to JSON"""
        return {
            "analysis_uuid": self.analysis_uuid,
            "analysis_type": self.analysis_type.value if self.analysis_type else None,
            "metadata": self.metadata,
            "query": self.query,
            "result_data": self.result_data.to_dict(orient="records")
            if isinstance(self.result_data, pd.DataFrame)
            else None,
            "result_plot": self.result_plot.to_json() if self.result_plot else None,
        }

    @classmethod
    def get_instance(cls, analysis_uuid: uuid.UUID) -> "Analysis":
        """Get analysis instance"""
        return Analysis.instances[analysis_uuid]
