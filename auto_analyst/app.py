import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import auto_analyst
from html_templates.html_templates import (
    render_output_component,
    render_html_table,
)
import plotly.express as px
import plotly.figure_factory as ff
import hydralit_components as hc
import time


st.set_page_config(
    page_title="Auto Analyst",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                footer {visibility: hidden;}
                #auto-analyst {
                text-align: center;
                margin-block-start: 0em;
                margin-block-end: 0em;
                }
                #data {
                text-align: center;
                }
                #analysis {
                text-align: center;
                }
            .stSpinner > div {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            .stSpinner  {
                border-top-color: #0f0;
            }

        </style>
        """,
    unsafe_allow_html=True,
)
st.title(":chart_with_upwards_trend: Auto Analyst")

if "questions" not in st.session_state:
    st.session_state["questions"] = []

if "results" not in st.session_state:
    st.session_state["results"] = []

col1, col2 = st.columns(2)


col1.subheader("Data")
holder = col1.empty()
uploaded_file = holder.file_uploader(
    "Upload a CSV file",
    type="csv",
    accept_multiple_files=False,
    label_visibility="collapsed",
)

# Column 2 subheader centered
col2.subheader("Analysis")
placeholder = col2.empty()

if uploaded_file is not None:

    @st.cache_data
    def load_data():
        return pd.read_csv(uploaded_file)

    df = load_data()
    holder.empty()

    col1.write("First 100 rows of the data")
    col1.dataframe(df.head(100), height=250)

    description = col1.text_area("Write a brief description of the data", height=75)
    if description:
        question = col1.text_area(
            "Write a question to start exploring the data", height=75
        )
        if question:
            with placeholder:
                with st.markdown(
                    '<div class="custom-spinner-container">', unsafe_allow_html=True
                ):
                    with st.spinner(text="Analyzing..."):
                        try:
                            result = auto_analyst.analyze(
                                description=description, question=question, data_df=df
                            )
                            print(result)
                            st.session_state.questions.append(question)
                            st.session_state.results.append(result)
                        except Exception as e:
                            st.write(e)

with col2:
    with st.container():
        l = len(st.session_state.questions)
        for i in reversed(range(len(st.session_state.questions))):
            if i == l - 1:
                with st.expander(st.session_state.questions[i], expanded=True):
                    st.write(st.session_state.results[i])
            else:
                with st.expander(st.session_state.questions[i], expanded=False):
                    st.write(st.session_state.results[i])
