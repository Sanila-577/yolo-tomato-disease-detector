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
        - chat (greetings, casual conversation, or questions about the detected disease that are already provided in the context)
        - rag (plant disease knowledge from database - symptoms, causes, prevention methods)
        - web (general knowledge or information not related to plant diseases)

        Rules:
        1. If the question asks about the disease NAME itself (e.g., "what is the name of the disease?"), route to 'chat' since it's in the system context
        2. If the question asks about disease treatment, symptoms, causes, or prevention, route to 'rag'
        3. Otherwise route to 'web' or 'chat' based on the question type

        Answer with only one intent: chat, rag, or web.
        Do Not Include Any Other Text
        """
    )

    messages = [system_prompt] + state["messages"]
    response = llm.invoke(messages)

    route = response.content.strip().lower().replace("\n", "").replace(" ", "")

    # Only allow valid routes
    if route not in ["chat", "rag", "web"]:
        print(f"⚠️ Router returned invalid route: {repr(route)}. Defaulting to 'rag'.")
        route = "rag"

    state["route"] = route
    print(f"🔀 Router: Routed to {state['route']}")
    return state