import jinja2
from typing import (
    Dict,
    List,
    Optional,
)
from ..data_catalog.base import Table

environment = jinja2.Environment()

analysis_type_system_prompt = "You are a helpful assistant that determines whether a question is asking for a SQL query, tabular data or a plot."
query_system_prompt = "You are a helpful assistant that only writes SQL SELECT queries. Reply only with SQL queries, wrap your query in triple backquotes."
transformed_data_system_prompt = "You are a helpful assistant that assists in defining the data needed to answer a question."
plotly_system_prompt = "You are a helpful assistant that only writes Python code using plotly library. Reply only with Python code, wrap your query in triple backquotes."
yes_no_system_prompt = "You are a helpful assistant that answers yes or no questions. Reply only with yes or no."

type_examples = [
    {"question": "How many sales were made in August?", "type": "data"},
    {"question": "Relationship between customer age and time spent", "type": "plot"},
    {"question": "Query to get 1000 random customers who live in USA", "type": "query"},
    {"question": "What is the average amount per transaction?", "type": "data"},
    {
        "question": "1, 7, 14, 28 retention for customer who signed up in August",
        "type": "plot",
    },
    {"question": "Plot the timeseries of ad impressions", "type": "plot"},
    {"question": "Query to get last quarters' sales", "type": "query"},
    {
        "question": "Top 10 customers by number of transactions",
        "type": "data",
    },
    {"question": "Histogram of customer age", "type": "plot"},
]

type_messages = [
    {"role": "system", "content": analysis_type_system_prompt},
] + [
    elem
    for example in type_examples
    for elem in [
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["type"]},
    ]
]


def render_type_messages(question) -> List[Dict[str, str]]:
    """Render type messages
    Args:
        question (str): Question to be answered
    Returns:
        List[Dict[str, str]]: List of messages to be displayed to the user"""
    return type_messages + [{"role": "user", "content": question}]


query_template = environment.from_string(
    """
Given the following tables
{% for tbl in source_data %}
{{ tbl.name }}: {{ tbl.description }}
{% endfor %}

With schema:
{% for table, schema_df in table_schema.items() %}
{{ table }}: {{ schema_df.to_string(index=False) }}
{% endfor %}

{% if analysis_type != 'plot' %}
Write a SQL query to answer the following question:
{{ question }}{% else %}
Write a SQL query to get the following data:
{{ transformed_data }}
{% endif %}"""
)


def render_query_prompt(
    question: str,
    source_data: List[Table],
    table_schema: Dict,
    analysis_type: str,
    transformed_data: str = "",
) -> str:
    """Render prompt to write a SQL query
    Args:
        question (str): Question to be answered
        source_data (List[Table]): List of source tables
        table_schema (Dict): Dictionary of table schemas
        analysis_type (str): Type of analysis
        transformed_data (str, optional): Transformed data. Defaults to "".
    Returns:
        str: Prompt to write a SQL query"""
    return query_template.render(
        question=question,
        source_data=source_data,
        table_schema=table_schema,
        analysis_type=analysis_type,
        transformed_data=transformed_data,
    )


update_query_template = environment.from_string(
    """
    Instructions:
    {{ prompt }}

    Query: 
    {{ query }}

    Failed with following error:
    {{ error }}

    Please update the query to answer the question.
    """
)


def render_update_query_prompt(
    prompt: Optional[str],
    query: Optional[str],
    error: Optional[str],
) -> str:
    """Render prompt to update a SQL query
    Args:
        prompt (Optional[str]): Prompt to update the query
        query (Optional[str]): SQL query
        error (Optional[str]): Error message
    Returns:
        str: Prompt to update a SQL query"""
    return update_query_template.render(
        prompt=prompt,
        query=query,
        error=error,
    )


transformed_data_template = environment.from_string(
    """
Given the following tables
{% for tbl in source_data %}
{{ tbl.name }}: {{ tbl.description }}
{% endfor %}

With schema:
{% for table, schema_df in table_schema.items() %}
{{ table }}: {{ schema_df.to_string(index=False) }}
{% endfor %}

Define table 'result_data' needed following question:
{{ question }}

Answer in following format:
Name: result_data
Description: <description of data>
Schema

Column Name | Type | Description
"""
)


def render_transformed_data_prompt(
    question: str,
    source_data: List[Table],
    table_schema: Dict,
) -> str:
    """Render prompt to define transformed data
    Args:
        question (str): Question to be answered
        source_data (List[Table]): List of source tables
        table_schema (Dict): Dictionary of table schemas
    Returns:
        str: Prompt to define transformed data"""
    return transformed_data_template.render(
        question=question,
        source_data=source_data,
        table_schema=table_schema,
    )


plotly_code_template = environment.from_string(
    """
For dataframe with following schema:
{{ transformed_data }}

Write plotly code to store the following plot in `fig` variable, don't call fig.show():
{{ question }}"""
)


def render_plotly_code_prompt(
    question: str,
    transformed_data: str,
) -> str:
    """Render prompt to write plotly code
    Args:
        question (str): Question to be answered
        transformed_data (str): Transformed data
    Returns:
        str: Prompt to write plotly code"""
    return plotly_code_template.render(
        question=question,
        transformed_data=transformed_data,
    )


plotly_code_check_template = environment.from_string(
    """
Does the following Python code store a plotly plot in `fig` variable?
{{ code }}

Answer only with yes or no. If you are unsure, answer no."""
)


def render_plotly_code_check_prompt(
    code: str,
) -> str:
    """Render prompt to check plotly code
    Args:
        code (str): Python code
    Returns:
        str: Prompt to check plotly code"""
    return plotly_code_check_template.render(
        code=code,
    )
