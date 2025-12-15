from core.build_graph import build_graph
from langchain_core.messages import HumanMessage

app = build_graph()

def run():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = app.invoke(
            {
                "question": user_input,
                "messages": [HumanMessage(content=user_input)],
                "route": None,
                "retrieved_docs": [],
                "web_retrievals": [],
                "enough_info": None,
                "final_answer": None
            }
        )
        
        print("\n=== ANSWER ===")
        print(result['final_answer'])