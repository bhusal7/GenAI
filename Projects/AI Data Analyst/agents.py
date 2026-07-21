# agents.py
from os import getenv
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from PY.tools import (
    analyze_csv,
    generate_visualizations,
    correlation_analysis,
    save_report,
)

load_dotenv()

llm = ChatMistralAI(
    model="open-mistral-7b",
    temperature=0.2,
    max_retries=5,
)

def build_eda_agent():
    return create_react_agent(
        model=llm,
        tools=[analyze_csv],
        prompt="You are an expert Data Analyst. Perform thorough dataset analysis."
    )

def build_visualization_agent():
    return create_react_agent(
        model=llm,
        tools=[generate_visualizations],
        prompt="You are an expert Data Visualization Specialist. Generate plots and explain them."
    )

def build_correlation_agent():
    return create_react_agent(
        model=llm,
        tools=[correlation_analysis],
        prompt="You are an expert Statistician. Perform detailed correlation analysis."
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional Data Science Report Writer."),
    ("human", """Create a complete report.

EDA Report:
{eda}

Visualization Report:
{visualization}

Correlation Report:
{correlation}

The report must contain:
1. Dataset Overview
2. Exploratory Data Analysis
3. Visualization Summary
4. Correlation Analysis
5. Key Insights
6. Recommendations""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Senior Data Science Reviewer."),
    ("human", "Review the report below:\n\n{report}\n\nProvide Score, Strengths, Weaknesses, and Final Verdict.")
])

critic_chain = critic_prompt | llm | StrOutputParser()