from csv_file import CSVFile
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os
from config import OPENAI_API_KEY
from prompts import (
    analytical_prompt, 
    data_prompt, 
    agg_plot_prompt, 
    sql_prompt
)
import duckdb
# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


data = CSVFile('Transaction data', csv_path="/Users/aadityabhat/Documents/autoanalyst/auto-analyst/data.csv")

llm = OpenAI(model_name='text-davinci-003')
analytical_chain = LLMChain(llm=llm, prompt=analytical_prompt)
data_answer_chain = LLMChain(llm=llm, prompt=data_prompt)
agg_plot_chain = LLMChain(llm=llm, prompt=agg_plot_prompt)

sql_chain= LLMChain(llm=llm, prompt=sql_prompt)


question = 'What are the top categories of expenses based on amount?'
description = data.description


# print('-------------------------')

# print(analytical_prompt.format(question=question))

# print('-------------------------')
# print(analytical_chain.run(question))

# print('-------------------------')

# print(data_prompt.format(description=description, question=question))

# print('-------------------------')
# print(data_answer_chain.run(description=description, question=question))

# print('-------------------------')


# print(agg_plot_prompt.format(question=question))

# print('-------------------------')
# print(agg_plot_chain.run(question=question))

# print('-------------------------')
# print(sql_prompt.format(table_name='df', column_names=data.get_columns(), question=question, description=description))

# print('-------------------------')
# query = sql_chain.run(table_name='df', column_names=data.get_columns(), question=question, description=description)

query = '''
SELECT Category, SUM(CAST(Amount AS DECIMAL)) AS Total_Expense 
FROM df
GROUP BY Category 
ORDER BY Total_Expense DESC;'''


# query = """SELECT Category, SUM(Amount) AS TotalExpense
# FROM df
# GROUP BY Category
# ORDER BY TotalExpense DESC;
# """

print(query)

df = data.df

print(duckdb.query(query).to_df())

