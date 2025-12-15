@tool
def retriever_tool(query: str) -> str:
    """
    Retrieve relevant document chunks from FAISS.
    """
    print("In the Retriever tool")
    docs = retriever._get_relevant_documents(query, run_manager=None)
    return "\n\n".join([d.page_content for d in docs])
