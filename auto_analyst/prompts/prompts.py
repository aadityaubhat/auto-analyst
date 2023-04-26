import jinja2

environment = jinja2.Environment()

system_prompt = "You are a helpful assistant that answers analytical questions. Answer as concisely as possible."
system_yes_no_prompt = "Answer yes or no."
system_sql_prompt = "You are a helpful assistant that only writes SQL SELECT queries."
system_plotly_prompt = (
    "You are a helpful assistant that only writes Python code using plotly library."
)
system_transform_prompt = "You are a helpful assistant that only describes data transformations. Answer in plain english and be as concisely as possible."

analytical_examples = [
    {"question": "How many sales were made in August?", "is_analytical": "yes"},
    {"question": "What is the average amount per transaction?", "is_analytical": "yes"},
    {"question": "How can we increase revenue?", "is_analytical": "no"},
    {"question": "Plot the timeseries of ad impressions", "is_analytical": "yes"},
    {"question": "Why are the sales declining?", "is_analytical": "no"},
    {
        "question": "Who are the top 10 customers by number of transactions?",
        "is_analytical": "yes",
    },
    {"question": "What is the puprose of life?", "is_analytical": "no"},
]

analytical_template = environment.from_string(
    """
Determine whether a question can be answered using simple aggregations or plotting of data. Answer yes or no.

{%- for example in examples %}
Question: {{ example['question'] }}
Can be answered by data: {{ example['is_analytical'] }}
{%- endfor %}
Question: {{ question }}
Can be answered by data:"""
)


def render_analytical_prompt(question):
    return analytical_template.render(examples=analytical_examples, question=question)


data_examples = [
    {
        "description": "A CSV file with data about sales",
        "question": "How many sales were made in August?",
        "can_be_answered": "yes",
    },
    {
        "description": "Customer complaints csv file",
        "question": "What are the most common customer complaints about?",
        "can_be_answered": "yes",
    },
    {
        "description": "Customer visits data",
        "question": "What are the top 10 selling products?",
        "can_be_answered": "No",
    },
    {
        "description": "Customer demographics",
        "question": "Plot the histogram of customer age",
        "can_be_answered": "Yes",
    },
    {
        "description": "Marketting emails data",
        "question": "Who is our oldest customer?",
        "can_be_answered": "no",
    },
    {
        "description": "Marketting emails data",
        "question": "What are the best times to send the marketting emails?",
        "can_be_answered": "yes",
    },
]

data_template = environment.from_string(
    """
Determine whether the asked question can be answered using given data. Answer yes or no.

{%- for example in examples %}
Given the data: {{ example['description'] }}
Question: {{ example['question'] }}
Can be answered by given data: {{ example['can_be_answered'] }}{%- endfor %}
Given the data: {{ description }}
Question: {{ question }}
Can be answered by given data:"""
)


def render_data_prompt(description, question):
    return data_template.render(
        examples=data_examples, description=description, question=question
    )


agg_plot_examples = [
    {"question": "How many sales were made in August?", "type": "aggregate"},
    {"question": "What is the average amount per transaction?", "type": "aggregate"},
    {"question": "Plot the timeseries of ad impressions", "type": "plot"},
    {
        "question": "Who are the top 10 customers by number of transactions?",
        "type": "aggregate",
    },
    {"question": "Histogram of customer age", "type": "plot"},
]

agg_prompt_template = environment.from_string(
    """
Determine whether the asked question can be answered using aggregate data or a plot. Answer aggregate or plot.

{%- for example in examples %}
Question: {{ example['question'] }}
Type: {{ example['type'] }}
{%- endfor %}
Question: {{ question }}
Type:"""
)


def render_agg_plot_prompt(question):
    return agg_prompt_template.render(examples=agg_plot_examples, question=question)


sql_template = environment.from_string(
    """
Table {{ table_name }} has description '{{ description }}'. 

The schema of the table is:
{{ schema }}

Here are the first 5 rows of the data:
{{ sample_data }}

{% if question %}
Write a DuckDB SQL query to answer the following question:
{{ question }}
{% endif %}

{% if transformation %}
Write a DuckDB SQL query to do the following:
{{ transformation }}
{% endif %}

DuckDB SQL Query:"""
)


def render_sql_prompt(table_name, description, schema, sample_data, **kwargs):
    if kwargs.get("question"):
        question = kwargs["question"]
        return sql_template.render(
            table_name=table_name,
            description=description,
            schema=schema,
            sample_data=sample_data,
            question=question,
        )

    if kwargs.get("transformation"):
        transformation = kwargs["transformation"]
        return sql_template.render(
            table_name=table_name,
            description=description,
            schema=schema,
            sample_data=sample_data,
            transformation=transformation,
        )


sql_error_template = environment.from_string(
    """
{{ prompt }}{{ query }}

Fails with the following error:
{{ error }}

New Query:"""
)


def render_sql_error_prompt(prompt, query, error):
    return sql_error_template.render(prompt=prompt, query=query, error=error)


plotly_template = environment.from_string(
    """
First 5 rows of the Dataframe '{{ table_name }}' are:
{{ sample_data }}

Write plotly code to store the following plot in `fig` variable:
{{ question }}

Plotly code:

import plotly.express as px
fig ="""
)


def render_plotly_prompt(table_name, sample_data, question):
    return plotly_template.render(
        table_name=table_name, sample_data=sample_data, question=question
    )


transform_template = environment.from_string(
    """
Table {{ table_name }} has description '{{ description }}'. 

The schema of the table is:
{{ schema }}

The plotting question:
{{ question }}

Write transformations needed to plot the data:
1."""
)


def render_transform_prompt(table_name, description, schema, question):
    return transform_template.render(
        table_name=table_name, description=description, schema=schema, question=question
    )
