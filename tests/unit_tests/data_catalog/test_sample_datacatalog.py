from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog
from auto_analyst.llms.openai import OpenAILLM, Model
from auto_analyst.config import OPENAI_API_KEY
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def sample_datacatalog():
    llm = OpenAILLM(OPENAI_API_KEY, Model.GPT_3_5_TURBO)
    sample_datacatalog = SampleDataCatalog(llm)
    yield sample_datacatalog


def test_get_source_tables(sample_datacatalog):
    question = "What is the total sales by country?"
    input_tables = sample_datacatalog.get_source_tables(question)
    print(input_tables)
    assert ["Invoice"] == [d["table_name"] for d in input_tables]


def test_get_table_schemas(sample_datacatalog):
    table_list = ["customer"]
    table_schemas = sample_datacatalog.get_table_schemas(table_list)
    assert table_schemas[0].equals(
        pd.DataFrame(
            {
                "cid": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                ],
                "name": [
                    "CustomerId",
                    "FirstName",
                    "LastName",
                    "Company",
                    "Address",
                    "City",
                    "State",
                    "Country",
                    "PostalCode",
                    "Phone",
                    "Fax",
                    "Email",
                    "SupportRepId",
                ],
                "type": [
                    "INTEGER",
                    "NVARCHAR(40)",
                    "NVARCHAR(20)",
                    "NVARCHAR(80)",
                    "NVARCHAR(70)",
                    "NVARCHAR(40)",
                    "NVARCHAR(40)",
                    "NVARCHAR(40)",
                    "NVARCHAR(10)",
                    "NVARCHAR(24)",
                    "NVARCHAR(24)",
                    "NVARCHAR(60)",
                    "INTEGER",
                ],
                "notnull": [
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    0,
                ],
                "dflt_value": [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                "pk": [
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            }
        )
    )


# llm = OpenAILLM(OPENAI_API_KEY, Model.GPT_4_0314)
# sample_datacatalog = SampleDataCatalog(llm)

# lst = sample_datacatalog.get_table_schemas(["customer"])
# print(sample_datacatalog.get_table_schemas(["customer"]))

# print(lst[0].to_dict("records"))

# print(lst[0].describe())