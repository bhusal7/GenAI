import os
import sys
import time

# Ensures Python adds the workspace root to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from PY.agents import (
    build_eda_agent,
    build_visualization_agent,
    build_correlation_agent,
    writer_chain,
    critic_chain,
)

def run_csv_pipeline(csv_path: str) -> dict:
    state = {}
    
    # Step-1 : EDA agent
    print("\n" + "=" * 50)
    print("Step 1 - EDA Agent is working")
    print("=" * 50)
    eda_agent = build_eda_agent()
    eda_result = eda_agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze the CSV file located at: {csv_path}"}]
    })
    state['eda_results'] = eda_result['messages'][-1].content
    time.sleep(2)

    # Step-2 : Visualization agent
    print("\n" + "=" * 50)
    print("Step 2 - Visualization Agent is working")
    print("=" * 50)
    viz_agent = build_visualization_agent()
    viz_result = viz_agent.invoke({
        "messages": [{"role": "user", "content": f"Generate visualizations for the CSV file at: {csv_path}"}]
    })
    state['viz_results'] = viz_result['messages'][-1].content
    time.sleep(2)

    # Step-3 : Correlation agent
    print("\n" + "=" * 50)
    print("Step 3 - Correlation Agent is working")
    print("=" * 50)
    cor_agent = build_correlation_agent()
    cor_result = cor_agent.invoke({
        "messages": [{"role": "user", "content": f"Perform correlation analysis on the CSV file at: {csv_path}"}]
    })
    state['cor_results'] = cor_result['messages'][-1].content
    time.sleep(2)

    # Step-4 : Writer Chain
    print("\n" + "=" * 50)
    print("Step 4 - Writer Chain is working")
    print("=" * 50)
    state['report'] = writer_chain.invoke({
        "eda": state['eda_results'][:2000],
        "visualization": state['viz_results'][:2000],
        "correlation": state['cor_results'][:2000]
    })
    print("\n Final Report \n", state['report'])
    time.sleep(2)

    # Step-5 : Critic agent
    print("\n" + "=" * 50)
    print("Step 5 - Critic chain is working")
    print("=" * 50)
    state["feedback"] = critic_chain.invoke({
        "report": state['report'][:3000]
    })
    print("\n Critic Report Feedback \n", state["feedback"])
    
    return state

if __name__ == "__main__":
    path = input("\nEnter CSV File Path: ")
    run_csv_pipeline(path)