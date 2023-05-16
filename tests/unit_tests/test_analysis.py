from auto_analyst.analysis import Analysis
import pandas as pd
import plotly.express as px
import pytest


@pytest.fixture(scope="module")
def analysis():
    analysis = Analysis("What is the total revenue?")
    yield analysis


def test_metadata(analysis):
    assert analysis.metadata == {}
    analysis.metadata = {"source_data": ["Invoice", "InvoiceLine"]}
    assert analysis.metadata == {"source_data": ["Invoice", "InvoiceLine"]}


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
    assert analysis.analysis_type == "query"
    analysis.analysis_type = "aggregation"
    assert analysis.analysis_type == "aggregation"
    analysis.analysis_type = "plot"
    assert analysis.analysis_type == "plot"
