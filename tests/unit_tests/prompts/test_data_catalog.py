from auto_analyst.prompts import data_catalog
import pandas as pd


def test_render_source_table_prompt():
    question = "What is the average rating of all the movies?"
    tables_df = pd.DataFrame(
        {
            "table_name": ["table1", "table2", "table3"],
            "table_description": ["desc1", "desc2", "desc3"],
        }
    )
    prompt = data_catalog.render_source_tables_prompt(question, tables_df)
    assert (
        prompt
        == """
From the list of following tables:
table_name table_description
    table1             desc1
    table2             desc2
    table3             desc3

Select the appropriate source tables for the following question:
What is the average rating of all the movies?

Answer in the following format:
table1, table2, table3, . . . tableN

If no appropriate tables are found, say 'No Tables Found'"""
    )
