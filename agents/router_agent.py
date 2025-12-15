from typing import TypedDict, Annotated, Sequence, Optional, List, Literal
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

from langchain_community.embeddings import HuggingFaceEmbeddings
from tavily import TavilyClient
from agents.state import AgentState
from core.llm import llm

load_dotenv()

def router_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content = """
        Classify the user's question into one of these intents:
        - chat (greetings or casual conversation)
        - rag (plant knowledge)
        - web (general knowledge)

        Answer with only one intent: chat, rag, or web.
        Do Not Include Any Other Text
        """
    )

    messages = [system_prompt] + state["messages"]
    response = llm.invoke(messages)

    route = response.content.strip().lower().replace("\n", "").replace(" ", "")

    # Only allow valid routes
    if route not in ["chat", "rag", "web"]:
        print(f"⚠️ Router returned invalid route: {repr(route)}. Defaulting to 'chat'.")
        route = "chat"

    state["route"] = route
    print(f"🔀 Router: Routed to {state['route']}")
    return state