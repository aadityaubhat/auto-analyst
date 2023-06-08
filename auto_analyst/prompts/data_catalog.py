import jinja2

environment = jinja2.Environment()

system_prompt = "You are a helpful assistant that helps find the accurate tables for a given question. Answer as concisely as possible."

source_tables_template = environment.from_string(
    """
From the list of following tables:
{{ tables_df.to_string(index=False) }}

Select the appropriate source tables for the following question:
{{ question }}

Answer in the following format:
table1, table2, table3, . . . tableN

If no appropriate tables are found, say 'No Tables Found'"""
)


def render_source_tables_prompt(question, tables_df) -> str:
    """Render prompt to select source tables for a given question
    Args:
        question (str): Question to be answered
        tables_df (pd.DataFrame): Dataframe containing list of all tables"""
    return source_tables_template.render(question=question, tables_df=tables_df)
