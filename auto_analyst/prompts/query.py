import jinja2

environment = jinja2.Environment()

system_prompt = "You are a helpful assistant that only writes SQL queries. Answer as concisely as possible."

sql_template = environment.from_string(
    """
For following tables:
{{ source_data.table_name }}: {{ source_data.description }} 

With schema:
{{ schema }}

{% if question %}
Write a SQL query to answer the following question:
{{ question }}
{% endif %}
{% if transformation %}
Write a SQL query to do the following:
{{ transformation }}
{% endif %}

SQL Query:"""
)
