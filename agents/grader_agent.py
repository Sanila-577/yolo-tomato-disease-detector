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

load_dotenv()

def unified_grader_answer_agent(state: AgentState) -> AgentState:
    """
    Unified agent that:
    - Grades RAG retrieved_docs or Web retrieved results
    - Generates the final answer if enough info exists
    """

    # 1️⃣ Determine source of context using the router output
    route = state.get("route")

    if route == "rag":
        context_source = "RAG"
        context_list = state.get("retrieved_docs", [])
    elif route == "web":
        context_source = "WEB"
        context_list = state.get("web_retrievals", [])
    else:
        print(f"⚠️ No valid route for grading: {route}")
        state["enough_info"] = False
        return state

    # If nothing retrieved under that route → cannot grade
    if not context_list:
        print(f"⚠️ No {context_source} content available for grading.")
        state["enough_info"] = False
        return state


    # 2️⃣ Grading system prompt
    grader_prompt = SystemMessage(
        content=f"""
    You are a relevance grader.

    Given the following context:
    {context_list}

    And the question:
    {state['question']}

    Does the context fully answer the question?
    Reply ONLY with 'yes' or 'no'.
    """
    )

    # 3️⃣ Grade context
    grade_response = llm.invoke([grader_prompt])
    enough_info = grade_response.content.strip().lower() == "yes"
    state["enough_info"] = enough_info

    print(f"📊 Grader result: {'enough info' if enough_info else 'NOT enough info'}")

    if not enough_info:
        return state    # fallback happens outside this agent

    # 4️⃣ Generate final answer using same context
    answer_prompt = SystemMessage(
        content=f"""
    Use the following context to answer the question concisely.
    Quote or reference the relevant parts from the context.
    Do NOT say 'I don't have enough information' if the answer is present in the context.

    Context:
    {context_list}

    Question:
    {state['question']}
    """
    )

    final_response = llm.invoke([answer_prompt])
    state["final_answer"] = final_response.content.strip()

    print("✅ Final answer generated.")
    print(f"Current state is: {state}")
    return state