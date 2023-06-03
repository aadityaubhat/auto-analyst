import json
from auto_analyst.llms.openai import OpenAILLM, Model
from auto_analyst.databases.sqlite import SQLLite
from auto_analyst.data_catalog.sample_datacatalog import SampleDataCatalog


def parse_config():
    """Parses config and returns database, data catalog, driver LLM, auto_analyst_settings"""
    with open("auto_analyst/config.json") as f:
        config = json.load(f)

    # Parse LLM config
    llm_config = config.get("llms", {})

    if not llm_config:
        raise Exception("LLM config is required")

    driverllm_config = llm_config.get("driverllm", "")

    if not driverllm_config:
        raise Exception("Driver LLM config is required")

    data_catalog_config = llm_config.get("data_catalog_llm", "")

    if not data_catalog_config:
        raise Exception("Data Catalog LLM config is required")

    if driverllm_config.get("type", "") == "openai":
        driver_llm = OpenAILLM(
            api_key=driverllm_config.get("api_key", ""),
            model=Model[driverllm_config.get("model", "")],
        )
    else:
        raise Exception("Invalid Driver LLM type")

    if data_catalog_config.get("type", "") == "openai":
        data_catalog_llm = OpenAILLM(
            api_key=data_catalog_config.get("api_key", ""),
            model=Model[data_catalog_config.get("model", "")],
        )
    else:
        raise Exception("Invalid Data Catalog LLM type")

    # Parse database config
    database_config = config.get("database", "")

    if not database_config:
        raise Exception("Database config is required")

    if database_config.get("type", "") == "sqlite":
        database = SQLLite(database_config.get("database_path", ""))
    else:
        raise Exception("Invalid database type")

    # Parse data catalog config
    data_catalog_config = config.get("data_catalog", "")

    if not data_catalog_config:
        raise Exception("Data Catalog config is required")

    if data_catalog_config.get("type", "") == "sample":
        data_catalog = SampleDataCatalog(data_catalog_llm)

    auto_analyst_settings = config.get("auto_analyst_settings", {})

    if not auto_analyst_settings:
        raise Exception("Auto Analyst Settings are required")

    return database, data_catalog, driver_llm, auto_analyst_settings


def parse_openai_api_key():
    with open("auto_analyst/config.json") as f:
        config = json.load(f)
    llm_config = config.get("llms", {})
    driverllm_config = llm_config.get("driverllm", "")
    return driverllm_config.get("api_key", "")
