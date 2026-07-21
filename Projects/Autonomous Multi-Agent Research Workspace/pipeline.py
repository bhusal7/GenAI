from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain

def run_research_pipeline(topic:str) -> dict:
    
    state = {}
    
    # Step-1 : search agent working
    print("\n" + "="*50)
    print("Step 1 - Search Agent is working")
    print("="*50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detected information about : {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content
    
    print("\n search_result", state['search_results'])
    
    
     # Step-2 : reader agent working
    print("\n" + "="*50)
    print("Step 2 - Search Agent is scraping top resources ...")
    print("="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user",
            f"Based on the following search results about '{topic}',"
            f"Pick the most revelent URL and scrape it for deeper content.\n\n"
            f"Search results:\n{state['search_results'][:800]}"
        )]
    })
    state["reader_results"] = reader_result["messages"][-1].content
    print("\n Scraped Content of Reader Results\n", state["reader_results"])
    
    
    # Step-3 : writer chain
    print("\n" + "="*50)
    print("Step-3 : Writer is drafting the report...")
    print("="*50)
    
    research_combined = (
        f"SEARCH RESULTS :\n {state['search_results']} \n\n "
        f"DETAILD SCRAPED CONTENT:\n {state['reader_results']}\n\n" 
    )
    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })
    print("\n Final Report \n",state['report'])
    
    
    # Step-4 : critic chain
    print("\n" + "="*50)
    print("Step-4 : Critic is reviewing the report ...")
    print("="*50)
    
    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })
    print("\n Critic Report Feedback \n", state["feedback"])
    
    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic :- ")
    run_research_pipeline(topic)