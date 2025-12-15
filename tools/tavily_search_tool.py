@tool
def tavily_search_tool(query: str) -> str:
    """
    Perform web scraping for the query using Tavily.
    Returns a combined string of results.
    """
    print("🌍 In Tavily Search Tool")
    try:
        web_data = tavily.search(query, max_results=3)
        results = [r["content"] for r in web_data.get("results", [])]
        return "\n\n".join(results) if results else "No web results found."
    except Exception as e:
        return f"Web search failed: {str(e)}"