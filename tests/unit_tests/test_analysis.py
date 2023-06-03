from auto_analyst.analysis import Analysis
import pandas as pd
import plotly.express as px
import pytest
from uuid import uuid4
from auto_analyst.analysis import AnalysisStatus, AnalysisType


@pytest.fixture(scope="module")
def analysis():
    analysis = Analysis("What is the total revenue?", uuid4())
    yield analysis


def test_metadata(analysis):
    assert analysis.metadata == {}
    analysis.metadata = {"source_data": ["Invoice", "InvoiceLine"]}
    analysis.metadata = {"table_schema": {"Invoice": ["InvoiceId", "Total"]}}
    assert analysis.metadata == {
        "source_data": ["Invoice", "InvoiceLine"],
        "table_schema": {"Invoice": ["InvoiceId", "Total"]},
    }


def test_query(analysis):
    assert analysis.query is None
    analysis.query = "select * from Invoice"
    assert analysis.query == "select * from Invoice"


def test_result_data(analysis):
    assert analysis.result_data is None
    analysis.result_data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    assert analysis.result_data.equals(
        pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    )


def test_result_plot(analysis):
    assert analysis.result_plot is None
    analysis.result_plot = px.bar(
        x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23]
    )
    assert analysis.result_plot == px.bar(
        x=["giraffes", "orangutans", "monkeys"], y=[20, 14, 23]
    )


def test_analysis_type(analysis):
    assert analysis.analysis_type is None
    analysis.analysis_type = "query"
    assert analysis.analysis_type == AnalysisType.QUERY
    analysis.analysis_type = "data"
    assert analysis.analysis_type == AnalysisType.DATA
    analysis.analysis_type = "plot"
    assert analysis.analysis_type == AnalysisType.PLOT
    with pytest.raises(ValueError):
        analysis.analysis_type = "prediction"


def test_analysis_status(analysis):
    assert analysis.analysis_status == AnalysisStatus.INITIATED
    analysis.analysis_status = AnalysisStatus.COMPLETED
    assert analysis.analysis_status == AnalysisStatus.COMPLETED
    analysis.analysis_status = AnalysisStatus.FAILED
    assert analysis.analysis_status == AnalysisStatus.FAILED
