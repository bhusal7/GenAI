from __future__ import annotations
from typing import Dict
from pathlib import Path

import sys
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from RAG.indexing import build_rag
from Tools.tools import set_retriever, read_code, save_report
from Agents.agents import (
    user_agent,
    research_agent,
    bug_agent,
    optimization_agent,
    documentation_agent,
    explain_chain,
    critic_chain,
)

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

retriever = build_rag(str(DATA_DIR))
set_retriever(retriever)

retriever = build_rag("data")
set_retriever(retriever)


def run_code_assistant_pipeline(query: str) -> Dict:
    state = {}

    state["query"] = query
    state["context"] = read_code.invoke(query)

    # Step-1 : User Agent
    print("\n" + "=" * 50)
    print("Step 1 - User Agent is working")
    print("=" * 50)

    user_reponse = user_agent()
    user_result = user_reponse.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["user_responses"] = user_result["messages"][-1].content

    # Step-2 : Research Agent
    print("\n" + "=" * 50)
    print("Step 2 - Research Agent is working")
    print("=" * 50)

    research_reponse = research_agent()
    research_result = research_reponse.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["research_responses"] = research_result["messages"][-1].content

    # Step-3 : Bug Agent
    print("\n" + "=" * 50)
    print("Step 3 - Bug Agent is working")
    print("=" * 50)

    bug_reponse = bug_agent()
    bug_result = bug_reponse.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["bug_responses"] = bug_result["messages"][-1].content

    # Step-4 : Optimization Agent
    print("\n" + "=" * 50)
    print("Step 4 - Optimization Agent is working")
    print("=" * 50)

    optimization_reponse = optimization_agent()
    optimization_result = optimization_reponse.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["optimization_responses"] = optimization_result["messages"][-1].content

    # Step-5 : Documentation Agent
    print("\n" + "=" * 50)
    print("Step 5 - Documentation Agent is working")
    print("=" * 50)

    documentation_reponse = documentation_agent()
    documentation_result = documentation_reponse.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["documentation_responses"] = documentation_result["messages"][-1].content

    # Step-6 : Explain Chain
    print("\n" + "=" * 50)
    print("Step 6 - Explain Chain is working")
    print("=" * 50)

    state["report"] = explain_chain.invoke(
        {"query": state["query"][:2000], "context": state["context"][:2000]}
    )
    print("\n Final Report:", state["report"])

    # Step-7 : Critic Chain
    print("\n" + "=" * 50)
    print("Step 7 - Critic Chain is working")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke(
        {"draft": state["report"][:3000]}
    )
    print("\n Critic Report Feedback \n", state["feedback"])

    # Step 8 : Save Report
    print("\n" + "=" * 60)
    print("Step 8 - Saving Report")
    print("=" * 60)

    save_report.invoke(
        {
            "content": state["feedback"],
            "filename": "AI_Code_Assistant_Report",
        }
    )

    return state


if __name__ == "__main__":
    user_input = input("Input :- ")
    run_code_assistant_pipeline(user_input)