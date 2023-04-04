import pandas as pd
import duckdb
from prompts.prompts import (
    render_sql_error_prompt,
    system_sql_prompt,
)
from llms.open_ai_utils import get_chat_reply


def execute_query(
    prompt: str, query: str, data_table: pd.DataFrame, retries=3
) -> pd.DataFrame:
    """
    Execute a query on the DuckDB database
    """

    for i in range(retries):
        try:
            result = duckdb.query(query).to_df()
            return result
        except Exception as e:
            print(e)
            new_prompt = render_sql_error_prompt(prompt=prompt, query=query, error=e)
            query = get_chat_reply(system_sql_prompt, new_prompt)

    raise Exception("Could not execute query")
