from auto_analyst.prompts import general
import pandas as pd
from auto_analyst.data_catalog.base import Table


def test_render_type_messages():
    question = "What is the average rating of all the movies?"
    messages = general.render_type_messages(question)
    assert messages == [
        {
            "role": "system",
            "content": "You are a helpful assistant that determines whether a question is asking for a SQL query, tabular data or a plot.",
        },
        {"role": "user", "content": "How many sales were made in August?"},
        {"role": "assistant", "content": "data"},
        {"role": "user", "content": "Relationship between customer age and time spent"},
        {"role": "assistant", "content": "plot"},
        {
            "role": "user",
            "content": "Query to get 1000 random customers who live in USA",
        },
        {"role": "assistant", "content": "query"},
        {"role": "user", "content": "What is the average amount per transaction?"},
        {"role": "assistant", "content": "data"},
        {
            "role": "user",
            "content": "1, 7, 14, 28 retention for customer who signed up in August",
        },
        {"role": "assistant", "content": "plot"},
        {"role": "user", "content": "Plot the timeseries of ad impressions"},
        {"role": "assistant", "content": "plot"},
        {"role": "user", "content": "Query to get last quarters' sales"},
        {"role": "assistant", "content": "query"},
        {"role": "user", "content": "Top 10 customers by number of transactions"},
        {"role": "assistant", "content": "data"},
        {"role": "user", "content": "Histogram of customer age"},
        {"role": "assistant", "content": "plot"},
        {"role": "user", "content": "What is the average rating of all the movies?"},
    ]


def test_render_query_prompt():
    question = "What is the average rating of all the movies?"
    source_data = [Table("movie", "Movie table")]
    table_Schema = {
        "movie": pd.DataFrame(
            {
                "column": ["id", "name", "rating"],
                "description": ["id", "name of the movie", "rating of the movie"],
            }
        )
    }
    analysis_type = "data"
    transformation = ""

    prompt = general.render_query_prompt(
        question, source_data, table_Schema, analysis_type, transformation
    )

    assert (
        prompt
        == """
Given the following tables

movie: Movie table


With schema:

movie: column         description
    id                  id
  name   name of the movie
rating rating of the movie



Write a SQL query to answer the following question:
What is the average rating of all the movies?"""
    )
