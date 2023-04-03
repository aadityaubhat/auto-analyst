# Auto-Analyst

Auto-Analyst is a powerful UI tool that simplifies the process of running analytical queries on your data using plain English. With Auto-Analyst, you can easily perform complex data aggregations, visualizations, and analyses without writing a single line of code.

## Demo

![Demo gif](https://github.com/aadityaubhat/auto-analyst/blob/main/auto_analyst/auto-analyst-demo.gif)

## Features

- Natural Language Processing (NLP) using Large Language Models (LLMs) to understand user input
- Simple and intuitive UI to interact with data and see resulting tables and charts
- Built-in support for popular data analysis libraries (Pandas, NumPy, Matplotlib, Seaborn)
- Your data remains local; it is never uploaded anywhere else
- Extensible and customizable to cater to specific use-cases

## Run Locally

To run Auto-Analyst locally do the following steps

- Clone the repo
- Create Python virtual environment
- Install requirements.txt
- Update auto_analyst/config.py with your OpenAI API key
- Run `streamlit run /auto_analyst/app.py`
