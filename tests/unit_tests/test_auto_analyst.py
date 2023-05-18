from auto_analyst.auto_analyst_new import AutoAnalyst
from auto_analyst.databases.sqlite import SQLLite
from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog
from auto_analyst.config import OPENAI_API_KEY
from auto_analyst.llms.openai import OpenAILLM, Model
import pytest


@pytest.fixture(scope="module")
def aa():
    driver_llm = OpenAILLM(OPENAI_API_KEY, Model.GPT_3_5_TURBO)
    sample_db = SQLLite()
    sample_datacatalog = SampleDataCatalog(driver_llm)

    aa = AutoAnalyst(
        database=sample_db, datacatalog=sample_datacatalog, driver_llm=driver_llm
    )
    yield aa


@pytest.mark.llm
def test_analyze_query(aa):
    analysis = aa.analyze("What is the total sales by country?")
    assert (
        analysis.query.lower()
        == """select billingcountry, sum(total) as totalsales\nfrom invoice\ngroup by billingcountry""".lower()
    )


# driver_llm = OpenAILLM(OPENAI_API_KEY, Model.GPT_3_5_TURBO)
# sample_db = SQLLite()
# sample_datacatalog = SampleDataCatalog(driver_llm)

# aa = AutoAnalyst(
#     database=sample_db, datacatalog=sample_datacatalog, driver_llm=driver_llm
# )

# analysis = aa.analyze("What is the total sales by country?")

# print(analysis.query)
# print(analysis.result_data)
