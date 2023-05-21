#! /Users/aadityabhat/Documents/autoanalyst/venv/bin/python

from llms.open_ai_utils import get_chat_reply
from prompts.prompts import (
    render_agg_plot_prompt,
    render_analytical_prompt,
    render_data_prompt,
    render_sql_prompt,
    render_plotly_prompt,
    render_transform_prompt,
    system_prompt,
    system_sql_prompt,
    system_plotly_prompt,
    system_transform_prompt,
    system_yes_no_prompt,
)
import pandas as pd
import logging
from files.csv_utils import clean_df
from files.file_sql import execute_query

logger = logging.getLogger(__name__)


def analyze(question: str, description, data_df: pd.DataFrame) -> str:
    """
    Analyze the question and return the answer
    """
    data_df = clean_df(data_df)

    # Determine whether the question can be answered using aggregate data or a plot
    agg_plot = get_chat_reply(system_prompt, render_agg_plot_prompt(question))
    if agg_plot == "aggregate":
        sql_prompt = render_sql_prompt(
            table_name="data_table",
            description=description,
            schema=data_df.dtypes,
            sample_data=data_df.head(),
            question=question,
        )

        print(f"SQL prompt: {sql_prompt}")
        sql_query = get_chat_reply(system_sql_prompt, sql_prompt)

        print(f"SQL query: {sql_query}")
        result = execute_query(prompt=sql_prompt, query=sql_query, data_table=data_df)

        return result

    elif agg_plot == "plot":
        transformation_prompt = render_transform_prompt(
            table_name="data_df",
            description=description,
            schema=data_df.dtypes,
            question=question,
        )

        transformation_description = get_chat_reply(
            system_transform_prompt, transformation_prompt
        )

        print("--" * 20)
        print(transformation_description)
        print("--" * 20)

        sql_transform_prompt = render_sql_prompt(
            table_name="data_df",
            description=description,
            schema=data_df.dtypes,
            sample_data=data_df.head(),
            transformation=transformation_description,
        )

        print("--" * 20)
        print(sql_transform_prompt)
        print("--" * 20)

        sql_transform_query = get_chat_reply(system_sql_prompt, sql_transform_prompt)

        print("--" * 20)
        print(sql_transform_query)
        print("--" * 20)

        transformed_df = execute_query(
            prompt=sql_transform_prompt, query=sql_transform_query, data_table=data_df
        )
        print(transformed_df)

        plotly_prompt = render_plotly_prompt(
            table_name="transformed_df",
            sample_data=transformed_df.head(),
            question=question,
        )

        print(f"Plotly prompt: {plotly_prompt}")
        plotly_code = get_chat_reply(system_plotly_prompt, plotly_prompt)

        print(f"""fig = {plotly_code}""")
        import plotly.express as px

        plotly_code = plotly_code.replace("fig.show()", "")
        exec(
            f"""fig = {plotly_code}""",
        )
        return locals()["fig"]

    else:
        return "Could not understand the question"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--description", type=str, required=True)
    parser.add_argument("--csv_path", type=str, required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv_path)
    analyze(args.question, args.description, data)
