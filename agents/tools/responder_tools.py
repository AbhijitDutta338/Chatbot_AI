from langchain.agents import Tool

def get_responder_tools():
    # Define responder specific tools here, e.g., doc_search, dispatch
    doc_search_tool = Tool(
        name="DocSearchTool",
        func=lambda query: "Document search result for: " + query,
        description="Search documents for responder queries."
    )
    dispatch_tool = Tool(
        name="DispatchTool",
        func=lambda query: "Dispatch action performed for: " + query,
        description="Dispatch responders based on query."
    )
    return [doc_search_tool, dispatch_tool]
