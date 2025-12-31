from core.build_graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage

app = build_graph()

def run_graph(user_input:str, messages=None):

    if messages is None:
        messages = []
            
    messages.append([HumanMessage(content=user_input)])# converts back to a HumanMessage type

    result = app.invoke(
        {
            "question": user_input,
            "messages": messages,
            "route": None,
            "retrieved_docs": [],
            "web_retrievals": [],
            "enough_info": None,
            "final_answer": None
        }
    )
    
    print("\n=== ANSWER ===")
    print(result['final_answer'])

    messages.append(AIMessage(content=result["final_answer"]))
    return result["final_answer"], messages

