from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.router_agent import router_agent
from agents.chat_agent import chat_agent
from agents.retriever_agent import retrieve_agent
from agents.web_agent import web_answer_agent
from agents.grader_agent import unified_grader_answer_agent

load_dotenv()

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_agent)
    graph.add_node("chat_agent", chat_agent)
    graph.add_node("retriever", retrieve_agent)
    graph.add_node("web_scraper", web_answer_agent)
    graph.add_node("grader_answer_generator", unified_grader_answer_agent)

    graph.set_entry_point("router")

    # conditonal edges
    graph.add_conditional_edges(
        "router",
        lambda s: s["route"],
        {
            "chat":"chat_agent",
            "rag": "retriever",
            "web": "web_scraper"
        }
    )

    graph.add_edge("retriever", "grader_answer_generator")
    graph.add_edge("web_scraper", "grader_answer_generator")

    graph.add_conditional_edges(
        "grader_answer_generator",
        lambda s: f"{s['route']}_{s['enough_info']}",  # string key
        {
            "rag_False": "web_scraper",
            "rag_True": END,
            "web_False": END,
            "web_True": END
        }
    )

    graph.add_edge("chat_agent", END)

    app = graph.compile()

    return app
