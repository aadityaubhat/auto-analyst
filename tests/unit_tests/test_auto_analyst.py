from flask import Flask
from auto_analyst.auto_analyst import AutoAnalyst
from auto_analyst.databases.sqlite import SQLLite
from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog
from auto_analyst.config_parser import parse_openai_api_key
from auto_analyst.llms.openai import OpenAILLM, Model
import pytest


@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    yield app


@pytest.fixture(scope="module")
def aa():
    driver_llm = OpenAILLM(parse_openai_api_key(), Model.GPT_3_5_TURBO)
    sample_db = SQLLite()
    sample_datacatalog = SampleDataCatalog(driver_llm)

    aa = AutoAnalyst(
        database=sample_db, datacatalog=sample_datacatalog, driver_llm=driver_llm
    )
    yield aa


@pytest.mark.llm
def test_analyze_query(aa, app):
    with app.app_context():
        analysis = aa.analyze("What is the total sales by country?")
        assert (
            analysis.query.lower()
            == """select c.country, sum(il.unitprice * il.quantity) as totalsales\nfrom customer c\njoin invoice i on c.customerid = i.customerid\njoin invoiceline il on i.invoiceid = il.invoiceid\ngroup by c.country;""".lower()
        )
