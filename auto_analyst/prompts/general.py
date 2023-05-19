import jinja2
from typing import (
    Dict,
    List,
)

environment = jinja2.Environment()

analysis_type_system_prompt = "You are a helpful assistant that determines whether a question can be answered using a SQL query, aggregation or data plot."
query_system_prompt = "You are a helpful assistant that only writes SQL queries. Reply only with SQL queries."

type_examples = [
    {"question": "How many sales were made in August?", "type": "aggregation"},
    {"question": "Relationship between customer age and time spent", "type": "plot"},
    {"question": "Query to get 1000 random customers who live in USA", "type": "query"},
    {"question": "What is the average amount per transaction?", "type": "aggregation"},
    {
        "question": "1, 7, 14, 28 retention for customer who signed up in August",
        "type": "plot",
    },
    {"question": "Plot the timeseries of ad impressions", "type": "plot"},
    {"question": "Query to get last quarters' sales", "type": "query"},
    {
        "question": "Top 10 customers by number of transactions",
        "type": "aggregation",
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


def render_type_messages(question):
    return type_messages + [{"role": "user", "content": question}]


query_template = environment.from_string(
    """
Given the following tables
{% for dct in source_data %}
{{ dct['table_name'] }}: {{ dct['description'] }}
{% endfor %}

With schema:
{% for table, schema_df in table_schema.items() %}
{{ table }}: {{ schema_df.to_string(index=False) }}
{% endfor %}

{% if analysis_type != 'plot' %}
Write a SQL query to answer the following question:
{{ question }}
{% else %}
Write a SQL query to do the following:
{{ transformation }}
{% endif %}
"""
)


def render_query_prompt(
    question: str,
    source_data: List[Dict],
    table_schema: Dict,
    analysis_type: str,
    transformation: str = "",
):
    return query_template.render(
        question=question,
        source_data=source_data,
        table_schema=table_schema,
        analysis_type=analysis_type,
        transformation=transformation,
    )
